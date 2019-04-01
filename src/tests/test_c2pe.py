import os
from typing import List, Tuple
from unittest import TestCase, mock

import c2pe
from c2pe.entrypoint import create_parser, ChineseTranslator
from c2pe.utils import load_file


class TestTranslate(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = create_parser()

    @staticmethod
    def _get_content(path='files/lyrics.txt'):
        with open(path, 'r') as f:
            return f.read()

    def setUp(self):
        text = self._get_content()
        self.translator = ChineseTranslator(text)

    def test_with_no_args(self):
        with self.assertRaises(SystemExit):
            self.args = self.parser.parse_args([])

    def test_load_file_relative(self):
        actual_text = load_file('files/lyrics.txt')
        expected_text = "手中握着格桑花呀"
        self.assertEqual(expected_text, actual_text)

    def test_load_file_absolute(self):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        actual_text = load_file(f'{abs_path}/files/lyrics.txt')
        expected_text = "手中握着格桑花呀"
        self.assertEqual(expected_text, actual_text)

    # @mock.patch.object(c2pe.entrypoint.ChineseTranslator, '_translate')
    @mock.patch('c2pe.entrypoint.ChineseTranslator._translate')
    def test_translate(self, *mocks):
        translate_mock = mocks[0]
        translate_mock.return_value = "Holding Gesang flowers in my hand"
        actual_output: List[Tuple] = self.translator.output()
        # expected_output = """手中握着格桑花呀\nshǒuzhōngwòzháogésānghuāyā\nHolding Gesang flowers in my hand\n\n"""
        self.assertEqual(len(actual_output), 1)
        print('hello')

    def test_remove_empty_lines(self):
        text = self._get_content('files/empty_lines.txt')
        self.translator = ChineseTranslator(text)
        normalized_text = self.translator.output()
        print(normalized_text)



