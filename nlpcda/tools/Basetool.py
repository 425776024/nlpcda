#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/5 1:57 PM
# @Author  : xinfa.jiang
# @Site    : 
# @File    : Basetool.py
# @Software: PyCharm

import random
import jieba as jieba
from nlpcda.config import company_path
#!/usr/bin/python
# -*- coding: utf-8 -*-

class Basetool:
    def __init__(self, base_file, create_num=5, change_rate=0.1, seed=1):
        self.random = random
        self.random.seed(seed)
        self.base_file = base_file
        self.create_num = create_num
        self.change_rate = change_rate
        self.base_file_mapobj = self.load_paser_base_file()
        self.jieba = jieba
        self.jieba.load_userdict(company_path)

    def set_userdict(self, txt_path):
        '''
        设置你自己的用户字典
        :param txt_path:
        :return:
        '''
        self.jieba.load_userdict(txt_path)
        self.jieba.add_word()

    def add_word(self, word: str):
        '''
        增加用户字典，更好切词
        :param word:
        :return:
        '''
        self.jieba.add_word(word)

    def add_words(self, word_list: list):
        for w in word_list:
            self.add_word(w)

    def load_paser_base_file(self):
        return None

    def replace(self, replace_str):
        return None
