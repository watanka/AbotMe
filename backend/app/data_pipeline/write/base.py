from abc import ABC, abstractmethod
from typing import List


class StoreWriter(ABC):
    @abstractmethod
    def save(self, docs: List[dict]):
        """
        각 doc은 최소한 다음 필드를 포함해야 함:
        chunk_text: str
        """
        pass
