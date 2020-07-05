#!/usr/bin/python
# -*- coding: utf-8 -*-

from nlpcda import Randomword
from nlpcda import Similarword
from nlpcda import Homophone
from nlpcda import RandomDeleteChar
from nlpcda import Ner
from nlpcda import CharPositionExchange
from nlpcda import baidu_translate
from nlpcda import EquivalentChar


def test_Randomword(test_str, create_num=3, change_rate=0.1):
    '''
    随机【（等价）实体】替换，这里是extdata/company.txt ，随机公司实体替换
    :param test_str: 替换文本
    :param create_num: 增强为多少个
    :param change_rate: 文本变化率/最大多少比例会被改变
    :return:
    '''
    smw = Randomword(create_num=create_num, change_rate=change_rate)
    return smw.replace(test_str)


def test_Similarword(test_str, create_num=3, change_rate=0.1):
    '''
    随机【同义词】替换
    :param test_str: 替换文本
    :param create_num: 增强为多少个
    :param change_rate: 文本变化率/最大多少比例会被改变
    :return:
    '''
    smw = Similarword(create_num=create_num, change_rate=change_rate)
    return smw.replace(test_str)


def test_Homophone(test_str, create_num=3, change_rate=0.1):
    '''
    随机【同意/同音字】替换
    :param test_str: 替换文本
    :param create_num: 增强为多少个
    :param change_rate: 文本变化率/最大多少比例会被改变
    :return:
    '''
    hoe = Homophone(create_num=create_num, change_rate=change_rate)
    return hoe.replace(test_str)


def test_RandomDeleteChar(test_str, create_num=3, change_rate=0.1):
    smw = RandomDeleteChar(create_num=create_num, change_rate=change_rate)
    return smw.replace(test_str)


def test_ner():
    ner = Ner(ner_dir_name='../write',
              ignore_tag_list=['O', 'T'],
              data_augument_tag_list=['Cause', 'Effect'],
              augument_size=3, seed=0)
    data_sentence_arrs, data_label_arrs = ner.augment('../write/1.txt')
    print(data_sentence_arrs, data_label_arrs)


def test_CharPositionExchange(test_str, create_num=10, change_rate=0.5):
    smw = CharPositionExchange(create_num=create_num, change_rate=change_rate)
    return smw.replace(test_str)


def test_baidu_translate():
    a = 'Free translation for each platform'
    s = baidu_translate(a, appid='xxx', secretKey='xxx')
    print(s)


def test_EquivalentChar(test_str, create_num=10, change_rate=0.5):
    s = EquivalentChar(create_num=create_num, change_rate=change_rate)
    return s.replace(test_str)


def test():
    ts = '''这是个实体：58同城；今天是2020年3月8日11:40，天气晴朗，天气很不错，空气很好，不差；这个nlpcad包，用于方便一键数据增强，可有效增强NLP模型的泛化性能、减少波动、抵抗对抗攻击'''
    rs1 = test_Randomword(ts)
    rs2 = test_Similarword(ts)
    rs3 = test_Homophone(ts)
    rs4 = test_RandomDeleteChar(ts)
    rs5 = test_EquivalentChar(ts)
    print('随机实体替换>>>>>>')
    for s in rs1:
        print(s)
    print('随机近义词替换>>>>>>')
    for s in rs2:
        print(s)
    print('随机近义字替换>>>>>>')
    for s in rs3:
        print(s)

    print('随机字删除>>>>>>')
    for s in rs4:
        print(s)
    print('等价字替换>>>>>>')
    for s in rs5:
        print(s)


if __name__ == '__main__':
    ts = '''今天是2020年3月8日11:40，天气晴朗，天气很不错。'''
    rs = EquivalentChar(create_num=3, change_rate=0.5)
    res = rs.replace(ts)
    print('等价字替换>>>>>>')
    for s in res:
        print(s)
