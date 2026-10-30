#!/usr/bin/python
# -*- coding: utf-8 -*-

from nlpcda.tools.Basetool import Basetool


class RandomDeleteChar(Basetool):
    """
    随机字删除，【字级别的】，增强数据
    """

    def __init__(
        self, create_num: int = 5, change_rate: float = 0.05, seed: int = 1, stopwords=None
    ):
        super(RandomDeleteChar, self).__init__("", create_num, change_rate, seed, stopwords)

    def replace(self, replace_str: str):
        replace_str = self._validate_text(replace_str)
        seg_list = self.jieba.cut(replace_str, cut_all=False)
        words = list(seg_list)
        sentences = [replace_str]
        if len(words) <= 3:
            return sentences
        protected = self._protected_tokens(replace_str, words)

        def generate_one():
            a_sentence = ""
            for i, word in enumerate(words):
                word_pre = words[i - 1] if i > 0 else ""
                word_back = words[i + 1] if i + 1 < len(words) else ""
                a_sentence += word if protected[i] else self.s1(word_pre, word, word_back)
            return a_sentence

        return self._generate_sentences(replace_str, generate_one)

    def is_int(self, s: str):
        try:
            int(s)
            return True
        except (TypeError, ValueError):
            return False

    def s1(self, word_pre: str, word: str, word_back: str):
        # 词不删
        if len(word) > 1:
            return word
        # 字是数字 不删
        if self.is_int(word):
            return word

        # 字不是数字，但前或者后，存在数字：3月6日，不删 月，删了就是 36 了
        if self.is_int(word_pre) or self.is_int(word_back):
            return word

        # 随机删除这个字
        if self.random.random() < self.change_rate:
            return ""
        else:
            return word


def test(test_str, create_num=10, change_rate=0.5):
    smw = RandomDeleteChar(create_num=create_num, change_rate=change_rate)
    return smw.replace(test_str)


if __name__ == "__main__":
    # 【天大药业】 是个实体，会被换成很多别的同级别实体
    ts = """”3月6日，2010年11月02日。中共中央总书记、国家主席、中央军委主席习近平在京出席决战决胜脱贫攻坚座谈会并发表重要讲话时这样强调"""
    rs = test(ts)
    for s in rs:
        print(s)
