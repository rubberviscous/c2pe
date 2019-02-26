import os
from unittest import TestCase, mock

from c2pe.entrypoint import create_parser, load_file, write_output, ChineseTranslator


class TestTranslate(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = create_parser()

    @staticmethod
    def _get_content():
        with open('files/lyrics.txt', 'r') as f:
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

    def test_write_output_relative_path(self):
        text = "test"
        path = "files/test.txt"
        write_output(text, path)

        filename_pair = os.path.splitext(path)
        expected_path = f"{filename_pair[0]}_translated{filename_pair[1]}"

        self.assertTrue(os.path.exists(expected_path))
        os.remove(expected_path)

    def test_write_output_absolute_path(self):
        text = "test"
        abs_path = os.path.dirname(os.path.abspath(__file__))
        path = f"{abs_path}/files/test.txt"
        write_output(text, path)
        filename_pair = os.path.splitext(path)
        expected_path = f"{filename_pair[0]}_translated{filename_pair[1]}"
        self.assertTrue(os.path.exists(expected_path))
        os.remove(expected_path)

    def test_write_output_absolute_path_with_no_file_extension(self):
        text = "test"
        abs_path = os.path.dirname(os.path.abspath(__file__))
        path = f"{abs_path}/files/test"
        write_output(text, path)
        filename_pair = os.path.splitext(path)
        expected_path = f"{filename_pair[0]}_translated{filename_pair[1]}"
        self.assertTrue(os.path.exists(expected_path))
        os.remove(expected_path)

    @mock.patch('c2pe.entrypoint.write_to_stdout')
    def test_write_output_stdout(self, *mocks):
        # Ensure that output is written to stdout if no path is given
        stdout_mock = mocks[0]
        text = "test"
        path = None
        write_output(text, path)
        self.assertEqual(1, stdout_mock.call_count)

    @mock.patch('c2pe.entrypoint.ChineseTranslator._translate')
    def test_translate(self, *mocks):
        translate_mock = mocks[0]
        translate_mock.return_value = "Holding Gesang flowers in my hand"
        text = self._get_content()
        actual_output = self.translator.output()
        expected_output = """手中握着格桑花呀\nshǒuzhōngwòzháogésānghuāyā\nHolding Gesang flowers in my hand\n\n"""
        self.assertEqual(actual_output, expected_output)



