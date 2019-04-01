import os
from typing import List, Tuple

from abc import ABC, abstractmethod


class BaseBackend(ABC):

    def __init__(self, data: List[Tuple], *args, **kwargs):
        self.data = data
        self.input_path = kwargs.get("source_path", None)
        if self.input_path:
            self.filename = self.get_filename(path=self.input_path)

    @abstractmethod
    def save(self, txt: str):
        pass

    @abstractmethod
    def output(self) -> str:
        pass

    @staticmethod
    def get_filename(path: object) -> Tuple[str]:
        """
        Given a path, will return the file name as tuple
        e.g ('name', 'txt')
        :param path:
        """
        filename_with_ext = os.path.basename(path)
        file_splitext = os.path.splitext(filename_with_ext)
        return file_splitext

