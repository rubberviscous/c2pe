import os
from unittest import TestCase, mock

from c2pe.backends import LocalBackend, GoogleBackend
from c2pe.backends.local_backend import BackendError
from tests.mixins import BackendMixin


class TestLocalBackend(BackendMixin, TestCase):
    @property
    def output_path(self):
        filename_with_ext = os.path.basename(self.input_path)
        file_splitext = os.path.splitext(filename_with_ext)

        file_name = file_splitext[0]
        file_ext = file_splitext[1]

        path = os.path.dirname(self.input_path)
        _output_path = f'{path}/{file_name}_translated{file_ext}'
        return _output_path

    @staticmethod
    def _get_backend(**kwargs):
        text = kwargs.get("text", None)
        source_path = kwargs.get("source_path", None)
        backend = LocalBackend(data=text, source_path=source_path)
        return backend

    def test_save_to_file(self):
        output: str = self._get_translation()
        backend = self._get_backend(text=output, source_path=self.input_path)
        backend.save()
        self.assertTrue(os.path.exists(self.output_path))
        os.remove(self.output_path)

    def test_save_to_file_invalid_source_path(self):
        with self.assertRaises(BackendError):
            backend = self._get_backend()
            backend.save()


# @mock.patch('c2pe.backends.google_backend.build')
class TestGoogleBackend(BackendMixin, TestCase):

    @staticmethod
    def _get_backend(**kwargs):
        text = kwargs.get("text", None)
        source_path = kwargs.get("source_path", None)
        backend = GoogleBackend(data=text, source_path=source_path)
        return backend

    def test_save_to_file(self, *mocks):
        # path = "files/test.txt"
        # output_path = "files/test_translated.txt"
        output: str = self._get_translation()
        backend = self._get_backend(text=output, source_path=self.input_path)
        backend.save()
        # self.assertTrue(os.path.exists(output_path))
        # os.remove(output_path)
