from typing import Self
from abc import ABC, abstractmethod
import logging


class AbstractLogger(ABC):
    @abstractmethod
    def debug(self, message: str) -> None:
        pass

    @abstractmethod
    def info(self, message: str) -> None:
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        pass


class DefaultLogger(AbstractLogger):
    __instance = None
    __initialized = False

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = AbstractLogger.__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if self.__initialized:
            return
        self.__initialized = True

        self.logger = logging.getLogger("lrc-dl")
        self.logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)
