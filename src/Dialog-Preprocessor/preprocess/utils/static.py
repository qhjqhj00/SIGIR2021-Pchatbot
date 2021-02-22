import re
import pkuseg
from tqdm import tqdm
from collections import Counter


class Statistics():
    def __init__(self,data):
        self.data = data
        self.min_length = 5
        self.max_length = 100
        self.post_num = 0
        self.resp_num = 0
        self.err_data = 0
    def word_freq(self):
        seg = pkuseg.pkuseg(model_name='web')
        # seg = pkuseg.pkuseg()
        stopwords = []
        text = []
        new_text = []
        with open("stopwords.txt","r") as f:
            stopwords = f.read()
        for line in tqdm(self.data):
            post, resp = line[0],line[1:]
            text.extend(seg.cut(post))
            for r in resp:
                text.extend(seg.cut(r))

        for word in text:
            if word not in stopwords:
                new_text.append(word)
        couter = Counter(new_text)
        print('Start create user_dictionary')
        with open("word_user.txt","w") as fout:
            for k,v in tqdm(couter.most_common()):
                fout.write(k + '\t' + str(v) + '\n')

    def check_sentence_length(self):
        bucket_p = {}
        bucket_r = {}
        new_data = []
        d = (self.max_length - self.min_length) / 10
        for line in self.data:
            resps = []
            post,resp = line[0], line[1:]
            self.post_num += 1
            post = self.check_lenth(post)
            k = str(int((len(post) - self.min_length) / d))
            bucket_p[k] = bucket_p[k] + 1 if k in bucket_p else 1
            for r in resp:
                self.resp_num += 1
                r = self.check_lenth(r)
                k = str(int((len(r) - self.min_length) / d))
                bucket_r[k] = bucket_r[k] + 1 if k in bucket_r else 1
                if r: resps.append(r)
            if not post or not resps: continue
            new_data.append([post]+resps)
        print('Total Post:%d , Response: %d , Pair: %d , Avg_Pair: %f ' % (self.post_num,self.resp_num,self.resp_num,1.0 * self.resp_num / self.post_num))
        with open("sentence_length.txt","w") as f:
            for kv in sorted(bucket_p.items(),key = lambda d: int(d[0])):
                key = kv[0]
                value = kv[1]
                idx = int(key)
                f.write('Post length %d - %d : %d \n' % (self.min_length + idx * d, self.min_length + (idx + 1) * d - 1, value))
            for kv2 in sorted(bucket_r.items(),key = lambda d: int(d[0])):
                key = kv2[0]
                value = kv2[1]
                idx = int(key)
                f.write('Response length %d - %d : %d \n' % (self.min_length + idx * d, self.min_length + (idx + 1) * d - 1, value))
            self.data = new_data
        return new_data
                         
    def check_lenth(self,sentence):
        if len(sentence) < self.min_length or len(sentence) > self.max_length:
            with open("err_data.txt","w") as f:
                f.write('empty data \n') if len(sentence) == 0 else f.write('error data: %s, %d\n' % (sentence,len(sentence))) 
            self.err_data += 1
            return ""
        return sentence







