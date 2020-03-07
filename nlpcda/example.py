#!/usr/bin/python
# -*- coding: utf-8 -*-

from nlpcda.tools.randomword import Randomword
from nlpcda.tools.similarword import Similarword
from nlpcda.tools.homophone import Homophone
from nlpcda.tools.randomdeletechar import RandomDeleteChar


def test_Randomword(test_str, create_num=10, change_rate=0.3):
    '''
    随机【（等价）实体】替换，这里是extdata/company.txt ，随机公司实体替换
    :param test_str: 替换文本
    :param create_num: 增强为多少个
    :param change_rate: 文本变化率/最大多少比例会被改变
    :return:
    '''
    smw = Randomword(create_num=create_num, change_rate=change_rate)
    return smw.replace(test_str)


def test_Similarword(test_str, create_num=10, change_rate=0.3):
    '''
    随机【同义词】替换
    :param test_str: 替换文本
    :param create_num: 增强为多少个
    :param change_rate: 文本变化率/最大多少比例会被改变
    :return:
    '''
    smw = Similarword(create_num=create_num, change_rate=change_rate)
    return smw.replace(test_str)


def test_Homophone(test_str, create_num=10, change_rate=0.3):
    '''
    随机【同意/同音字】替换
    :param test_str: 替换文本
    :param create_num: 增强为多少个
    :param change_rate: 文本变化率/最大多少比例会被改变
    :return:
    '''
    hoe = Homophone(create_num=create_num, change_rate=change_rate)
    return hoe.replace(test_str)


def test_RandomDeleteChar(test_str, create_num=10, change_rate=0.5):
    smw = RandomDeleteChar(create_num=create_num, change_rate=change_rate)
    return smw.replace(test_str)


if __name__ == '__main__':
    ts = '''这个天大药业很不错啊，测试测试。这是一场疫情防控的人民战争、总体战、阻击战，习近平总书记亲自指挥、亲自部署。运筹帷幄 指挥若定始终把人民群众生命安全和身体健康放在第一位'''
    rs1 = test_Randomword(ts)
    rs2 = test_Similarword(ts)
    rs3 = test_Homophone(ts)
    rs4 = test_RandomDeleteChar(ts)
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
