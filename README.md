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
<table>
   <tr>
      <td>Post</td>
      <td>Response</td>
      <td>history1</td>
      <td>history2</td>
      <td>history3</td>
      <td>history4</td>
      <td>history5</td>
   </tr>
   <tr>
      <td>酒酿 小 圆子 窝蛋 ， 蒸 南瓜 玉米 和 阳光 玫瑰 山寨 一 把 芳婆 的 酒酿 圆子 ， 挺 好吃 的 ， 加 了 点干 桂花 增香</td>
      <td>干 桂花 是 点睛</td>
      <td>这个 蘑菇 看 起来 特别 好吃 </td>
      <td>太 可爱 的 每日 小食 了 ， 非常 非常 喜欢</td>
      <td>烦烦 和 光光 就是 永远 都 吃 不 胖 的 神仙 体质</td>
      <td>失踪 人口 回归 了 ， 做饭 阿姨 找好 了 吗</td>
      <td>穿 搭博 主好 美 呀 </td>
   </tr>
   <tr>
      <td>甜 心 進 行 曲 终于 拿到 珠光粉 小 煎饼 了 呜呜呜 ！ 偏光 真是 太 美惹 ！ 搭配 甜系 小 裙子 简直 完美 ！ 大小 对 我 来说 也 特别 合适 ！ 已经 成为 近期 出门 搭配 的 最 爱 了 ！ ！ ！ bag</td>
      <td>你 穿 这个 好 看死 了 ！</td>
      <td>太 仙 了 呜呜 </td>
      <td>哈哈哈 你 太 甜 了 </td>
      <td>抽 就 抽 ， 不要 放 自拍 ， 俺 受 不住 </td>
      <td>妈呀 你 太 美 了 ！ ！</td>
      <td>呃 啊 太 可爱 了 呜呜 呜 </td>
   </tr>
   <tr>
      <td>woj ： 考辛斯 寻求 一 份 年薪 在 1200-1800万 的 合同 。 但是 现在 甚至 没有 球队 愿意 给 他 一 份 中产 合同</td>
      <td>200万 湖人 要 了</td>
      <td>我 怀疑 你 在 开车 ， 但是 我 没有 证据</td>
      <td>我 谢谢 您 嘞 ， 去去去 快去 换季 后 赛塔图姆 吧 </td>
      <td>六 年 没 进季 后赛 了 我们 说 啥 了 ？ 输球 是 抗议 活动 的 导火索 ？？？ 你 要是 好好 整 能 让 人 看见 希望 谁 抗议 啊 ？？？ 还 不是 因为 你 洛杉矶 朴槿惠 闺蜜 干政 ？？？</td>
      <td>勇士 火箭 都 不 喜欢 ， 甚至 有点 讨厌 ， 但是 今天 这 场 比赛 ， 确实 勇士 更 值得 赢 </td>
      <td>范乔丹 ： 看 老子 心情 吧</td>
   </tr>
</table>


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
