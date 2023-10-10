import abc


class BaseConnectors(abc.ABC):

    @abc.abstractmethod
    def connect(self, *args, **kwargs) -> None:
        pass
