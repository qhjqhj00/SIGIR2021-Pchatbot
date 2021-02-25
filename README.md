# Pchatbot: A Large-Scale Dataset for Personalized Chatbot

[Chinese Version](https://github.com/qhjqhj00/Pchatbot/blob/main/README_zh.md)

### Introduction

we introduce Pchatbot, a large scale conversation dataset dedicated for the development of personalized dialogue models. In this dataset, we assign anonymized user IDs and timestamps to conversations. Users’ dialogue histories can be retrieved and used to build rich user profiles. With the availability of the dialogue histories, we can move from personality based models to personalized models.

Pchatbot has two subsets, named PchatbotW and PchatbotL, built from open-domain Weibo and judicial forums respectively.Since the data volume of each sub-data set is too large, we divided each sub-data set into 10 equal parts according to the number of users, and named them PchatbotW-i and PchatbotL-i.
### Dataset Statistics

The detailed statistics of Pchatbot is shown in the following table:

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



We construct two standard dataset from Pchatbot for both generation-based and retrieval-based tasks, named PchatbotW-R and PchatbotW-G. The two datasets can be directly used in coressponding dialogue tasks. Their statistics are shown in the following table:

|                               | PchatbotW-R | PchatbotW-G |
| ----------------------------- | ----------- | ----------- |
| Number of users               | 420,000     | 300,000     |
| Avg. history length           | 32.3        | 11.4        |
| Avg. length of post           | 24.9        | 22.9        |
| Avg. length of response       | 10.1        | 9.6         |
| Number of response candidates | 10          | -           |
| Number of training samples    | 3,000,000   | 2,707,880   |
| Number of validation samples  | 600,000     | 600,000     |
| Number of testing samples     | 600,000     | 600,000     |

To obtain statistics, run:

`python src/statistics.py`

We will then release standard datasets for PchatbotL.

### Data Content and Format

#### Obtain the data 

Please fill in the application form and send it to the contact mail, we will then send download links to you.

[Application Form](https://github.com/qhjqhj00/Pchatbot/blob/main/application.pdf)

#### Pchatbot Files

The upload format of the dataset is .tar.bz2, you can decompress it as follows：
```python
tar -jxvf xx.tar.bz2
```

The format of each piece of data in the data set is：

`Post \t Post_user_id \t Post_timestamp \t Response \t Response_user_id \t Response_timestamp \n`

post and response are sentences with word segmentation, separated by spaces.And we give several examples of the data in data/sample.txt


We also give some examples of user personalized information, as shown in the figure below, due to space constraints, we only selected 5 historical records for the user in each example.
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
      <td style="width:100px;word-break:keep-all">“Post:今日 晚餐 黄焖鸡 ， 红烧 带鱼 和 丝瓜蛋 汤 淘鲜达 送来 的 带鱼 不 好 ， 说 是 中段 ， 实际 是 前段 和 尾巴 ， 没 多少 肉 都 懒得 拍 。 黄焖鸡 太 下饭 啦 ， 和 家属 都 添 了 小 半 碗 米饭 。 下午 做 的 巧克力 冰淇淋 ， 味道 棒棒 哒 
         Response:烦烦 和 光光 就是 永远 都 吃 不 胖 的 神仙 体质” </td>
      <td>"因 為荔 枝樹 不是 每年 都 能 結果 ， 不是 每年 都 能 吃到 ， 但 卻是 每年 夏天 我 最 期待 的 水果 ， 期待 的 童年味 ， 在 河邊 玩耍 ， 在 樹下 等 荔枝 的 夏日 。", "一定 要 有 机会 了 去 南方 看看 荔枝树 的 样子"</td>
      <td>"用 喜欢 的 餐具 穿 舒适 的 衣裙 吃 简单 可口 的 食物 这些 小快乐 足以 点亮 平淡 的 生活 餐具 白裙子 by", "穿 搭博 主好 美 呀"</td>
      <td>"柠檬 冰淇淋 搞定 ！ 还有 强行 出镜 的 柠檬 扇子 广告 ， 这么 尬 为啥 还要 发 呢 ？ 因为 那个 抠门 的 家伙 给 我 的 寄 了 一 箱子 芒果 ， 所谓 拿人 手短 吃 人 嘴软 ， 希望 对方 也 有 这样 的 觉悟", "柠檬 盘子 也 很 好看"</td>
      <td>["天天 和 徐大 美丽 混一 起 。", "这个 蘑菇 看 起来 特别 好吃"</td>
   </tr>
<!--    <tr>
      <td>甜 心 進 行 曲 终于 拿到 珠光粉 小 煎饼 了 呜呜呜 ！ 偏光 真是 太 美惹 ！ 搭配 甜系 小 裙子 简直 完美 ！ 大小 对 我 来说 也 特别 合适 ！ 已经 成为 近期 出门 搭配 的 最 爱 了 ！ ！ ！ bag</td>
      <td>你 穿 这个 好 看死 了 ！</td>
      <td>太 仙 了 呜呜 </td>
      <td>哈哈哈 你 太 甜 了 </td>
      <td>抽 就 抽 ， 不要 放 自拍 ， 俺 受 不住 </td>
      <td>妈呀 你 太 美 了 ！ ！</td>
      <td>呃 啊 太 可爱 了 呜呜 呜 </td>
   </tr> -->
   <tr>
      <td>woj ： 考辛斯 寻求 一 份 年薪 在 1200-1800万 的 合同 。 但是 现在 甚至 没有 球队 愿意 给 他 一 份 中产 合同</td>
      <td>200万 湖人 要 了</td>
      <td>"别 问 我 支持 火箭 还是 勇士 了 我 支持 小卡 凌晨 4点 在 洛杉矶 跑步 、 被 一个 老外 拖进 篮球场 、 教 了 几 个 小时 后 仰跳 投", "我 怀疑 你 在 开车 ， 但是 我 没有 证据"</td>
      <td>"消息 ： 鹈鹕 本来 对 湖人 之前 给 的 筹码 很 心动 ， 但是 现在 莺歌 的 病情 改变 了 一切", "我 谢谢 您 嘞 ， 去去去 快去 换季 后 赛塔图姆 吧" </td>
      <td>"水花 兄弟 这 两 位 ， 场下 真的 暖 ， 场上 关键 时刻 真的 硬 作为 两队 的 中立 球迷 ， 这 场 比赛 给 我 看 的 热血 沸腾 了 ， 火箭 最后 也 一直 坚挺 着 ， 真的 精彩 ， 真的", "勇士 火箭 都 不 喜欢 ， 甚至 有点 讨厌 ， 但是 今天 这 场 比赛 ， 确实 勇士 更 值得 赢"</td>
      <td>"大家 觉得 猛龙 和 雄鹿 谁 最 有 可能 进入 到 总决赛 ？", "范乔丹 ： 看 老子 心情 吧" </td>
      <td>"小卡 会 成为 三连冠 终结者 王朝 毁灭者 吗 ？？", "哈哈 职业 阻止 三 连 冠"</td>
   </tr>
</table>


### Data Preprocessing

Instructions for data cleaning, preprocessing, aggregation and dataset constructs are in `./src/` folder.

### Baseline models

We provide results of baseline models on the PchatbotW-R and PchatbotW-G dataset. For evaluation details, please refer to our [paper](https://arxiv.org/abs/2009.13284). We will continue to update the results of other baseline models:

#### PchatbotW-R

|           | R10@1 | R10@2 | R10@5 | MRR   | nDCG  | Paper                                                        | Code                                 |
| --------- | ----- | ----- | ----- | ----- | ----- | ------------------------------------------------------------ | ------------------------------------ |
| Conv-KNRM | 0.323 | 0.520 | 0.893 | 0.538 | 0.818 | Convolutional Neural Networks for Soft-Matching N-Grams in Ad-hoc Search | https://github.com/yunhenk/Conv-KNRM |
| DAM       | 0.438 | 0.644 | 0.966 | 0.635 | 0.881 | Multi-Turn Response Selection for Chatbots with Deep Attention Matching Network | https://github.com/baidu/Dialogue    |
| IOI       | 0.442 | 0.651 | 0.969 | 0.639 | 0.890 | One Time of Interaction May Not Be Enough: Go Deep with an Interaction-over-Interaction Network for Response Selection in Dialogues | https://github.com/chongyangtao/IOI  |
| RSM-DCK   | 0.428 | 0.627 | 0.947 | 0.623 | 0.858 | Learning to Detect Relevant Contexts and Knowledge for Response Selection in Retrieval-based Dialogue Systems | Provided by the author               |



#### PchatbotW-G

|            | BLEU-1 | ROUGE-L | Dist-1 | Dist-2 | P-F1 | Paper | Code |
| ---------- | ------ | ------- | ------ | ------ | ---- | ----- | ---- |
| Seq2Seq    |        |         |        |        |      |       |      |
| SPEAKER    |        |         |        |        |      |       |      |
| PERSONAWAE |        |         |        |        |      |       |      |
| DialoGPT   |        |         |        |        |      |       |      |



### License

This repository is liciensed under Apache-2.0 License.

The Pchatbot dataset is liciensed under [CC BY-NC 2.0](https://creativecommons.org/licenses/by-nc/2.0/).



### FAQ



## Citation

@article{li2020pchatbot,
  title={Pchatbot: A Large-Scale Dataset for Personalized Chatbot},
  author={Li, Xiaohe and Zhong, Hanxun and Guo, Yu and Ma, Yueyuan and Qian, Hongjin and Liu, Zhanliang and Dou, Zhicheng and Wen, Ji-Rong},
  journal={arXiv preprint arXiv:2009.13284},
  year={2020}
}



### 
