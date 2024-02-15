import abc


class BaseConnectors(abc.ABC):

    @abc.abstractmethod
    async def connect(self, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    async def download(self, *args, **kwargs):
        pass


class BaseSqlConnector(abc.ABC):

    @abc.abstractmethod
    async def connect(self):
        pass

    @abc.abstractmethod
    async def execute(self, *args, **kwargs):
        pass
