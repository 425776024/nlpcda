# NLP Chinese Data Augmentation 一键中文数据增强工具

使用：`pip install nlpcda`

开源不易，欢迎 star🌟

pypi:https://pypi.org/project/nlpcda/

---

## 介绍

一键中文数据增强工具，支持：
- 1.随机实体替换
- 2.近义词
- 3.近义近音字替换
- 4.随机字删除（内部细节：数字时间日期片段，内容不会删）
- 5.`新增`：NER类 `BIO` 数据增强
- 6.`新增` 随机置换邻近的字：**研表究明，汉字序顺并不定一影响文字的阅读理解**<<是乱序的
- 7.`新增`百度中英翻译互转实现的增强
- 8.`新增`中文等价字替换（1	一	壹	①，2	二	贰	②）

`经过细节特殊处理，尽量保证不改变原文语义。即使改变也能被猜出来、能被猜出来、能被踩出来、能被菜粗来、被菜粗、能菜粗来`

## 计划中的未来内容
- [使用 WordNet数据库 来做同义词替换](http://openkg.cn/dataset/chinese-wordnet)
- 随机噪声注入？随机插入一些字符，太简单实现了。
- 遗传算法中的交叉突变思想？随机突然改变极小部分字，多个同类型文本中的短句片段（，。！：……分割），相互交换。
- 利用pingyin？[https://github.com/mozillazg/python-pinyin](https://github.com/mozillazg/python-pinyin) 
- 基于HMM/CRF的数据增强？
- 基于LaserTagger的文本复述，输入A，用句子B去复述它，B尽量和A语义一致。[实现了lasertagger-chinese](https://github.com/425776024/lasertagger-chinese)
- 基于Word2Vec、BERT等词向量的词语近距离的替换、MASK猜测置换 ？？但是无法控制它生成，以及缺点MASK位置。
- 引入TF-IDF、TextRank、关键词字典等，可以选择：替换/不替换关键词 ？？
- 还有什么？？

## 意义
- 在不改变原文语义的情况下，生成指定数量的训练语料文本
- 对NLP模型的泛化性能、对抗攻击、干扰波动，有很好的提升作用
- 参考比赛(本人用此策略+base bert拿到：50+-/1000)：https://www.biendata.com/competition/2019diac/



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
        augument_size=3, seed=0),
data_sentence_arrs, data_label_arrs = ner.augment(file_name='0.txt')
# 3条增强后的句子、标签 数据，len(data_sentence_arrs)==3
# 你可以写文件输出函数，用于写出，作为后续训练等
print(data_sentence_arrs, data_label_arrs)
```

### 6.随机置换邻近的字
- char_gram=3：某个字至于邻近的3个字交换
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

### 7.百度中英翻译互转实现的增强
note:

> 申请你的 appid、secretKey: http://api.fanyi.baidu.com/api/trans
>
```python
from nlpcda import baidu_translate

a = 'Free translation for each platform'
# 申请你的 appid、secretKey
s = baidu_translate(content=a, appid='xxx', secretKey='xxx')
print(s)

```

### 8.等价字替换
参数：
- base_file ：缺省时使用内置【等价数字字表】，你可以设定/自己指定更加丰富的等价字表：
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

Randomword.add_word('小明')
Randomword.add_words(['小明','小白','天地良心'])
# Similarword，Homophone，RandomDeleteChar 同上

```