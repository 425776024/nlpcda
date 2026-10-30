import random
import tempfile
import unittest
from pathlib import Path

from nlpcda import Ner


class NerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def write(self, name, content):
        path = self.root / name
        path.write_bytes(content.encode("utf-8"))
        return path

    def test_blank_sentence_separators_crlf_and_no_trailing_newline(self):
        path = self.write("train.txt", "北\tB-LOC\r\n京\tI-LOC\r\n\r\n上\tB-LOC\r\n海\tI-LOC")
        (self.root / "nested").mkdir()
        self.write(".DS_Store", "not annotation data")
        ner = Ner(self.root, ["O"], ["LOC"], augument_size=3)
        sentences, labels = ner.augment(path)
        self.assertEqual(["".join(chars) for chars in sentences], ["上海", "北京"])
        self.assertEqual(labels, [["B-LOC", "I-LOC"], ["B-LOC", "I-LOC"]])

    def test_singleton_entity_pool_returns_no_candidates(self):
        path = self.write("train.txt", "北\tB-LOC\n京\tI-LOC\n")
        ner = Ner(self.root, ["O"], ["LOC"])
        self.assertEqual(ner.augment(path), ([], []))

    def test_length_changing_replacement_regenerates_bio_labels(self):
        path = self.write("train.txt", "北\tB-LOC\n京\tI-LOC\n好\tO\n")
        self.write("other.txt", "上\tB-LOC\n海\tI-LOC\n市\tI-LOC\n")
        ner = Ner(self.root, ["O"], ["LOC"])
        sentences, labels = ner.augment(path)
        self.assertEqual(sentences, [list("上海市好")])
        self.assertEqual(labels, [["B-LOC", "I-LOC", "I-LOC", "O"]])

    def test_ner_does_not_change_global_random_or_other_instances(self):
        path = self.write("train.txt", "北\tB-LOC\n京\tI-LOC\n")
        self.write("other.txt", "上\tB-LOC\n海\tI-LOC\n\n深\tB-LOC\n圳\tI-LOC\n")
        random.seed(123)
        before = random.getstate()
        first = Ner(self.root, ["O"], ["LOC"], seed=7)
        expected = first.augment(path)
        second = Ner(self.root, ["O"], ["LOC"], seed=7)
        Ner(self.root, ["O"], ["LOC"], seed=999).augment(path)
        self.assertEqual(second.augment(path), expected)
        self.assertEqual(random.getstate(), before)

    def test_invalid_bio_reports_file_and_line(self):
        for annotation in ("坏行\n", "北\tS-LOC\n", "北\tI-LOC\n"):
            with self.subTest(annotation=annotation):
                self.write("train.txt", annotation)
                with self.assertRaisesRegex(ValueError, r"train.txt:1:"):
                    Ner(self.root, ["O"], ["LOC"])

    def test_zero_size_is_noop_and_negative_size_is_rejected(self):
        path = self.write("train.txt", "北\tB-LOC\n京\tI-LOC\n")
        self.assertEqual(Ner(self.root, ["O"], ["LOC"], augument_size=0).augment(path), ([], []))
        with self.assertRaisesRegex(ValueError, "augument_size"):
            Ner(self.root, ["O"], ["LOC"], augument_size=-1)


if __name__ == "__main__":
    unittest.main()
