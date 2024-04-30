import abc


class Compileable(abc.ABC):
    @abc.abstractmethod
    def compile(self, punctuation_mark: str) -> str:
        pass
