import abc


class BaseEmbeddings(abc.ABC):

    # def __init__(
    #         self,
    #         **kwargs
    # ):
    #     super().__init__(**kwargs)

    @abc.abstractmethod
    async def embed(self, **kwargs) -> None:
        pass
