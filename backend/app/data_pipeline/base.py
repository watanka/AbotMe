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
    def save(self, docs: List[dict]):
        """
        각 doc은 최소한 다음 필드를 포함해야 함:
        - chunk_text: str
        - label_id: List[str] 또는 str
        - tags: List[str]
        - name: str
        (추가 메타정보도 포함 가능)
        """
        pass
