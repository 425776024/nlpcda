#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from nlpcda.tools.simbert.generator import SynonymsGenerator


class Simbert:
    _config = {
        'model_path': '/xxx/chinese_simbert_L-12_H-768_A-12',
        'device': 'cpu',
        'max_len': 32,
        'seed': 1
    }

    def __init__(self, config: dict = {}):
        if config.get('device') is None:
            config['device'] = self._config['device']
        if config.get('max_len') is None:
            config['max_len'] = self._config['max_len']
        if config.get('seed') is None:
            config['seed'] = self._config['seed']

        self.config = config
        if config['device'] == 'cpu':
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        self.model = SynonymsGenerator(config['model_path'], config['max_len'], config['seed'])

    def replace(self, sent, k=5, threhold=0.85):
        # 产生n个相似句结果，取相似度大于阈值threhold的里面的前k个
        n = k * 4
        synonyms = self.model.gen_synonyms(text=sent, n=n, k=k, threhold=threhold)
        return synonyms


if __name__ == '__main__':
    config = {
        'model_path': '/xxxx/chinese_simbert_L-12_H-768_A-12',
        'device': 'cpu',
        'max_len': 32,
        'seed': 1,
        'threhold': 0.8,
    }
    simbert = Simbert(config=config)
    sent = '把我的一个亿存银行安全吗'
    synonyms = simbert.replace(sent=sent, k=5, threhold=0.85)
    print(synonyms)
