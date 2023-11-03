from abc import ABCMeta, abstractmethod


class BaseIndexer(metaclass=ABCMeta):

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass

    @abstractmethod
    async def index(self, *args, **kwargs):
        pass
