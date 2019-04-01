import os
from typing import List, Tuple

from c2pe.backends.base_backend import BaseBackend


class BackendError(Exception):
    pass


class LocalBackend(BaseBackend):

    def __init__(self, data: List[Tuple], *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.data = data

        if self.input_path:
            normalized_path = self.normalize_path(self.input_path)
            self.output_path = self.generate_output_path(normalized_path)
        else:
            raise BackendError("Input path not specified.")

    def generate_output_path(self, path: str):
        """
        Generate output path based on input path
        :param path:
        :return:
        """
        file_name = self.filename[0]
        file_ext = self.filename[1]
        path = os.path.dirname(path)
        output_path = f'{path}/{file_name}_translated{file_ext}'
        return output_path

    @staticmethod
    def normalize_path(path: str):
        return os.path.expanduser(path)

    def save(self):
        if self.input_path:
            self.write_to_file(self.data, self.output_path)
        else:
            raise BackendError("The source path was not specified.")

    def write_to_file(self, data: List[Tuple], path):
        self.output_path = os.path.expanduser(path)
        filename_pair = os.path.splitext(path)

        if not filename_pair[0] and not filename_pair[1]:
            raise ValueError("invalid path specified")

        output_text = ""
        for line in data:
            for sub_line in line:
                output_text += f'{sub_line}\n'

            output_text += '\n'

        with open(path, 'w+') as f:
            f.write(output_text)

    def output(self):
        """
        Get the content of the saved file
        :return:
        """
        with open(self.output_path, 'r') as f:
            return f.read()

    @staticmethod
    def write_to_stdout(text):
        # write output to stdout
        print(text)
