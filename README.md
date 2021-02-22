# Pchatbot: A Large-Scale Dataset for Personalized Chatbot

[Chinese Version](https://github.com/qhjqhj00/Pchatbot/blob/main/README_zh.md)

### Introduction

we introduce Pchatbot, a large scale conversation dataset dedicated for the development of personalized dialogue models. In this dataset, we assign anonymized user IDs and timestamps to conversations. Users’ dialogue histories can be retrieved and used to build rich user profiles. With the availability of the dialogue histories, we can move from personality based models to personalized models.

Pchatbot has two subsets, named PchatbotW and PchatbotL, built from open-domain Weibo and judicial forums respectively.Since the data volume of each sub-data set is too large, we divided each sub-data set into 10 equal parts according to the number of users, and named them PchatbotW-i and PchatbotL-i.
### Dataset Statistics

The detailed data of the data set is shown in the following table:

|                         | PchatbotW     | PchatbotL     | PchatbotW-1 | PchatbotL-1 |
|-------------------------|---------------|---------------|-------------|-------------|
| #Posts                  | 5,319,596     | 20,145,956    | 3,597,407   | 4,662,911   |
| #Responses              | 139,448,339   | 59,427,457    | 13,992,870  | 5,523,160   |
| #Users in posts         | 772,002       | 5,203,345     | 417,294     | 1,107,989   |
| #Users in responses     | 23,408,367    | 203,636       | 2,340,837   | 20,364      |
| Avg.#responses per post | 26.214        | 2.950         | 3.890       | 1.184       |
| Max.#responses per post | 525           | 120           | 136         | 26          |
| #Words                  | 8,512,945,238 | 3,013,617,497 | 855,005,996 | 284,099,064 |
| Avg.#words per pair     | 61.047        | 51.014        | 61.103      | 51.438      |


To obtain statistics, run:

`python statistics.py`

(这个跟zhx确认)

### Data Content and Format

#### Obtain the data 

Please fill in the application form and send it to the contact mail, we will then send download links to you.

[Application Form](https://github.com/qhjqhj00/Pchatbot/blob/main/application.pdf)

#### Pchatbot Files

The upload format of the dataset is .tar.bz2, you can decompress it as follows：
```python
tar -jxvf xx.tar.bz2
```


`PchatbotL.release_ver` 

The format of each piece of data in the data set is：

`Post \t Post_user_id \t Post_timestamp \t Response \t Response_user_id \t Response_timestamp \n`

post and response are sentences with word segmentation, separated by spaces.And we give several examples of the data in data/sample.txt

(写一下格式和文件介绍，给几个sample，目前这两个文件在155服务器：/home/hanxun_zhong/data/PChatbot下)

`PchatbotW.release_ver`



### Data Preprocessing

（跟zhx确定一下处理的代码）



### License

（我们的数据集使用这个license，简单介绍一下）

https://creativecommons.org/licenses/by-nc/2.0/



### FAQ



## Citation

@article{li2020pchatbot,
  title={Pchatbot: A Large-Scale Dataset for Personalized Chatbot},
  author={Li, Xiaohe and Zhong, Hanxun and Guo, Yu and Ma, Yueyuan and Qian, Hongjin and Liu, Zhanliang and Dou, Zhicheng and Wen, Ji-Rong},
  journal={arXiv preprint arXiv:2009.13284},
  year={2020}
}



### 
