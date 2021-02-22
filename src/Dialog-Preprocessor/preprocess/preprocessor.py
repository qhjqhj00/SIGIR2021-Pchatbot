import os
import json

from tqdm import tqdm

from utils.filter import Filter
from utils.multi_process_wraper import *
from utils.cutter import Cutter
from utils.statistic import Statistics

class Preprocessor():
    def __init__(self, filter_obj=None):
        if not filter_obj:
            filter_obj = Filter()
        self.filter_obj = filter_obj
        self.post2freq = {}
        self.resp2freq = {}

    @staticmethod
    def load(fp):
        data = []
        with open(fp, 'r') as f:
            for line in f:
                subs = json.loads(line)
                if len(subs) <= 1:
                    continue
                data.append(subs)
        return data

    @staticmethod
    def save(fp, data):
        if not data:
            return "No Data."
        with open(fp, 'w') as f:
            for line in data:
                if len(line) > 1:
                    f.write(json.dumps(line, ensure_ascii=False) + "\n")

    @staticmethod
    def update_data(data, infos):
        assert len(data) == len(infos)
        if not infos[0]: return []
        new_line = []
        for item, info in zip(data, infos):
            if info:
                item[0] = info
                new_line.append(item)
        return new_line

    def local_preprocess(self, line):
        post = self.filter_obj.single_text_pipe(line[0][0])
        if not post: return []

        texts = [self.filter_obj.single_text_pipe(item[0]) for item in line]
        threshold = self.filter_obj.max_reread_patience
        rereader_killer = self.filter_obj.text2frequency(texts[1:], threshold)
        for idx, r in enumerate(texts[1:], start=1):
            if r: r = self.filter_obj.reread_machine_unit(r, rereader_killer)
            if r: r = self.filter_obj.balance_length_unit(post, r)
            texts[idx] = r

        new_line = self.update_data(line, texts)
        if len(new_line) > 1: 
            return new_line
        return []

    def global_preprocess(self, line):
        texts = [item[0] for item in line]
        texts[0] = self.filter_obj.clip_text_freq_unit(texts[0], self.post2freq)
        if not texts[0]:
            return []
        for idx, r in enumerate(texts[1:], start=1):
            if r: r = self.filter_obj.clip_text_freq_unit(r, self.resp2freq)
            texts[idx] = r
        new_line = self.update_data(line, texts)
        if len(new_line) > 1: 
            return new_line
        return []

    def get_data_frequency(self, data):
        all_posts, all_resps = [], []
        for line in data:
            all_posts.append(line[0][0])
            all_resps.extend([item[0] for item in line[1:]])

        threshold = self.filter_obj.max_text_freq
        post2freq = self.filter_obj.text2frequency(all_posts, threshold)
        resp2freq = self.filter_obj.text2frequency(all_resps, threshold)
        return post2freq, resp2freq

    def run(self, data):
        print('Start Local Preprocessing')
        coarse_data = []
        for line in tqdm(data):
            # line = self.local_preprocess(line)
            if line: coarse_data.append(line)
        data = coarse_data
        
        new_data = []
        self.post2freq, self.resp2freq = self.get_data_frequency(data)
        print('Start Global Preprocessing')
        for line in tqdm(data):
            line = self.global_preprocess(line)
            if line: new_data.append(line)
        data = new_data

        return data

    def run_mp(self, src_fp, tgt_fp, pid_num=5, keep_pid_file=True):
        coarse_fp = tgt_fp + '.coarse'
        worker = Worker(src_fp, coarse_fp, self.local_preprocess)
        mp = MultiProcessor(worker, pid_num)
        mp.run()
        print("All Local Processes Done.")
        worker.merge_result(keep_pid_file=keep_pid_file)

        data = self.load(coarse_fp)
        self.post2freq, self.resp2freq = self.get_data_frequency(data)
        del data

        worker = Worker(coarse_fp, tgt_fp, self.global_preprocess)
        mp = MultiProcessor(worker, pid_num)
        mp.run()
        print("All Global Processes Done.")
        worker.merge_result(keep_pid_file=keep_pid_file)

if __name__ == '__main__':
    os.system("mkdir -p logging")
    pid_num = 25
    P = Preprocessor()
    filter_obj = Filter(logging_fp="./logging/filter_all.log")
    P = Preprocessor(filter_obj)
    src_fp, tgt_fp = 'test/Weibo_24_35.sample.10000', 'test/weibo_corpus'
    # src_fp, tgt_fp = '/home/xiaohe_li/0_data/Weibo_24_35.raw.out', '/home/xiaohe_li/0_data/weibo_whole.corpus'
    P.run_mp(src_fp, tgt_fp, pid_num, keep_pid_file=False)
    
    # data = P.load(src_fp)
    # data = P.run(data)
    # P.save('corpus/weibo_corpus', data)

    print("Begin Cut Sentences.")
    cutted_fp = tgt_fp + '.cutted'
    cutter = Cutter(method='pkuseg')
    worker = Worker(tgt_fp, cutted_fp, cutter.cut_data_line)
    mp = MultiProcessor(worker, pid_num)
    mp.run()
    worker.merge_result(keep_pid_file=False)
    print('Finish.')

    print('Stat.')
    data = P.load(cutted_fp)
    Statistics.stat_data(data)

