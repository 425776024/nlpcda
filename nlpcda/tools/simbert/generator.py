# -*- coding: utf-8 -*-
import os
import numpy as np
from bert4keras.backend import keras
from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import sequence_padding, AutoRegressiveDecoder


def setup_seed(seed):
    try:
        import random
        import numpy as np
        np.random.seed(seed)
        random.seed(seed)
    except Exception as e:
        pass


class SynonymsGenerator(AutoRegressiveDecoder):
    """seq2seq解码器
    """

    def __init__(self, model_path, max_len=32, seed=1):
        # super().__init__()
        setup_seed(seed)
        self.config_path = os.path.join(model_path, "bert_config.json")
        self.checkpoint_path = os.path.join(model_path, "bert_model.ckpt")
        self.dict_path = os.path.join(model_path, "vocab.txt")
        self.max_len = max_len
        self.tokenizer = Tokenizer(self.dict_path, do_lower_case=True)
        self.bert = build_transformer_model(
            self.config_path,
            self.checkpoint_path,
            with_pool='linear',
            application='unilm',
            return_keras_model=False,
        )
        self.encoder = keras.models.Model(self.bert.model.inputs,
                                          self.bert.model.outputs[0])
        self.seq2seq = keras.models.Model(self.bert.model.inputs,
                                          self.bert.model.outputs[1])
        super().__init__(start_id=None, end_id=self.tokenizer._token_end_id,
                         maxlen=self.max_len)

    @AutoRegressiveDecoder.set_rtype('probas')
    def predict(self, inputs, output_ids, states):
        token_ids, segment_ids = inputs
        token_ids = np.concatenate([token_ids, output_ids], 1)
        segment_ids = np.concatenate(
            [segment_ids, np.ones_like(output_ids)], 1)
        return self.seq2seq.predict([token_ids, segment_ids])[:, -1]

    def generate(self, text, n=1, topk=5):
        token_ids, segment_ids = self.tokenizer.encode(
            text, max_length=self.max_len)
        output_ids = self.random_sample([token_ids, segment_ids], n, topk)
        return [self.tokenizer.decode(ids) for ids in output_ids]

    def gen_synonyms(self, text, n=100, k=20, threhold=0.75):
        """"含义： 产生sent的n个相似句，然后返回最相似的k个。
        做法：用seq2seq生成，并用encoder算相似度并排序。
        """
        r = self.generate(text, n)
        r = [i for i in set(r) if i != text]
        r = [text] + r
        X, S = [], []
        for t in r:
            x, s = self.tokenizer.encode(t)
            X.append(x)
            S.append(s)
        X = sequence_padding(X)
        S = sequence_padding(S)
        Z = self.encoder.predict([X, S])
        Z /= (Z ** 2).sum(axis=1, keepdims=True) ** 0.5
        scores = np.dot(Z[1:], Z[0])
        argsort = scores.argsort()
        scores = scores.tolist()
        # print(scores.shape)
        # return [(r[i + 1], scores[i]) for i in argsort[::-1][:k] if scores[i] > threhold]
        return [(r[i + 1], scores[i]) for i in argsort[::-1][:k]]
