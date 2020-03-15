# NLP Chinese Data Augmentation 一键中文数据增强工具

使用：`pip install nlpcda`

---

## 介绍

一键中文数据增强工具，支持：
- 随机实体替换
- 近义词
- 近义近音字替换
- 随机字删除（内部细节：数字时间日期片段，内容不会删）
- ~~翻译互转（中文转英、法德日...、再翻译回来），未实现，计划中~~
- `经过细节特殊处理，90%以上置信度，保证不改变原文语义。99%置信度即使改变也能被猜出来、能被猜出来、能被踩出来、能被菜粗来、被菜粗、能菜粗来`

## 计划中的未来内容

- 翻译互转实现的增强（站在翻译巨头肩膀上的增强）
- 优化字典内容、加载与生成速度优化
- ~~引入编辑距离？超过阀值的增强舍去~~
- 开发辅助工具类：
- - 有标签文本的一键增强
  - 开箱即用的全套增强（一次综合上面多个替换类的增强结果）
  - 多线程辅助的批量数据集增强（你就不用费事了，给个数组集合就完事了）

## 意义
- 在不改变原文语义的情况下，生成指定数量的训练语料文本
- 对NLP模型的泛化性能、对抗攻击、干扰波动，有很好的提升作用
- 参考比赛：https://www.biendata.com/competition/2019diac/



作者：Email:425776024@qq.com

---
## API

### 随机(等价)实体替换

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
from nlpcda.tools.randomword import Randomword

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

### 随机同义词替换
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
from nlpcda.tools.similarword import Similarword

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

### 随机近义字替换
参数：
- base_file ：缺省时使用内置【同义同音字表】，你可以设定/自己指定更加丰富的同义同音字表：
    > 是文本文件路径，内容形如（空格隔开）：\
    > de	的	地	得	德	嘚	徳	锝	脦	悳	淂	鍀	惪	恴	棏\
    > 拼音2 字b1 字b2 ... 字bk\
    > ...\
    > 拼音n 字n1 字n2\
- create_num=3 ：返回最多3个增强文本
- change_rate=0.3 ： 文本改变率
- seed ： 随机种子
```python
from nlpcda.tools.homophone import Homophone

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

### 随机字删除
参数：
- create_num=3 ：返回最多3个增强文本
- change_rate=0.3 ： 文本改变率
- seed ： 随机种子
```python
from nlpcda.tools.randomdeletechar import RandomDeleteChar

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

### 添加自定义词典
用于使用之前，增加分词效果
```python
from nlpcda.tools.randomword import Randomword
from nlpcda.tools.similarword import Similarword
from nlpcda.tools.homophone import Homophone
from nlpcda.tools.randomdeletechar import RandomDeleteChar

Randomword.add_word('小明')
Randomword.add_words(['小明','小白','天地良心'])
# Similarword，Homophone，RandomDeleteChar 同上

```