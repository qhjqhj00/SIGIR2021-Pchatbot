import os
import json
from multiprocessing import Process

class Worker():
    def __init__(self, src_fp, tgt_fp, func):
        self.src_fp = src_fp
        self.tgt_fp = tgt_fp
        self.parse_line = func
        self.postfix = '.pid.'

    def run(self, pid, p_num):
        pid_file_fp = self.tgt_fp + self.postfix + str(pid)
        with open(self.src_fp, 'r') as f_in, open(pid_file_fp, 'w') as f_out:
            for idx, line in enumerate(f_in):
                if idx % p_num != pid: continue
                out_string = self.parse_line(json.loads(line))
                if out_string: f_out.write(json.dumps(out_string, ensure_ascii=False) + '\n')

    def merge_result(self, keep_pid_file=False):
        os.system('cat %s%s* > %s' % (self.tgt_fp, self.postfix, self.tgt_fp))
        if not keep_pid_file:
            os.system('rm %s%s*' % (self.tgt_fp, self.postfix))

class MultiProcessor():
    def __init__(self, worker, pid_num):
        self.worker = worker
        self.pid_num = pid_num

    def run(self):
        for pid in range(self.pid_num):
            p = Process(target= self.worker.run, args = (pid, self.pid_num))
            p.start()
            
        for pid in range(self.pid_num):
            p.join()

if __name__ == "__main__":
    import json
    def parse_line(line):
        # 定义解析文件行数据的函数，输出为处理后的保存到文件的字符串
        return str(json.loads(line)['_id'])
        
    worker = Worker('test/test.json', 'test/test_mp_out.json', parse_line)
    mp = MultiProcessor(worker, 10)
    mp.run()
    print("All Processes Done.")
    worker.merge_result(keep_pid_file=True)