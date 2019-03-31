from abc import ABC, abstractmethod


class BaseBackend(ABC):

    def __init__(self, text: str, *args, **kwargs):
        pass

    @abstractmethod
    def save(self, txt: str):
        pass
