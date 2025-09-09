"""
ChromaDB + VertexAI 임베딩 기반 벡터 스토어 구현체
"""

from typing import Any, List

from langchain_chroma import Chroma
from langchain_core.documents import Document

from .base import VectorStore
from .embedding import EmbeddingModel


class ChromaVectorStore(VectorStore):
    def __init__(self, persist_directory: str, embedding_engine: EmbeddingModel):
        self.persist_directory = persist_directory
        self.embeddings = embedding_engine.get_model()
        self.db = Chroma(
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name="resume",
        )

    def add_texts(self, texts: List[str], **kwargs) -> List[str]:
        results = self.db.add_texts(texts, **kwargs)
        return results

    def add_documents(self, documents: List[Document], **kwargs) -> List[str]:
        results = self.db.add_documents(documents, **kwargs)
        return results

    def search(self, query: str, k: int = 3, filter_dict: dict = None) -> List[Any]:
        retriever = self.db.as_retriever(
            search_type="mmr", search_kwargs={"k": k, "fetch_k": k * 2}
        )
        return retriever.invoke(query, filter=filter_dict)

    def similarity_search(
        self, query: str, k: int = 5, filter_dict: dict = None
    ) -> List[Any]:
        return self.db.similarity_search(query, k=k, filter=filter_dict)

    def query_with_metadata(self, msg: dict, k: int = 5) -> List[Any]:
        filter_dict = self._metadata_filter(msg.additional_kwargs)
        return self.db.similarity_search(query=msg.content, k=k, filter=filter_dict)

    def _metadata_filter(self, metadata: dict) -> dict:
        tags = metadata.get("tags", [])
        name = metadata.get("name", "")
        filters = []
        if tags:
            filters.append({"tags": {"$in": tags}})
        if name:
            filters.append({"name": name})
        filter_dict = (
            {"$or": filters} if len(filters) > 1 else (filters[0] if filters else None)
        )
        return filter_dict
