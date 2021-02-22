import regex as re
import json
import random
import string
import logging

import emoji
from langdetect import detect
from langdetect import detect_langs
from langdetect import DetectorFactory

DetectorFactory.seed = 0
DELETE_TEXT = "<DELETE_TEXT>"
TIME_LIMIT = 10


default_regex = [
    ["super_tag", r'\[超话\]', lambda _1: DELETE_TEXT],
    ["dangerous_str", r'^b\'.+\'$', lambda _1: DELETE_TEXT],
    ["「」『』【】〖〗",r'(「.*?」|『.*?』|【.*?】|〖.*?〗){3,}', lambda _1: DELETE_TEXT],
    ["advertise", r'(复|複)(製|制).*淘', lambda _1: DELETE_TEXT],
    ["url", r'[a-zA-z]+://[^\s]*', None],
    ["repost",r'/ ?/? ?@ ?(?:[\w_\-] ?){,30}? ?:.+', None],
    ["comment", r'回复@.*?:', None],
    ["weibo_mention", r'(@+)\S+', None],
    ["weibo_emoji", r'\[ ?(?:. ?){1,10} ?\]', None],
    ["emoji",r':.*?:', None],
    ["black", r'\s{2,}', None],
    ["tag",r'#.*?#', None],
    ['specific',r'转发微博|图片评论', None],
    ['location',r'[\?\?\?]+', None],
    ['200b',u'\u200b|\ufeff', None],
    ["duplicate", r'(?P<remain>(?P<item>\S|(\S.*\S))(?:\s*(?P=item)){1})(?:\s*(?P=item)){2,}', lambda match_obj: match_obj.group('remain')]
]

filter_config = {
    "min_len": 5,
    "max_len": 200,
    "max_text_freq": 1000,
    "max_reread_patience": 3,
    "stopword_file_path": "",
    "log_file_path": "",
    "balance_factor": 2
}

def kaomoji_regex_generator(emoticon_path='assets/emoticon.json'):
    with open(emoticon_path, 'r', encoding = 'utf-8') as emoticon_file:
        emoticons = sorted(json.load(emoticon_file),key = lambda x:len(x),reverse = True)
    all_word_pattern = re.compile(r'^\w+$')
    emoticon_regexs = [ '(?:' + (r'(?:\A| )' + k + r'(?:\Z| )' if all_word_pattern.match(k) else r'\s*'.join([re.escape(ch) for ch in k])) + ')' for k in emoticons]
    regex = '|'.join(emoticon_regexs)
    return ["kaomoji", regex, None]

def crazy_fans_regex_generator(stars_path='assets/stars.json'):
    with open(stars_path, 'r', encoding = 'utf-8') as f:
        stars = json.load(f)
    regex = "(.*(" + '|'.join(stars) + ")+.*){3,}"
    return ["crazy_fans", regex, lambda _1: DELETE_TEXT]


class Filter():
    def __init__(self, config=None, regex_list=None, logging_fp=None):
        if not regex_list:
            regex_list = default_regex
            regex_list.append(kaomoji_regex_generator())
            regex_list.insert(5, crazy_fans_regex_generator())

        self.regex_list = []
        for name, pattern, func in regex_list:
            pattern = re.compile(pattern)
            self.regex_list.append([name, pattern, func])
        
        if not config:
            config = filter_config
        self.min_len = config['min_len']
        self.max_len = config['max_len']
        self.max_text_freq = config['max_text_freq']
        self.max_reread_patience = config['max_reread_patience']
        self.balance_factor = config['balance_factor']
        self.config = config

        if not logging_fp: logging_fp = 'logging/filter.log'
        log_formatter = logging.Formatter('%(message)s')
        log_handler = logging.FileHandler(logging_fp, mode='w')
        log_handler.setFormatter(log_formatter)
        logger = logging.getLogger('filter')
        logger.addHandler(log_handler)
        logger.setLevel(level=logging.INFO)
        self.logger = logger

    def clean_pattern_in_sentence(self, sentence, pattern, task_name=None, replace=None):
        s = sentence
        find_count = 1
        if task_name == 'emoji':
            s = emoji.demojize(s)
        while find_count:
            find_count = 0
            try:
                obj = pattern.finditer(s, timeout=5)
            except TimeoutError:
                self.logger.info(f'regex_unit\ttime_out\t{sentence}')
                return ""
            for match in reversed(list((obj))):
                find_count += 1
                start, end = match.span()
                if replace:
                    item = replace(match)
                    if item == DELETE_TEXT: return ""
                    s = s[:start] + (' ' if start > 0 and s[start - 1] not in string.whitespace else '') + item + (' ' if end < len(s) and s[end] not in string.whitespace else '') + s[end:]
                else:
                    s = s[:start] + (' ' if start > 0 and end < len(s) and s[start - 1] not in string.whitespace and s[end] not in string.whitespace else '') + s[end:]
        return s
       
    def regex_unit(self, text):
        for task_name, pattern, replace_func in self.regex_list:
            old = text
            text = self.clean_pattern_in_sentence(text, pattern, task_name, replace_func)
            if old != text: 
                self.logger.info(f'regex_unit\t{task_name}\t{old}\t{text}')
        return text

    def clip_length_unit(self, text):
        if self.min_len <= len(self.pure_chinese_text(text)) and len(text) <= self.max_len:
            return text
        return ""

    def balance_length_unit(self, text1, text2):
        t1 = self.pure_chinese_text(text1)
        t2 = self.pure_chinese_text(text2)
        if len(t1) * self.balance_factor < len(t2):
            self.logger.info(f'balance_length_unit\t{text1}\t{text2}')
            return ""
        return text2

    def language_unit(self,text,lan_model=False,min_freq=0.3):
        if lan_model:
            chinese_freq = 1.0
            try:
                lan = detect(text)  
            except:
                lan = 'unk'
        else:
            lan = 'freq'
            chinese_num = 0
            for c in list(text):
                if self.is_chinese(c):
                    chinese_num += 1
            chinese_freq = 1.0 * chinese_num / (len(text) + 1)
        if (lan != 'zh-cn' and lan != 'ko' and lan != 'unk' and lan != 'freq') or (chinese_freq < min_freq):
            if text: self.logger.info(f'language_unit: \t{chinese_freq}\t{text}')
            return ""
        return text

    def clip_text_freq_unit(self, text, text2freq):
        pure = self.pure_chinese_text(text)
        freq = text2freq.get(pure, 0)
        if freq <= self.max_text_freq:
            return text
        roll = random.random()
        if roll < 1.0*self.max_text_freq / (freq + 0.00001):
            return text
        self.logger.info(f'clip_text_freq_unit\t{text}')
        return ""

    def reread_machine_unit(self, text, text2freq):
        pure = self.pure_chinese_text(text)
        if text2freq.get(pure, 0) >= self.max_reread_patience:
            self.logger.info(f'reread_machine_unit\t{text}')
            return ""
        return text

    def single_text_pipe(self, text):
        text = re.sub(r'\s+', ' ', text).strip()
        if text: text = self.regex_unit(text)
        if text: text = self.clip_length_unit(text)
        if text: text = self.language_unit(text)
        return text

    def text2frequency(self, data, threshold):
        freq = {}
        for text in data:
            if not text: continue
            pure = self.pure_chinese_text(text)
            freq[pure] = freq.get(pure, 0) + 1
        safe_text = set([text for text, cnt in freq.items() if cnt <= threshold])
        for k in safe_text: del freq[k]
        return freq

    @staticmethod
    def pure_chinese_text(text):
        return re.sub(r'\W', '', text).replace('_', '')

    @staticmethod
    def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
        else:
            return False
