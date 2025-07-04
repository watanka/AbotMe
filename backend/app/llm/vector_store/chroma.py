"""
ChromaDB + VertexAI 임베딩 기반 벡터 스토어 구현체
"""

from typing import Any, List, Optional

from langchain_community.vectorstores import Chroma

from .base import VectorStore
from .embedding import EmbeddingModel


class ChromaVectorStore(VectorStore):
    def __init__(self, persist_directory: str, embedding_engine: EmbeddingModel):
        self.persist_directory = persist_directory
        self.embeddings = embedding_engine.get_model()
        self.db = Chroma(
            embedding_function=self.embeddings, persist_directory=self.persist_directory
        )

    def add_documents(
        self, documents: List[str], metadatas: Optional[List[dict]] = None
    ) -> List[str]:
        return self.db.add_texts(documents, metadatas=metadatas)

    def similarity_search(self, query: str, k: int = 5) -> List[Any]:
        return self.db.similarity_search(query, k=k)
