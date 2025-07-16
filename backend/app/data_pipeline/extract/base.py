from abc import ABC, abstractmethod
from typing import Any

class Extractor(ABC):
    @abstractmethod
    def extract(self, source: str) -> Any:
        pass
