#!/usr/bin/python
# -*- coding: utf-8 -*-

from nlpcda.tools.Basetool import Basetool


class RandomDeleteChar(Basetool):
    '''
    随机字删除，【字级别的】，增强数据
    '''

    def __init__(self, create_num: int = 5, change_rate: float = 0.05, seed: int = 1):
        super(RandomDeleteChar, self).__init__('', create_num, change_rate, seed)

    def replace(self, replace_str: str):
        replace_str = replace_str.replace('\n', '').strip()
        seg_list = self.jieba.cut(replace_str, cut_all=False)
        words = list(seg_list)
        sentences = [replace_str]
        if len(words) <= 3:
            return sentences
        t = 0

        while len(sentences) < self.create_num:
            t += 1
            a_sentence = ''
            for i, word in enumerate(words[:-1]):
                word_back = words[i + 1]
                if i == 0:
                    a_sentence += self.s1('', word, word_back)
                else:
                    word_pre = words[i - 1]
                    a_sentence += self.s1(word_pre, word, word_back)

            if a_sentence not in sentences:
                sentences.append(a_sentence)
            if t > self.create_num * self.loop_t / self.change_rate:
                break
        return sentences

    def is_int(self, s: str):
        try:
            is_int = int(s)
            return True
        except:
            return False

    def s1(self, word_pre: str, word: str, word_back: str):
        # 词不删
        if len(word) > 1: return word
        # 字是数字 不删
        if self.is_int(word):
            return word

        # 字不是数字，但前或者后，存在数字：3月6日，不删 月，删了就是 36 了
        if self.is_int(word_pre) or self.is_int(word_back):
            return word

        # 随机删除这个字
        if self.random.random() < self.change_rate:
            return ''
        else:
            return word


def test(test_str, create_num=10, change_rate=0.5):
    smw = RandomDeleteChar(create_num=create_num, change_rate=change_rate)
    return smw.replace(test_str)


if __name__ == '__main__':
    # 【天大药业】 是个实体，会被换成很多别的同级别实体
    ts = '''”3月6日，2010年11月02日。中共中央总书记、国家主席、中央军委主席习近平在京出席决战决胜脱贫攻坚座谈会并发表重要讲话时这样强调'''
    rs = test(ts)
    for s in rs:
        print(s)
