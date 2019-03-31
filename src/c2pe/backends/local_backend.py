import os

from c2pe.backends.base_backend import BaseBackend


class BackendError(Exception):
    pass


class LocalBackend(BaseBackend):

    def __init__(self, text: str, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.text = text
        self.source_path = kwargs.get("source_path", None)

    def save(self):
        if self.source_path:
            filename_with_ext = os.path.basename(self.source_path)
            file_splitext = os.path.splitext(filename_with_ext)
            file_name = file_splitext[0]
            file_ext = file_splitext[1]
            path = os.path.dirname(self.source_path)
            save_path = f'{path}/{file_name}_translated{file_ext}'
            self.write_to_file(self.text, save_path)
        else:
            # output to stdout
            # self.write_to_stdout(self.text)
            raise BackendError("The source path was not specified.")

    @staticmethod
    def write_to_file(text, path):
        path = os.path.expanduser(path)
        filename_pair = os.path.splitext(path)

        if not filename_pair[0] and not filename_pair[1]:
            raise ValueError("invalid path specified")

        with open(path, 'w+') as f:
            f.write(text)

    @staticmethod
    def write_to_stdout(text):
        # write output to stdout
        print(text)
