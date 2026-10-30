# NLP Chinese Data Augmentation 一键中文数据增强工具

使用：`pip install nlpcda`

Python >=3.8。已有安装可运行 `python -m pip install --upgrade nlpcda`。

### 2.5.9 基础维护更新

修复随机删除末尾内容丢失、零增强率除零、全局随机状态和分词词典相互影响、
NER 空行解析及单实体词池报错等问题。基础功能不需要 TensorFlow、Keras 或 NumPy；
SimBERT 仅在实例化时加载独立安装的模型依赖。完整说明见 [CHANGELOG.md](CHANGELOG.md)。

规则增强的 `create_num` 表示返回结果的**最多总数，包含原文**，结果去重。
`change_rate` 范围为 `[0, 1]`，设为 `0` 时只返回原文；原文保留换行与首尾空白。
每个实例有独立的随机状态和用户词典。同样的输入、配置和调用顺序可复现结果，
但结果不保证与旧版逐字相同。

开源不易，欢迎 star🌟

pypi:https://pypi.org/project/nlpcda/

---

## 介绍

一键中文数据增强工具，支持：
- [1.随机实体替换](#1随机等价实体替换)
- [2.近义词](#2随机同义词替换)
- [3.近义近音字替换](#3随机近义字替换)
- [4.随机字删除（内部细节：数字时间日期片段，内容不会删）](#4随机字删除)
- [5.NER类 `BIO` 数据增强](#5ner命名实体-数据增强)
- [6.随机置换邻近的字：**研表究明，汉字序顺并不定一影响文字的阅读理解**<<是乱序的](#6随机置换邻近的字)
- [7.中文等价字替换（1	一	壹	①，2	二	贰	②）](#7等价字替换)
- [8.翻译互转实现的增强](#8翻译互转实现的增强)
- [9.使用`simbert`做生成式相似句生成](#9simbert)

`经过细节特殊处理，比如不改变年月日数字，尽量保证不改变原文语义。即使改变也能被猜出来、能被猜出来、能被踩出来、能被菜粗来、被菜粗、能菜粗来`

## WIP
- 基于语音的洗文本过程（类似翻译）。`文本`转`语音`>`语音`识别回`文本`：基于fastspeech2对文本生成语音，基于wav2vec2语音识别文本
> 例子：
> 
> input: 新华社北京消息 > `fastspeech2` > x.wav
> 
> x.wav > `wav2vec2` > output: 新华设北京消息
> 

- 数字转换工具（用于文本转换、中文语音合成需要纯中文）
> 今天是8月29日消息 > 今天是八月二十九日消息
> 
> 我有1234个苹果 > 我有一千二百三十四个苹果

## 意义
- 在不改变原文语义的情况下，生成指定数量的训练语料文本
- 对NLP模型的泛化性能、对抗攻击、干扰波动，有很好的提升作用
- 参考比赛(本人用此策略+base bert拿到：50+-/1000)：https://www.biendata.net/competition/2019diac/
- 基于nlpcda，本人[CCKS 2020：基于标题的大规模商品实体检索](https://www.biendata.net/competition/ccks_2020_6/final-leaderboard/)获得第9名，名字叫`nlpcda`

> ⚠️ 单纯刷准确率分数的比赛，用此包一般不会有分数提升



---
## API

### 1.随机(等价)实体替换

参数：
- base_file ：缺省时使用内置（公司）实体。对公司实体进行替换
    > 是文本文件路径，内容形如：\
    > 实体1\
    > 实体2\
    > ...\
    > 实体n
- create_num=3 ：返回最多3个增强文本
- change_rate=0.3 ： 文本改变率
- seed ： 随机种子

```python
from nlpcda import Randomword

test_str = '''这是个实体：58同城；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，不差；这个nlpcad包，用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击'''

smw = Randomword(create_num=3, change_rate=0.3)
rs1 = smw.replace(test_str)

print('随机实体替换>>>>>>')
for s in rs1:
    print(s)
'''
随机实体替换>>>>>>
这是个实体：58同城；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，不差；这个nlpcad包，用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击
这是个实体：长兴国际；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，不差；这个nlpcad包，用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击
这是个实体：浙江世宝；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，不差；这个nlpcad包，用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击
'''

```

### 2.随机同义词替换
参数：
- base_file ：缺省时使用内置同义词表，你可以设定/自己指定更加丰富的同义词表：
    > 是文本文件路径，内容形如（空格隔开）：\
    > Aa01A0 人类 生人 全人类\
    > id2 同义词b1 同义词b2 ... 同义词bk\
    > ...\
    > idn 同义词n1 同义词n2\
- create_num=3 ：返回最多3个增强文本
- change_rate=0.3 ： 文本改变率
- seed ： 随机种子

```python
from nlpcda import Similarword

test_str = '''这是个实体：58同城；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，不差；这个nlpcad包，用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击'''

smw = Similarword(create_num=3, change_rate=0.3)
rs1 = smw.replace(test_str)

print('随机同义词替换>>>>>>')
for s in rs1:
    print(s)

'''
随机同义词替换>>>>>>
这是个实体：58同城；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，不差；这个nlpcad包，用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击
这是个实体：58同城；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，不差；这个nlpcad包，用于方便一键数量增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击
这是个实体：58同城；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，不差；斯nlpcad包，用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击
'''


```

### 3.随机近义字替换
参数：
- base_file ：缺省时使用内置【同义同音字表】，你可以设定/自己指定更加丰富的同义同音字表：
    > 是文本文件路径，内容形如（\t隔开）：\
    > de	的	地	得	德	嘚	徳	锝	脦	悳	淂	鍀	惪	恴	棏\
    > 拼音2 字b1 字b2 ... 字bk\
    > ...\
    > 拼音n 字n1 字n2\
- create_num=3 ：返回最多3个增强文本
- change_rate=0.3 ： 文本改变率
- seed ： 随机种子
```python
from nlpcda import Homophone

test_str = '''这是个实体：58同城；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，不差；这个nlpcad包，用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击'''

smw = Homophone(create_num=3, change_rate=0.3)
rs1 = smw.replace(test_str)

print('随机近义字替换>>>>>>')
for s in rs1:
    print(s)

'''
随机近义字替换>>>>>>
这是个实体：58同城；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，不差；这个nlpcad包，用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击
这是个实体：58同城；今填是2020年3月8日11:40，天气晴朗，天气很不错，空气痕好，不差；这个nlpcad包，用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击
鷓是个实体：58同乘；今天是2020年3月8日11:40，天迄晴朗，天气很不错，空气很儫，不差；这个nlpcad包，用于方便一键数据增强，犐有效增牆NLP模型的橎化性能、减少波动、抵抗对抗攻击
'''

```

### 4.随机字删除
参数：
- create_num=3 ：返回最多3个增强文本
- change_rate=0.3 ： 文本改变率
- seed ： 随机种子
```python
from nlpcda import RandomDeleteChar

test_str = '''这是个实体：58同城；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，不差；这个nlpcad包，用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击'''

smw = RandomDeleteChar(create_num=3, change_rate=0.3)
rs1 = smw.replace(test_str)

print('随机字删除>>>>>>')
for s in rs1:
    print(s)

'''
随机字删除>>>>>>
这是个实体：58同城；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，不差；这个nlpcad包，用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击
这是个实体：58同城；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气，不差；这个nlpcad包用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗
个实体：58同城；今天是2020年3月8日11:40，天气晴朗，天气很不错空气很好，不差；这个nlpcad包，用于方便一键数据增强，可有效增强NLP模型泛化性能、减少波动、抵抗对抗
'''

```

### 5.NER命名实体 数据增强
输入标注好的NER数据目录，和需要增强的标注文件路径，和增强的数量，即可一键增强

Ner类参数：
- ner_dir_name='ner_data' : 在ner数据放在ner_data目录下（里面很多.txt）
- ner_dir_name提供的目录下是各种标注数据文件，文件内容以标准的NER 的BIO格式分开：
> 字1 \t TAG
>
> 北 \t B-LOC
>
> 京 \t I-LOC
>
> 今 \t O
>
> 天 \t O
>
> 很 \t O
>
> 热 \t O
>
> 。 \t O
- ignore_tag_list=['O'] : 数据里面O标签的不需要管
- data_augument_tag_list=['P', 'LOC'] : 只对P、LOC标签的实体做增强
- augument_size=3 : 每条标注数据，最多新增强数量
- seed=0 : 随机种子/ 可缺省

调用函数augment()参数
- file_name: 1条标注训练文件的路径，如0.txt
- ner.augment(file_name='0.txt')

例子：
```python
from nlpcda import Ner

ner = Ner(ner_dir_name='ner_data',
        ignore_tag_list=['O'],
        data_augument_tag_list=['P', 'LOC','ORG'],
        augument_size=3, seed=0)
data_sentence_arrs, data_label_arrs = ner.augment(file_name='0.txt')
# 3条增强后的句子、标签 数据，len(data_sentence_arrs)==3
# 你可以写文件输出函数，用于写出，作为后续训练等
print(data_sentence_arrs, data_label_arrs)
```

支持用空行分隔多个 BIO 句子；每句最多生成 `augument_size` 条不同于原句的结果，
输出保持句子独立。替换实体长度变化时会重新生成 BIO 标签；没有可替换实体时返回空结果。
实体词池应仅从训练集目录构建，避免引入验证集或测试集的信息。

### 6.随机置换邻近的字
- char_gram=3：某个字只和邻近的3个字交换
- 内部细节：遇到数字，符号等非中文，不会交换
```python
from nlpcda import CharPositionExchange

ts = '''这是个实体：58同城；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，不差；这个nlpcad包，用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击'''
smw = CharPositionExchange(create_num=3, change_rate=0.3,char_gram=3,seed=1)
rs=smw.replace(ts)
for s in rs:
    print(s)

'''
这是个实体：58同城；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，不差；这个nlpcad包，用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击
这实个是体：58城同；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，差不；这个nlpcad包，便用一数方增键强据于，增有效可强NLP模型性泛化的能、动少减波、抵对攻抗抗击
这是个体实：58城同；今是天2020年3月8日11:40，朗气晴天，天气很错不，空好很气，不差；个这nlpcad包，方便键一据增用数于强，可有效强增NLP模型的性化泛能、动减波少、抗抗击抵对攻
'''

```

### 7.等价字替换
参数：
- base_file ：缺省时使用内置【等价数字字表】，你可以设定/自己指定更加丰富的等价字表(或者使用函数：add_equivalent_list)：
    > 是文本文件路径，内容形如（(\t)隔开）：\
    > 0	零	〇\
    > 1	一	壹	①\
    > ...\
    > 9	九	玖	⑨
- create_num=3 ：返回最多3个增强文本
- change_rate=0.3 ： 文本改变率
- seed ： 随机种子
```python
from nlpcda import EquivalentChar

test_str = '''今天是2020年3月8日11:40，天气晴朗，天气很不错。'''

s = EquivalentChar(create_num=3, change_rate=0.3)
# 添加等价字
s.add_equivalent_list(['看', '瞅'])
res=s.replace(test_str)
print('等价字替换>>>>>>')
for s in res:
    print(s)

'''
等价字替换>>>>>>
今天是2020年3月8日11:40，天气晴朗，天气很不错。
今天是二〇2〇年3月八日1①:4〇，天气晴朗，天气很不错。
今天是二0贰零年3月捌日11:40，天气晴朗，天气很不错
'''

```

### 添加自定义词典
用于使用之前，增加分词效果
```python
from nlpcda import Randomword
from nlpcda import Similarword
from nlpcda import Homophone
from nlpcda import RandomDeleteChar
from nlpcda import Ner
from nlpcda import CharPositionExchange

augmenter = Randomword()
augmenter.add_word('小明')
augmenter.add_words(['小明','小白','天地良心'])
# Similarword，Homophone，RandomDeleteChar 同上

```


### 8.翻译互转实现的增强
1.百度中英翻译互转实现的增强
note:

> 申请你的 appid、secretKey: http://api.fanyi.baidu.com/api/trans
>
```python
from nlpcda import baidu_translate

zh = '天气晴朗，天气很不错，空气很好'
# 申请你的 appid、secretKey
# 两遍洗数据法（回来的中文一般和原来不一样，要是一样，就不要了，靠运气？）
en_s = baidu_translate(content=zh, appid='xxx', secretKey='xxx',t_from='zh', t_to='en')
zh_s = baidu_translate(content=en_s, appid='xxx', secretKey='xxx',t_from='en', t_to='zh')
print(zh_s)

```

2.谷歌翻译互转实现的增强

pip 包：[py-googletrans](https://py-googletrans.readthedocs.io/en/latest/)

免费的谷歌翻译API，需要翻墙且不稳定

[https://py-googletrans.readthedocs.io/en/latest](https://py-googletrans.readthedocs.io/en/latest)

pip install googletrans
```python
from googletrans import Translator
def googletrans(content='一个免费的谷歌翻译API', t_from='zh-cn', t_to='en'):
    translator = Translator()
    s = translator.translate(text=content, dest=t_to,src=t_from)
    return s.text

```



### 9.simbert
[来源：https://github.com/ZhuiyiTechnology/pretrained-models](https://github.com/ZhuiyiTechnology/pretrained-models)

[参考：https://github.com/ZhuiyiTechnology/simbert](https://github.com/ZhuiyiTechnology/simbert)

下载其中任意模型，解压到任意位置赋值给`model_path`变量：

| 名称           | 训练数据大小 | 词表大小 | 模型大小 | 下载地址 |
| :----------:  |:---------:| :------: | :------: | :------: |
| SimBERT Tiny  | 2200万相似句组  | 13685   | 26MB   | [百度网盘](https://pan.baidu.com/s/1z_agqTuBTuyHANwrS-gPcg)(1tp7) |
| SimBERT Small |  2200万相似句组 | 13685  | 49MB  | [百度网盘](https://pan.baidu.com/s/1kq_EQDI0gpiZBLFd_AxwrA)(nu67) |
| SimBERT Base  |  2200万相似句组 | 13685  | 344MB | [百度网盘](https://pan.baidu.com/s/1uGfQmX1Kxcv_cXTVsvxTsQ)(6xhq) |

参数：
- config：model_path（上述下载的模型位置），设备（cpu/cuda...）、最大长度、随机种子
- sent：需要增强的句子
- create_num：构造的句子数量

环境参考（手动安装）：

以下为历史环境记录，不表示已通过当前 Python/TensorFlow 版本的模型推理验证。
规则增强无需安装这些模型依赖。`CUDA_VISIBLE_DEVICES` 可省略，省略时保留现有设备配置；
`model_path` 必须指向已下载的本地模型目录。
```

keras==2.3.1
bert4keras==0.7.7
# tensorflow==1.13.1
tensorflow-gpu==1.13.1

```
```python
from nlpcda import Simbert
config = {
        'model_path': '/xxxx/chinese_simbert_L-12_H-768_A-12',
        'CUDA_VISIBLE_DEVICES': '0,1',
        'max_len': 32,
        'seed': 1
}
simbert = Simbert(config=config)
sent = '把我的一个亿存银行安全吗'
synonyms = simbert.replace(sent=sent, create_num=5)
print(synonyms)
'''
[('我的一个亿，存银行，安全吗', 0.9871675372123718), 
('把一个亿存到银行里安全吗', 0.9352194666862488), 
('一个亿存银行安全吗', 0.9330801367759705), 
('一个亿的存款存银行安全吗', 0.92387855052948),
 ('我的一千万存到银行安不安全', 0.9014463424682617)]
'''


```

## 开发与发布验证

```bash
python -m pip install . build twine
python -m unittest discover -s tests -v
python -m build
python -m twine check dist/*
```

CI 在 Linux 的 Python 3.8–3.14，以及 Windows/macOS 的 Python 3.12 上检查
安装后的包。SimBERT 模型推理与百度翻译在线请求需要另行准备模型或服务凭据，
不属于离线回归测试的覆盖范围。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=425776024/nlpcda&type=Date)](https://www.star-history.com/#425776024/nlpcda&Date)



