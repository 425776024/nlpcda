#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 15:18


import os
from collections import defaultdict
import random
from numbers import Integral


def get_random(start, end):
    assert start <= end - 1
    return random.randint(start, end - 1)


class Ner:
    def __init__(self, ner_dir_name: str, ignore_tag_list: list,
                 data_augument_tag_list: list,
                 augument_size: int = 3,
                 seed: int = 0):
        if isinstance(augument_size, bool) or not isinstance(augument_size, Integral) or augument_size < 0:
            raise ValueError('augument_size must be a non-negative integer')
        self.random = random.Random(seed)
        self.ignore_tag_list = ignore_tag_list
        self.size = augument_size
        self.data_augument_tag_list = data_augument_tag_list
        self.tag_map = self.__get_all_tag_map(ner_dir_name)

    def __get_random_ner(self, tag: str, original: str):
        candidates = [entity for entity in self.tag_map[tag] if entity != original]
        return self.random.choice(candidates) if candidates else original

    def __get_all_tag_map(self, dir_name: str):
        '''
        得到目录下全部标注文件的，各种实体，ignore_tag_list 里面的不要
        :param dir_name:
        :return:
        '''
        tag_map = defaultdict(list)
        for name in sorted(os.listdir(dir_name)):
            file_path = os.path.join(dir_name, name)
            if not os.path.isfile(file_path) or name.startswith('.'):
                continue
            data_iter = self.__get_file_data_iter(file_path)
            for char_tag in data_iter:
                t_tag, t_ner_sentence = char_tag[0], char_tag[1]
                if t_tag in self.ignore_tag_list:
                    continue
                if t_ner_sentence not in tag_map[t_tag]:
                    tag_map[t_tag].append(t_ner_sentence)
        return tag_map

    def __get_file_data_iter(self, file_path: str):
        for sentence in self.__get_sentence_data_iter(file_path):
            yield from sentence

    def __get_sentence_data_iter(self, file_path: str):
        '''
        NER的BIO标注文本 xxx.txt的file_path，要对它做增强
        :param file_path: 路径path
        :return:
        '''
        with open(file_path, 'r', encoding='utf-8') as r_f:
            pre_tag = ''
            ner_sentence = ''
            sentence = []
            for line_number, line in enumerate(r_f, 1):
                if not line.strip():
                    if ner_sentence:
                        sentence.append([pre_tag, ner_sentence])
                    if sentence:
                        yield sentence
                    pre_tag, ner_sentence, sentence = '', '', []
                    continue
                fields = line.rstrip('\r\n').rsplit('\t', 1)
                if len(fields) != 2 or not fields[0]:
                    raise ValueError(f'{file_path}:{line_number}: expected token<TAB>BIO-label')
                t_char, t_label = fields
                if t_label == 'O':
                    tp_tag = 'O'
                elif t_label.startswith(('B-', 'I-')) and len(t_label) > 2:
                    tp_tag = t_label[2:]
                else:
                    raise ValueError(f'{file_path}:{line_number}: invalid BIO label {t_label!r}')
                if t_label.startswith('I-') and pre_tag != tp_tag:
                    raise ValueError(f'{file_path}:{line_number}: I-label must follow the same entity type')
                if pre_tag == '':
                    pre_tag = tp_tag
                    ner_sentence += t_char
                elif pre_tag == tp_tag and t_label[0] != 'B':
                    ner_sentence += t_char
                else:
                    sentence.append([pre_tag, ner_sentence])
                    pre_tag = tp_tag
                    ner_sentence = t_char
            if ner_sentence != '':
                sentence.append([pre_tag, ner_sentence])
            if sentence:
                yield sentence

    def __data_augment_one(self, org_data):

        new_data = []
        for di in org_data:
            t_tag, t_ner_sentence = di[0], di[1]
            if t_tag in self.data_augument_tag_list and t_tag in self.tag_map:
                rdm_select_ner = self.__get_random_ner(t_tag, t_ner_sentence)
                new_data.append([t_tag, rdm_select_ner])
            else:
                new_data.append([t_tag, t_ner_sentence])
        return new_data

    def __data_augment(self, org_data, size=3):
        '''
        对原始数据做增强
        :param org_data:
        :param size: 增强/最多/数量
        :return:
        '''

        new_data = []
        seen = set()
        org_sent = ''.join([di[1] for di in org_data])
        for i in range(size):
            o_new_data = self.__data_augment_one(org_data)
            new_sent = ''.join([di[1] for di in o_new_data])
            if org_sent != new_sent and new_sent not in seen:
                new_data.append(o_new_data)
                seen.add(new_sent)
        return new_data

    def __paser_ner(self, ner_data):
        # 数据还原成NER数组，字数组，标签数组
        sentence_arr = []
        label_arr = []
        for i in range(len(ner_data)):
            for j in range(len(ner_data[i][1])):
                if ner_data[i][0] == 'O':
                    label_arr.append(ner_data[i][0])
                else:
                    if j == 0:
                        label_arr.append('B-' + ner_data[i][0])
                    else:
                        label_arr.append('I-' + ner_data[i][0])
                sentence_arr.append(ner_data[i][1][j])
        return sentence_arr, label_arr

    def augment(self, file_name) -> tuple:
        '''
        对文件做增强，输出文件路径，返回size个增强好的数据对 [sentence_arr, label_arr]
        :param file_name:
        :return:
        '''
        data_sentence_arrs = []
        data_label_arrs = []
        for org_data in self.__get_sentence_data_iter(file_name):
            for ndi in self.__data_augment(org_data, self.size):
                sentence_arr, label_arr = self.__paser_ner(ndi)
                data_sentence_arrs.append(sentence_arr)
                data_label_arrs.append(label_arr)
        return data_sentence_arrs, data_label_arrs
