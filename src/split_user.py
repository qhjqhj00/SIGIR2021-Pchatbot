import json
import re
import os
from tqdm import tqdm
from collections import Counter, defaultdict

from statistics import Statistics


def load(fp, patition=None):
    def clean(subs):
        if re.search(r'【.*】', subs[0]): return False
        if len(subs[0].split(' ')) > 60: return False
        return True
    data = []
    cnt = 0
    with open(fp, 'r') as f:
        for line in tqdm(f, desc="Load Data: "):
            cnt += 1
            if not cnt % 2:
                subs += line.strip().split('\t')
                assert len(subs) == 8
                if not patition: 
                    data.append(subs)
                elif subs[6] == patition or subs[6] in patition: 
                    if clean(subs):
                        data.append(subs)
                else: break
            else:
                subs = line.strip().split('\t')
    return data

def filter_data(data):
    history_cnt = Counter([subs[4] for subs in data])
    Statistics.get_bucket(history_cnt.values())
    return data

def get_user_data(model_data_dir, data):
    if not os.path.exists(model_data_dir):
        os.makedirs(model_data_dir)
    user_data = defaultdict(list)
    #p, pid, ptime, u, uid, utime, part, train/dev/test
    for subs in tqdm(data):
        sub = subs[:6]
        user_data[subs[4]].append(sub)
    for k, v in tqdm(user_data.items(), desc="Store"):
        with open(model_data_dir + str(k), 'w') as fp:
            fp.write(json.dumps(v, ensure_ascii=False))

if __name__ == "__main__":
    data_fp = "../data/sample.txt"
    model_data_dir = "../data/sample_byuser_filter/"
    data = load(data_fp, patition=['1'])
    data = filter_data(data)
    get_user_data(model_data_dir, data)


    