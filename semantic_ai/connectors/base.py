import abc


class BaseConnectors(abc.ABC):

    @abc.abstractmethod
    async def connect(self, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    async def download(self, *args, **kwargs):
        pass
