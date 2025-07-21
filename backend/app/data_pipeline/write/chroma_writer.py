import json
from typing import List

from app.llm.vector_store.base import VectorStore

from .base import VectorStoreWriter


class ChromaVectorStoreWriter(VectorStoreWriter):
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def save(self, docs: List[str]):
        """단순 텍스트 chunk(str)만 저장"""
        for i, doc in enumerate(docs):
            self.vector_store.add_documents(documents=[doc], ids=[f"resume-{i}"])


class ChromaMetadataVectorStoreWriter(VectorStoreWriter):
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def save(self, docs: List[dict]):
        """메타정보(dict) 포함 chunk 저장"""
        for _, doc in enumerate(docs):
            tags = json.dumps(doc.get("tags", []))  # list -> str
            name = doc.get("name", "")
            x0 = doc.get("x0")
            top = doc.get("top")
            x1 = doc.get("x1")
            bottom = doc.get("bottom")
            label_id = doc.get("label_id", "")
            self.vector_store.add_documents(
                documents=[doc.get("chunk_text", "")],
                metadatas=[
                    {
                        "tags": tags,
                        "name": name,
                        "x0": x0,
                        "top": top,
                        "x1": x1,
                        "bottom": bottom,
                        "page_id": doc.get("page_id"),
                    }
                ],
                ids=[f"resume-{label_id}"],
            )
