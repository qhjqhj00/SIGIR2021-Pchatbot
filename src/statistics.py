import re
from tqdm import tqdm
from collections import Counter


class Statistics():
    def __init__(self):
        pass

    @staticmethod
    def get_bucket(data, bucket_num=10):
        _max, _min = max(data), min(data)
        base = pow(10, max(len(str(_max)) - 1, 1))
        ceil = ((_max - 1) // base + 1) * base
        bucket_range = ceil // bucket_num
        bucket_cnt = [0] * bucket_num
        for d in data:
            bucket_cnt[(d-1)//bucket_range] += 1
        
        print(f"Min length : {_min}, Max length : {_max}")
        for i, cnt in enumerate(bucket_cnt):
            print(f"{i*bucket_range: >4} - {(i+1)*bucket_range: >4} \t {cnt: >9} items.\t{100.0*cnt/len(data):.2f}%")

    @staticmethod
    def stat_data(data):
        post_num = len(data)
        resp_num_list = list(map(len, data))
        resp_num = sum(resp_num_list) - post_num
        print(f"Posts: {post_num}\n" + \
              f"Respones: {resp_num}\n" + \
              f"Resps per Post Avg :{1.0*resp_num/post_num:.2f}")
        print("Resps Per Post Distribute:")
        Statistics.get_bucket(resp_num_list)

        bucket_post, bucket_resp = [], []
        for item in data:
            post_len = len(item[0][0].split(' '))
            resp_len_list = [len(r[0].split(' ')) for r in item[1:]]
            bucket_post.append(post_len)
            bucket_resp.extend(resp_len_list)
        
        print("\nPost Distribute:")
        Statistics.get_bucket(bucket_post)
        print("\nReponse Distribute:")
        Statistics.get_bucket(bucket_resp)
