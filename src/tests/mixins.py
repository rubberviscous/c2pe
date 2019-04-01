import os
from unittest import TestCase, mock

from c2pe.entrypoint import ChineseTranslator, create_parser, translate
from c2pe.utils import load_file


class CommandLineMixin(TestCase):
    pass


@mock.patch('c2pe.entrypoint.translate')
class BackendMixin(TestCase):
    # The input file path
    input_path = "files/lyrics.txt"

    @staticmethod
    def get_parser():
        return create_parser()

    @staticmethod
    def _get_backend(**kwargs):
        raise NotImplementedError()

    def _get_content(self):
        return load_file(self.input_path)

    def _get_translation(self, *mocks):
        return [('手中握着格桑花呀', 'shǒuzhōngwòzháogésānghuāyā', 'Holding Gesang flowers in my hand')]

    def test_with_input_args(self, *mocks):
        expected_output = self._get_translation()
        translate_mock = mocks[0]
        translate_mock.return_value = expected_output

        parser = self.get_parser()
        args = parser.parse_args(['files/lyrics.txt'])
        translated_output = translate(args.input)

        backend = self._get_backend(text=translated_output, source_path=args.input)
        backend.save()

        actual_output = backend.output()

        self.assertEqual(actual_output, expected_output)
