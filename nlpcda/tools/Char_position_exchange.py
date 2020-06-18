#!/usr/bin/python
# -*- coding: utf-8 -*-

from nlpcda.tools.Basetool import Basetool


class CharPositionExchange(Basetool):
    '''
    随机字 交换：研表究明，汉字序顺并不定一影响文字的阅读理解<<是乱序的
    '''

    def __init__(self, create_num: int = 5, change_rate: float = 0.05, char_gram: int = 3, seed: int = 1):
        super(CharPositionExchange, self).__init__('', create_num, change_rate, seed)
        self.char_gram = char_gram

    def __replace_one(self, one_sentence: str):
        # 变为字 数组
        sen_chars = list(one_sentence)
        for i in range(len(sen_chars)):
            if self.random.random() < self.change_rate:
                # 非中文字不动！
                if self.__is_chinese(sen_chars[i]) == False:
                    continue
                # 交换位置
                change_i = self.__cpt_exchange_position(sen_chars, i)
                # 进行交换
                sen_chars[i], sen_chars[change_i] = sen_chars[change_i], sen_chars[i]
        return ''.join(sen_chars)

    def __cpt_exchange_position(self, sen_chars: list, position_i):
        # 计算出交换位置
        i = position_i
        j = position_i
        # 从position_i左边，找到第一个不是中文的位置，or 全是中文则不能超过char_gram范围
        while i > 0 and self.__is_chinese(sen_chars[i]) and abs(i - position_i) < self.char_gram:
            i -= 1
        # 从position_i右边，找到第一个不是中文的位置，or 全是中文则不能超过char_gram范围
        while j < len(sen_chars) - 1 and self.__is_chinese(sen_chars[j]) and abs(j - position_i) < self.char_gram:
            j += 1
        # 不是中文导致的推出，需要撤回位置
        if not self.__is_chinese(sen_chars[i]):
            if i < position_i:
                i += 1
        if not self.__is_chinese(sen_chars[j]):
            if j > position_i:
                j -= 1
        return self.random.randint(i, j)

    def __is_chinese(self, a_chr):
        return u'\u4e00' <= a_chr <= u'\u9fff'

    def replace(self, replace_str: str):
        replace_str = replace_str.replace('\n', '').strip()
        sentences = [replace_str]
        t = 0

        while len(sentences) < self.create_num:
            t += 1
            a_sentence = self.__replace_one(replace_str)

            if a_sentence not in sentences:
                sentences.append(a_sentence)
            if t > self.create_num * self.loop_t / self.change_rate:
                break
        return sentences


def test(test_str, create_num=10, change_rate=0.5):
    smw = CharPositionExchange(create_num=create_num, change_rate=change_rate)
    return smw.replace(test_str)


if __name__ == '__main__':
    # 【天大药业】 是个实体，会被换成很多别的同级别实体
    ts = '''3月6日，2010年11月02日。中共中央总书记、国家主席、中央军委主席习近平在京出席决战决胜脱贫攻坚座谈会并发表重要讲话时这样强调'''
    rs = test(ts)
    for s in rs:
        print(s)
