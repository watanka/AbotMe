"""
Embedding 추상화 (Base)
"""

from abc import ABC, ABCMeta, abstractmethod
from typing import Any


class EmbeddingModel(ABC, metaclass=ABCMeta):
    @abstractmethod
    def get_model(self) -> Any:
        """
        임베딩 모델 객체 반환 (벡터스토어에서 embedding_function으로 사용)
        """
        pass
