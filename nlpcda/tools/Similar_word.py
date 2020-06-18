#!/usr/bin/python
# -*- coding: utf-8 -*-

from nlpcda.tools.Basetool import Basetool
from nlpcda.config import similarword_path


class Similarword(Basetool):
    '''
    近义词，用于大致不改变原文下，【词级别的】，增强数据
    '''

    def __init__(self, base_file=similarword_path, create_num=5, change_rate=0.05, seed=1):
        super(Similarword, self).__init__(base_file, create_num, change_rate, seed)


    def load_paser_base_file(self):
        combine_dict = {}
        for line in open(self.base_file, "r", encoding='utf-8'):
            seperate_word = line.strip().split(" ")
            num = len(seperate_word)
            for i in range(1, num):
                wi = seperate_word[i]
                # add to user dict
                if len(wi) > 1: self.add_word(wi)
                combine_dict[wi] = seperate_word[1:]
        print('load :%s done' % (self.base_file))
        return combine_dict

    def replace(self, replace_str:str):
        replace_str = replace_str.replace('\n', '').strip()
        seg_list = self.jieba.cut(replace_str, cut_all=False)
        words = list(seg_list)
        sentences = [replace_str]
        t = 0
        while len(sentences) < self.create_num:
            t += 1
            a_sentence = ''
            for word in words:
                a_sentence += self.s1(word)

            if a_sentence not in sentences:
                sentences.append(a_sentence)
            if t > self.create_num * self.loop_t / self.change_rate:
                break
        return sentences

    def s1(self, word:str):
        # 替换所有在combine_dict中的
        if len(word) == 1: return word
        if word in self.base_file_mapobj and self.random.random() < self.change_rate:
            wi = self.random.randint(0, len(self.base_file_mapobj[word]) - 1)
            place = self.base_file_mapobj[word][wi]
            return place
        else:
            return word


def test(test_str, create_num=10, change_rate=0.3):
    smw = Similarword(create_num=create_num, change_rate=change_rate)
    try:
        return smw.replace(test_str)
    except:
        print('error in Similarword.replace')
        return [test_str]


if __name__ == '__main__':
    ts = '''这个天大药业很不错啊，测试测试。这是一场疫情防控的人民战争、总体战、阻击战，习近平总书记亲自指挥、亲自部署。运筹帷幄 指挥若定始终把人民群众生命安全和身体健康放在第一位'''
    rs = test(ts)
    for s in rs:
        print(s)
