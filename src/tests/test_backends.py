import os
from unittest import TestCase

from c2pe.backends import LocalBackend
from c2pe.backends.local_backend import BackendError


class TestLocalBackend(TestCase):
    @staticmethod
    def _get_backend(**kwargs):
        text = kwargs.get("text", None)
        source_path = kwargs.get("source_path", None)
        backend = LocalBackend(text=text, source_path=source_path)
        return backend

    def test_save_to_file(self):
        path = "files/test.txt"
        output_path = "files/test_translated.txt"
        backend = self._get_backend(text="text", source_path=path)
        backend.save()
        self.assertTrue(os.path.exists(output_path))
        os.remove(output_path)

    def test_save_to_file_invalid_source_path(self):
        backend = self._get_backend(text="text", source_path=None)
        with self.assertRaises(BackendError):
            backend = self._get_backend()
            backend.save()
