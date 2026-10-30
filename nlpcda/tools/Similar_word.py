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
        with open(self.base_file, "r", encoding='utf-8') as source:
            for line in source:
                seperate_word = line.split()
                # Cilin marks related/independent words with #/@. Custom IDs are allowed.
                if not seperate_word or seperate_word[0].endswith(('#', '@')):
                    continue
                for wi in seperate_word[1:]:
                    if len(wi) > 1:
                        self.add_word(wi)
                    combine_dict[wi] = [word for word in seperate_word[1:] if word != wi]
        return combine_dict

    def replace(self, replace_str:str):
        replace_str = self._validate_text(replace_str)
        seg_list = self.jieba.cut(replace_str, cut_all=False)
        words = list(seg_list)
        return self._generate_sentences(replace_str, lambda: ''.join(self.s1(word) for word in words))

    def s1(self, word:str):
        # 替换所有在combine_dict中的
        if len(word) == 1: return word
        if self.base_file_mapobj.get(word) and self.random.random() < self.change_rate:
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
