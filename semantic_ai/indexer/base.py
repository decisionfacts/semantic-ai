from abc import ABCMeta, abstractmethod


class BaseIndexer(metaclass=ABCMeta):

    @abstractmethod
    def create(self, *args, **kwargs):
        pass
