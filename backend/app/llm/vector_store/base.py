"""
벡터 스토어 추상화 (Base)
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional


class VectorStore(ABC):
    """
    벡터 스토어 추상 인터페이스.
    다양한 벡터 DB(Chroma, FAISS, Pinecone 등)를 교체 가능하도록 추상화.
    """

    @abstractmethod
    def add_documents(
        self, documents: List[str], metadatas: Optional[List[dict]] = None
    ) -> List[str]:
        """
        텍스트 문서 리스트를 벡터로 임베딩 후 저장.
        :param documents: 임베딩할 텍스트 리스트
        :param metadatas: 각 문서에 대한 메타데이터 리스트
        :return: 저장된 문서의 ID 리스트
        """
        pass

    @abstractmethod
    def similarity_search(self, query: str, k: int = 5) -> List[Any]:
        """
        쿼리와 유사한 문서 k개 반환
        :param query: 검색 쿼리(텍스트)
        :param k: 반환할 문서 수
        :return: 유사 문서 리스트
        """
        pass
