#!/usr/bin/python
# -*- coding: utf-8 -*-


from nlpcda.tools.Basetool import Basetool
from nlpcda.config import Equivalent_char_path


class EquivalentChar(Basetool):
    '''
    等价字，用于随机替换等价字，【字级别的】，增强数据
    '''

    def __init__(self, base_file=Equivalent_char_path, create_num=5, change_rate=0.05, seed=1):
        super(EquivalentChar, self).__init__(base_file, create_num, change_rate, seed)

    def load_paser_base_file(self):
        self.base_file_mapobj = {}
        for line in open(self.base_file, "r", encoding='utf-8'):
            equivalent_list = line.strip().split("\t")
            assert len(equivalent_list) > 1
            self.add_equivalent_list(equivalent_list)
        print('load :%s done' % (self.base_file))
        return self.base_file_mapobj

    def add_equivalent_list(self, equivalent_list):
        '''
        添加等价字list
        :param equivalent_list:
        :return:
        '''
        num = len(equivalent_list)
        for i in range(num - 1):
            self.base_file_mapobj[equivalent_list[i]] = equivalent_list[:i] + equivalent_list[i + 1:]
        self.base_file_mapobj[equivalent_list[-1]] = equivalent_list[:-1]

    def replace(self, replace_str: str):
        replace_str = replace_str.replace('\n', '').strip()
        chars = list(replace_str)
        sentences = [replace_str]
        t = 0
        while len(sentences) < self.create_num:
            t += 1
            a_sentence = ''
            for chrr in chars:
                if chrr in self.base_file_mapobj and self.random.random() < self.change_rate:
                    wi = self.random.randint(0, len(self.base_file_mapobj[chrr]) - 1)
                    place = self.base_file_mapobj[chrr][wi]
                else:
                    place = chrr
                a_sentence += place
            if a_sentence not in sentences:
                sentences.append(a_sentence)
            if t > self.create_num * self.loop_t / self.change_rate:
                break
        return sentences


def test(test_str, create_num=3, change_rate=0.3):
    hoe = EquivalentChar(create_num=create_num, change_rate=change_rate)
    try:
        return hoe.replace(test_str)
    except:
        print('error in Homophone.replace')
        return [test_str]


if __name__ == '__main__':
    ts = '''今天是7月5日21:32:21。'''
    rs = test(ts)
    for s in rs:
        print(s)
