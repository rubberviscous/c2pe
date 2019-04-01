#!/usr/bin/env python3

import argparse
import importlib
from typing import List, Tuple

from googletrans import Translator
import pinyin

from c2pe.utils import load_file


class ChineseTranslator(object):

    def __init__(self, text):
        self.text = text

    def _translate(self) -> str:
        translator = Translator()
        translation = translator.translate(self.text)
        return translation.text

    def _pinyin(self):
        return pinyin.get(self.text)

    def normalize(self) -> str:
        text_list = [line for line in self.text.split("\n") if line.strip() != '']

        return '\n'.join(text_list)

    def output(self) -> List[Tuple]:
        """
        Each line of chinese characters are translated to pinyin and english
        :return:
        A list of tuples. Each tuple consists of chinese, pinyin, and english.
        [(手中握着格桑花呀, shǒuzhōngwòzháogésānghuāyā, Holding Gesang flowers in my hand)]
        """
        self.text = self.normalize()
        text_list = self.text.split("\n")

        translated_text = self._translate()
        translated_text_list = translated_text.split("\n")

        py = self._pinyin()
        pinyin_list = py.split("\n")

        zipped = zip(text_list, pinyin_list, translated_text_list)
        output = list(zipped)

        return output

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="The path to file containing Chinese characters.")
    parser.add_argument("--backend", type=str, help="The backend to use to save the file. Defaults to local.",
                        default="local")
    # parser.add_argument("--output", type=str, help="The path to save the output.")
    return parser


def get_backend_cls(name: str):
    module_path = f'c2pe.backends.{name}_backend'
    module = importlib.import_module(module_path)
    backend_cls = getattr(module, f'{name.capitalize()}Backend')
    return backend_cls


def translate(file: str) -> List[Tuple]:
    chinese_chars = load_file(file)

    translator = ChineseTranslator(chinese_chars)
    return translator.output()


def main():
    parser = create_parser()
    args = parser.parse_args()

    translated_output: List[Tuple] = translate(args.input)

    # import backend
    backend_cls = get_backend_cls(args.backend)
    backend_instance = backend_cls(data=translated_output, source_path=args.input)
    backend_instance.save()


if __name__ == '__main__':
    main()


