import re
from tqdm import tqdm
def load(fp):
    data = []
    with open(fp, 'r') as f:
        for line in tqdm(f):
            line = line.rstrip()
            subs = line.split('\t')
            if len(subs) <= 1:
                continue
            data.append(subs)
    return data
regex_list = [r'\[ ?(?:. ?)+ ?\]',
     r'#.*?#',
     r'\{?(?:. ?)+ ?\}',
     r'「.*?」',
     r'【.*?】',
     r'<.*?>',
     r'《.*?》',
     # r'\u0022.*?\u0022',
     r'\"([^\"]*)\"',
     r'\( ?(?:. ?)+ ?\)',
     r'‘.*?’',
     r'“.*?”',
     r'（.*?）',
     r'『.*?』'

]
data = load('weibo_corpus_dev')
regex = regex_list[12]
print(regex)
f = open('Specific/specific_content_『』.txt','w')
for line in tqdm(data):
    for s in line:
        ret = re.match(regex,s)
        if ret:
            print(s)
            f.write(ret.group())
            f.write('\n')