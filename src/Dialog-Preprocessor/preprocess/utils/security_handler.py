import json
import string
import re
import time
import signal
import requests

default_regex = [
    ["QQ_pattern", r'(?:[Qq][Qq][:：]{0,1}\t*\d{6,10})', None],
	["number_pattern",r'(?:[〇一二三四五六七八九\d]\t*){9,}',None],
    ["email_pattern", r'\w+@(?:\w+\.)+(?:com|cn|net|edu)', None],
    ["phone_pattern", r'(?:\(?0\d{2,3}[)-]*\d{7,8})|(?:1[3-9]\d{9})', None],
#    ["url_pattern", r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", None],
    ["urll_pattern", r"(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F])){3,100}\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F])){7,100}", None],
#    ["unique", r"(?:\(\"ck\d{7}\"\)[;；]{0,1})|(?:石家庄刘素波律师：免费咨询、代写法律文书、代理诉讼，电话：13673133931   邮箱：liusubo12@sohu.com 博客：lvshizhijia.blog.sohu.com 工作QQ:503981806)|(?:hideifblank)", None]
]

filter_config = {
    "min_len": 5,
    "max_len": 256,
    "log_file_path": "",
    "regex_path": ""
}

default_entity={
	"人名":None
}

class security_handler():
	def __init__(self,config=filter_config):
		regex_list=[]
		if not config['regex_path']:
			regex_list=default_regex
		else :
			regex_list.extend(self.regex_generator(config['regex_path']))
		self.regex_list=regex_list
		self.min_len = config['min_len']
		self.max_len = config['max_len']
		self.config=config
		self.log_file_path=config['log_file_path']
		self.count={}
		self.entity={}

	def parse_line(self,line):
		# try:
		# 	post, rsps = line.split('\t')
		# except Exception as e:
		# 	return None

		url='http://183.174.228.47:8282/RUCNLP/ner?doc=%s&type=weibo'
		#post_entity, rsps_entity = "", ""
		line_entity=""
		try:
			r = requests.get(url % line)
			line_entity = json.dumps(r.json(), ensure_ascii=False)
		except:
			pass

		# try:
		# 	r = requests.get(url % rsps)
		# 	rsps_entity = json.dumps(r.json(), ensure_ascii=False)
		# except:
		# 	pass

		#return "%s\t%s\t%s\t%s" % (post, post_entity, rsps, rsps_entity)
		return "%s\t%s"%(line,line_entity)

	def clean_entity(self,sentence):
		data=self.parse_line(sentence)
		try:
			item=data.split('\t')
			sentence=item[0]
			if(sentence=='the content is empty!'):
				return ""
			sentence_entity=eval(item[1])
			for one_entity in sentence_entity:
				sentence_entity_list=[]
				if(one_entity['type'] in default_entity):
					sentence_entity_list.append(one_entity['entity'])
					self.entity[one_entity['type']] = self.entity[one_entity['type']] + 1 if one_entity['type'] in self.entity else 1
					sentence=self.delete(sentence,sentence_entity_list,default_entity[one_entity['type']])

			return sentence
		except Exception as e:
			return "clean entity failed"

	def regex_generator(path):
		with open(path,'r',encoding='utf-8') as f:
			regex_list=json.load(f)
		return regex_list


	def count_regex(self,old,sentence,task_name,_print=False):
		self.count[task_name] = self.count[task_name] + 1 if task_name in self.count else 1
		if _print:
			print('task : %s'%(task_name))
			print('Old: %s'%(old))
			print('New: %s'%(sentence))

	def count_entity(self,old,sentence,_print=False):
		if _print:
			print('----handle entity----')
			print('Old: %s'%(old))
			print('New: %s'%(sentence))


	def delete(self,sentence,entities,replace=None):
		if(replace==None):
			replace=""
		for entity in entities:
			sentence=sentence.replace(entity,replace)
		return sentence

	def clean_pattern(self,sentence,pattern,task_name=None,replace=None):
		pattern_list=re.findall(pattern,sentence)
		sentence=self.delete(sentence,pattern_list,replace=replace)
		return sentence

	def handler(self,signum,frame):
		raise AssertionError

	def clean_pattern_in_sentence(self,sentence,pattern,task_name=None,replace=None):
		signal.signal(signal.SIGALRM,self.handler)
		signal.alarm(2)
		sentence=self.clean_pattern(sentence,pattern,task_name,replace)
		signal.alarm(0)
		return sentence


	def entity_unit(self,text):
		try:
			old = text
			text = self.clean_entity(text)
			if old != text:
				self.count_entity(old,text,_print=False)
		except Exception as e:
			print("failed to change entity" )
		return text

	def regex_unit(self, text):
		for task_name, pattern, replace_func in self.regex_list:
			try:
				old = text
				text = self.clean_pattern_in_sentence(text, pattern, task_name, replace_func)
				if old != text:
					self.count_regex(old,text,task_name,_print=False)
			except Exception as e:
				print("failed to change \""+text+"\" "+"in pattern "+task_name )
				continue
		return text

	def length_unit(self, text):
		if self.min_len <= len(text) <= self.max_len:
			return text
		return ""



if __name__=="__main__":
	handler=security_handler()
	for i in range(10):
		text=input()
		text=handler.length_unit(text)
		text=handler.entity_unit(text)
		text=handler.regex_unit(text)
		print(text)
