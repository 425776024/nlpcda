#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
from numbers import Integral, Real
from nlpcda.config import company_path

import jieba as t_jieba


class Basetool:
    def __init__(self, base_file: str, create_num: int = 5, change_rate: float = 0.1, seed: int = 1):
        if isinstance(create_num, bool) or not isinstance(create_num, Integral) or create_num < 1:
            raise ValueError('create_num must be a positive integer')
        if (isinstance(change_rate, bool) or not isinstance(change_rate, Real)
                or not math.isfinite(change_rate) or not 0 <= change_rate <= 1):
            raise ValueError('change_rate must be a finite number between 0 and 1')
        self.random = random.Random(seed)
        self.base_file = base_file
        self.create_num = create_num
        self.change_rate = change_rate
        self.jieba = t_jieba.Tokenizer()
        self.set_userdict(company_path)
        self.loop_t = 2
        self.base_file_mapobj = self.load_paser_base_file()

    def set_userdict(self, txt_path: str):
        '''
        设置你自己的用户字典
        :param txt_path:
        :return:
        '''
        with open(txt_path, 'rb') as dictionary:
            self.jieba.load_userdict(dictionary)

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

    def _validate_text(self, text):
        if not isinstance(text, str):
            raise TypeError('text must be a string')
        return text

    def _generate_sentences(self, text, generate_one):
        """Return unique candidates, including the unchanged input, with bounded retries."""
        sentences = [text]
        if not text or self.create_num == 1 or self.change_rate == 0:
            return sentences
        seen = {text}
        # A tiny rate must not result in millions of unsuccessful retries.
        max_attempts = math.ceil(self.create_num * self.loop_t / max(self.change_rate, 0.01))
        for _ in range(max_attempts):
            sentence = generate_one()
            if sentence not in seen:
                sentences.append(sentence)
                seen.add(sentence)
                if len(sentences) >= self.create_num:
                    break
        return sentences

    def replace(self, replace_str):
        return None
