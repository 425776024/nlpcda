#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from nlpcda.config import company_path

import jieba as t_jieba


class Basetool:
    def __init__(self, base_file: str, create_num: int = 5, change_rate: float = 0.1, seed: int = 1):
        self.random = random
        self.random.seed(seed)
        self.base_file = base_file
        self.create_num = create_num
        self.change_rate = change_rate
        self.jieba = t_jieba
        self.set_userdict(company_path)
        self.loop_t = 2
        self.base_file_mapobj = self.load_paser_base_file()

    def set_userdict(self, txt_path: str):
        '''
        设置你自己的用户字典
        :param txt_path:
        :return:
        '''
        self.jieba.load_userdict(txt_path)

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
