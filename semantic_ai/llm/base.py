import abc
from abc import ABC


class BaseLLM(ABC):

    @abc.abstractmethod
    async def llm_model(self, *args, **kwargs):
        pass
