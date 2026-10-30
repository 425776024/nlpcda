import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import jieba

from nlpcda import (
    CharPositionExchange, EquivalentChar, Homophone, RandomDeleteChar,
    Randomword, Similarword,
)
from nlpcda.tools.Basetool import Basetool


AUGMENTERS = (CharPositionExchange, EquivalentChar, Homophone,
              RandomDeleteChar, Randomword, Similarword)


class AugmenterTests(unittest.TestCase):
    def test_zero_rate_preserves_exact_input_for_every_augmenter(self):
        for cls in AUGMENTERS:
            with self.subTest(augmenter=cls.__name__):
                augmenter = cls(create_num=3, change_rate=0)
                for text in ('', '短句', '  今天是2026年10月30日\n天气很好  '):
                    self.assertEqual(augmenter.replace(text), [text])

    def test_original_is_included_and_outputs_are_unique(self):
        for cls in AUGMENTERS:
            with self.subTest(augmenter=cls.__name__):
                text = '今天是2026年10月30日，天气很好，欢迎使用数据增强工具。'
                results = cls(create_num=4, change_rate=0.3).replace(text)
                self.assertEqual(results[0], text)
                self.assertLessEqual(len(results), 4)
                self.assertEqual(len(results), len(set(results)))

    def test_invalid_parameters_fail_before_loading_resources(self):
        for cls in AUGMENTERS:
            for value in (0, -1, 1.5, True, '3'):
                with self.subTest(augmenter=cls.__name__, create_num=value):
                    with self.assertRaisesRegex(ValueError, 'create_num'):
                        cls(create_num=value)
            for value in (-0.1, 1.1, float('nan'), float('inf'), True, '0.1'):
                with self.subTest(augmenter=cls.__name__, change_rate=value):
                    with self.assertRaisesRegex(ValueError, 'change_rate'):
                        cls(change_rate=value)
        for value in (0, -1, 1.5, True):
            with self.assertRaisesRegex(ValueError, 'char_gram'):
                CharPositionExchange(char_gram=value)

    def test_non_string_input_is_rejected_consistently(self):
        for cls in AUGMENTERS:
            with self.subTest(augmenter=cls.__name__):
                with self.assertRaisesRegex(TypeError, 'string'):
                    cls().replace(None)

    def test_deletion_preserves_protected_final_number_and_final_word(self):
        augmenter = RandomDeleteChar(create_num=3, change_rate=1)
        for text in ('今天北京天气很好12345', '今天北京天气很好数据增强'):
            with self.subTest(text=text):
                last_word = list(augmenter.jieba.cut(text))[-1]
                for result in augmenter.replace(text):
                    self.assertTrue(result.endswith(last_word), result)

    def test_seed_is_local_and_instances_do_not_interfere(self):
        random.seed(2026)
        global_state = random.getstate()
        first = CharPositionExchange(create_num=5, change_rate=0.8, seed=7)
        expected = first.replace('欢迎使用中文数据增强工具测试随机状态隔离')
        actual_augmenter = CharPositionExchange(create_num=5, change_rate=0.8, seed=7)
        other = CharPositionExchange(seed=999)
        other.replace('另一个增强器不应该改变已有增强器的随机序列')
        self.assertEqual(actual_augmenter.replace('欢迎使用中文数据增强工具测试随机状态隔离'), expected)
        self.assertEqual(random.getstate(), global_state)

    def test_user_dictionary_is_local_to_each_instance(self):
        word = '甲乙专属自定义词丙丁'
        global_frequency = jieba.dt.FREQ.get(word)
        first, second = CharPositionExchange(), CharPositionExchange()
        first.add_word(word)
        self.assertIn(word, first.jieba.FREQ)
        self.assertNotIn(word, second.jieba.FREQ)
        self.assertEqual(jieba.dt.FREQ.get(word), global_frequency)

    def test_tiny_change_rate_has_bounded_retries(self):
        augmenter = Basetool('', create_num=3, change_rate=1e-320)
        calls = []

        def unchanged():
            calls.append(None)
            return '原文'

        self.assertEqual(augmenter._generate_sentences('原文', unchanged), ['原文'])
        self.assertLessEqual(len(calls), 600)

    def test_custom_synonym_ids_and_whitespace_are_supported(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'synonyms.txt'
            path.write_text('\ncustom   开心\t高兴\nrelated# 开心 悲伤\n', encoding='utf-8')
            augmenter = Similarword(base_file=path, change_rate=1)
            self.assertEqual(augmenter.s1('开心'), '高兴')

    def test_custom_entities_are_added_to_local_tokenizer(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'entities.txt'
            path.write_text('甲乙专属公司\n丙丁专属公司\n\n', encoding='utf-8')
            augmenter = Randomword(base_file=path, change_rate=1, create_num=2)
            self.assertIn('甲乙专属公司', list(augmenter.jieba.cut('今天甲乙专属公司发布产品。')))
            result = augmenter.replace('今天甲乙专属公司发布产品。')
            self.assertEqual(len(result), 2)
            self.assertIn('丙丁专属公司', result[1])
            self.assertEqual(augmenter.replace('甲乙专属公司'), ['甲乙专属公司', '丙丁专属公司'])

    def test_import_does_not_load_optional_model_dependencies_or_print(self):
        script = '''
import importlib.abc
import sys
class BlockModels(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'bert4keras', 'tensorflow', 'keras', 'numpy'}:
            raise AssertionError('Unexpected optional import: ' + fullname)
sys.meta_path.insert(0, BlockModels())
from nlpcda import *
assert Simbert is not None
'''
        result = subprocess.run([sys.executable, '-c', script], text=True,
                                capture_output=True, check=True)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
