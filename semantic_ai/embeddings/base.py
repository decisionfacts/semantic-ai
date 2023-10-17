import abc


class BaseEmbeddings(abc.ABC):

    @abc.abstractmethod
    async def embed(self, **kwargs) -> None:
        pass
