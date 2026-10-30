#!/usr/bin/python
# -*- coding: utf-8 -*-


from nlpcda.config import Equivalent_char_path
from nlpcda.tools.Basetool import Basetool


class EquivalentChar(Basetool):
    """
    等价字，用于随机替换等价字，【字级别的】，增强数据
    """

    def __init__(
        self, base_file=Equivalent_char_path, create_num=5, change_rate=0.05, seed=1, stopwords=None
    ):
        super(EquivalentChar, self).__init__(base_file, create_num, change_rate, seed, stopwords)

    def load_paser_base_file(self):
        self.base_file_mapobj = {}
        with open(self.base_file, "r", encoding="utf-8") as source:
            for line in source:
                equivalent_list = line.split()
                if equivalent_list:
                    self.add_equivalent_list(equivalent_list)
        return self.base_file_mapobj

    def add_equivalent_list(self, equivalent_list):
        """
        添加等价字list
        :param equivalent_list:
        :return:
        """
        if isinstance(equivalent_list, str):
            raise ValueError("equivalent_list must contain at least two distinct strings")
        equivalent_list = list(dict.fromkeys(equivalent_list))
        if len(equivalent_list) < 2 or any(
            not isinstance(word, str) or not word for word in equivalent_list
        ):
            raise ValueError("equivalent_list must contain at least two distinct strings")
        num = len(equivalent_list)
        for i in range(num - 1):
            self.base_file_mapobj[equivalent_list[i]] = (
                equivalent_list[:i] + equivalent_list[i + 1 :]
            )
        self.base_file_mapobj[equivalent_list[-1]] = equivalent_list[:-1]

    def replace(self, replace_str: str):
        replace_str = self._validate_text(replace_str)
        chars = list(replace_str)
        protected = self._protected_positions(replace_str)

        def generate_one():
            a_sentence = ""
            for index, chrr in enumerate(chars):
                if (
                    index not in protected
                    and chrr in self.base_file_mapobj
                    and self.random.random() < self.change_rate
                ):
                    wi = self.random.randint(0, len(self.base_file_mapobj[chrr]) - 1)
                    place = self.base_file_mapobj[chrr][wi]
                else:
                    place = chrr
                a_sentence += place
            return a_sentence

        return self._generate_sentences(replace_str, generate_one)


def test(test_str, create_num=3, change_rate=0.3):
    hoe = EquivalentChar(create_num=create_num, change_rate=change_rate)
    return hoe.replace(test_str)


if __name__ == "__main__":
    ts = """今天是7月5日21:32:21。"""
    rs = test(ts)
    for s in rs:
        print(s)
