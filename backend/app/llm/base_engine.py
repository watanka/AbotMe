from abc import ABC, abstractmethod
from typing import Callable, Optional


class BaseEngine(ABC):
    @abstractmethod
    def retrieve_context(self, msg: str, callback: Optional[Callable] = None):
        pass

    @abstractmethod
    def generate_answer(
        self, msg: str, context: dict, callback: Optional[Callable] = None
    ):
        pass
