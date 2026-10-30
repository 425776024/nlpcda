#!/usr/bin/python
# -*- coding: utf-8 -*-


from nlpcda.config import homophone_path
from nlpcda.tools.Basetool import Basetool


class Homophone(Basetool):
    """
    按拼音分组的同音字替换，用于字符级数据扰动。
    """

    def __init__(
        self, base_file=homophone_path, create_num=5, change_rate=0.05, seed=1, stopwords=None
    ):
        super(Homophone, self).__init__(base_file, create_num, change_rate, seed, stopwords)

    def load_paser_base_file(self):
        combine_dict = {}
        with open(self.base_file, "r", encoding="utf-8") as source:
            for line in source:
                seperate_word = line.split()
                for word in seperate_word[1:]:
                    combine_dict[word] = [other for other in seperate_word[1:] if other != word]
        return combine_dict

    def replace(self, replace_str: str):
        replace_str = self._validate_text(replace_str)
        words = list(replace_str)
        protected = self._protected_positions(replace_str)

        def generate_one():
            a_sentence = ""
            for index, word in enumerate(words):
                if (
                    index not in protected
                    and self.base_file_mapobj.get(word)
                    and self.random.random() < self.change_rate
                ):
                    wi = self.random.randint(0, len(self.base_file_mapobj[word]) - 1)
                    place = self.base_file_mapobj[word][wi]
                else:
                    place = word
                a_sentence += place
            return a_sentence

        return self._generate_sentences(replace_str, generate_one)


def test(test_str, create_num=10, change_rate=0.3):
    hoe = Homophone(create_num=create_num, change_rate=change_rate)
    return hoe.replace(test_str)


if __name__ == "__main__":
    ts = """这是一场疫情防控的人民战争、总体战、阻击战，习近平总书记亲自指挥、亲自部署。运筹帷幄 指挥若定始终把人民群众生命安全和身体健康放在第一位"""
    rs = test(ts)
    for s in rs:
        print(s)
