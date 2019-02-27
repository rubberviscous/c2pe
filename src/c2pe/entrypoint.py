#!/usr/bin/env python3

import argparse
import os

from googletrans import Translator
import pinyin


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

    def output(self) -> str:
        self.text = self.normalize()
        text_list = self.text.split("\n")

        translated_text = self._translate()
        translated_text_list = translated_text.split("\n")

        py = self._pinyin()
        pinyin_list = py.split("\n")

        zipped = zip(text_list, pinyin_list, translated_text_list)
        output = list(zipped)

        output_text = ""
        for line in output:
            for sub_line in line:
                output_text += f'{sub_line}\n'

            output_text += '\n'

        return output_text


def load_file(path: str) -> str:
    """
    Will load file and extract all characters as strings, given relative or absolute path
    :param path:
    :return str:
    """
    # if path begins with ~, will expand path
    path = os.path.expanduser(path)
    data = None
    with open(path, 'r') as f:
        data = f.read()
    return data


def write_output(text: str, path: str):
    if path:
        write_to_file(text, path)
    else:
        # output to stdout
        write_to_stdout(text)


def write_to_file(text, path):
    path = os.path.expanduser(path)
    filename_pair = os.path.splitext(path)

    if not filename_pair[0] and not filename_pair[1]:
        raise ValueError("invalid path specified")

    with open(path, 'w+') as f:
        f.write(text)


def write_to_stdout(text):
    # write output to stdout
    print(text)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="The path to file containing Chinese characters.")
    parser.add_argument("--output", type=str, help="The path to save the output.")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    chinese_chars = load_file(args.input)

    translator = ChineseTranslator(chinese_chars)
    translated_output = translator.output()

    write_output(translated_output, args.output)


if __name__ == '__main__':
    main()


