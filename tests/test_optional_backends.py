import os
import sys
import types
import unittest
from unittest.mock import Mock, patch

from nlpcda import Simbert, baidu_translate


class BackendTests(unittest.TestCase):
    def test_simbert_defaults_do_not_mutate_config_or_require_cuda(self):
        generator = types.ModuleType("nlpcda.tools.simbert.generator")
        generator.SynonymsGenerator = Mock()
        config = {"model_path": "/local/model"}
        with patch.dict(sys.modules, {"nlpcda.tools.simbert.generator": generator}), patch.dict(
            os.environ, {}, clear=False
        ):
            os.environ.pop("CUDA_VISIBLE_DEVICES", None)
            model = Simbert(config)
            self.assertNotIn("CUDA_VISIBLE_DEVICES", os.environ)
            generator.SynonymsGenerator.assert_called_once_with("/local/model", 32, 1)
            self.assertEqual(model.config["seed"], 1)
        self.assertEqual(config, {"model_path": "/local/model"})

    def test_simbert_requires_explicit_model_path(self):
        with self.assertRaisesRegex(ValueError, "model_path"):
            Simbert()

    def test_simbert_missing_optional_dependency_is_actionable(self):
        with patch.dict(sys.modules, {"nlpcda.tools.simbert.generator": None}):
            with self.assertRaisesRegex(ImportError, "optional dependencies"):
                Simbert({"model_path": "/local/model"})

    @patch("nlpcda.tools.Translate.requests.get")
    def test_translation_uses_https_timeout_and_all_returned_lines(self, get):
        get.return_value.json.return_value = {"trans_result": [{"dst": "你好"}, {"dst": "世界"}]}
        self.assertEqual(baidu_translate("hello\nworld", "id", "secret", timeout=5), "你好\n世界")
        args, kwargs = get.call_args
        self.assertTrue(args[0].startswith("https://"))
        self.assertEqual(kwargs["timeout"], 5)
        self.assertEqual(kwargs["params"]["q"], "hello\nworld")
        get.return_value.raise_for_status.assert_called_once_with()

    @patch("nlpcda.tools.Translate.requests.get")
    def test_translation_api_errors_are_descriptive(self, get):
        get.return_value.json.return_value = {"error_code": "54003", "error_msg": "rate limit"}
        with self.assertRaisesRegex(RuntimeError, "54003.*rate limit"):
            baidu_translate("hello", "id", "secret")

    @patch("nlpcda.tools.Translate.requests.get")
    def test_translation_rejects_invalid_response(self, get):
        for response in ({"trans_result": []}, [], None):
            with self.subTest(response=response):
                get.return_value.json.return_value = response
                with self.assertRaisesRegex(RuntimeError, "invalid response"):
                    baidu_translate("hello", "id", "secret")


if __name__ == "__main__":
    unittest.main()
