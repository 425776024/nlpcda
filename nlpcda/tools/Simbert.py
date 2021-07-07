#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from nlpcda.tools.simbert.generator import SynonymsGenerator


class Simbert:
    _config = {
        'model_path': '/xxx/chinese_simbert_L-12_H-768_A-12',
        'CUDA_VISIBLE_DEVICES': '0,1',
        'max_len': 32,
        'seed': 1
    }

    def __init__(self, config: dict = {}):
        if config.get('max_len') is None:
            config['max_len'] = self._config['max_len']
        if config.get('seed') is None:
            config['seed'] = self._config['seed']

        self.config = config
        os.environ["CUDA_VISIBLE_DEVICES"] = config['CUDA_VISIBLE_DEVICES']
        self.model = SynonymsGenerator(config['model_path'], config['max_len'], config['seed'])

    def replace(self, sent:str, create_num=5):
        # 产生n个相似句结果，取相似度大于阈值threhold的里面的前k个
        n = create_num * 4
        synonyms = self.model.gen_synonyms(text=sent, n=n, k=create_num)
        return synonyms


if __name__ == '__main__':
    config = {
        'model_path': '/Users/jiang/Documents/pre_train_models/chinese_simbert_L-12_H-768_A-12',
        'max_len': 32,
        'seed': 1
    }
    simbert = Simbert(config=config)
    sent = '我天啊！太罕见了！山下智久木村拓哉龟梨和也同框'
    synonyms = simbert.replace(sent=sent, create_num=5)
    print(synonyms)
