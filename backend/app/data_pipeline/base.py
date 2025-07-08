from abc import ABC, abstractmethod
from typing import List

class Extractor(ABC):
    @abstractmethod
    def extract(self, source: str) -> str:
        pass

class Chunker(ABC):
    @abstractmethod
    def chunk(self, text: str) -> List[str]:
        pass

class VectorStoreSaver(ABC):
    @abstractmethod
    def save(self, docs: List[str]):
        pass
