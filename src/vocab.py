# raw_data : weibo_corpus.cutted format data
# data: post.train format data
import sys
import json
import random
import os
from collections import Counter
from tqdm import tqdm

def get_data_vocab(data, vocab_num=40000):
    # <unk> <s> </s> first
    # format data/src_vocab_file
    vocab_dic = {}
    for text in data:
        words = text.split(' ')
        for w in words:
            if not w: continue
            vocab_dic[w] = vocab_dic.get(w, 0) + 1
    vocab = [k for k, _ in sorted(vocab_dic.items(), key=lambda x: -x[1])]
    # vocab = ['<unk>', '<s>', '</s>'] + vocab[:vocab_num - 3]
    return vocab[:vocab_num]

def get_userID_vocab(data, vocab_num=80000):
    vocab_dic = Counter(data)
    vocab = [k for k, _ in sorted(vocab_dic.items(), key=lambda x: -x[1])]
    # vocab = ['<unk>'] + vocab[:vocab_num-1]
    return vocab[:vocab_num]

def load_data(raw_data):
    post, resp = [], []
    resp_userID = []
    phase = 'train'
    with open(os.path.join(raw_data, 'post.'+phase), 'r') as fpost, open(os.path.join(raw_data, 'resp.'+phase), 'r') as fresp, open(os.path.join(raw_data, 'resp_id.'+phase), 'r') as fuser:
        for p, r, u in zip(fpost, fresp, fuser):
            post.append(p.strip())
            resp.append(r.strip())
            resp_userID.append(u.strip())
    assert len(post) == len(resp) == len(resp_userID)
    return post, resp, resp_userID

def save_data(fp, data):
    print(f"Save {fp}")
    with open(fp, 'w') as f:
        for text in tqdm(data):
            f.write(text + '\n')

if __name__ == "__main__":
    raw_fp, save_dir, phase, vocab_size, userID_vocab_size = sys.argv[1:]
    save_dir = save_dir.rstrip('/')
    vocab_size = int(vocab_size)
    userID_vocab_size = int(userID_vocab_size)
    post, resp, resp_userID = load_data(raw_fp)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    if phase == "train":
        if vocab_size:
            post_vocab = get_data_vocab(post, vocab_num=vocab_size)
            resp_vocab = get_data_vocab(resp, vocab_num=vocab_size)
            save_data(f"{save_dir}/src_vocab_file_" + str(vocab_size), post_vocab)
            save_data(f"{save_dir}/tgt_vocab_file_" + str(vocab_size), resp_vocab)

        if userID_vocab_size:
            resp_userID_vocab = get_userID_vocab(resp_userID, vocab_num=userID_vocab_size)
            save_data(f"{save_dir}/tgt_userID_vocab_file_" + str(vocab_size), resp_userID_vocab)