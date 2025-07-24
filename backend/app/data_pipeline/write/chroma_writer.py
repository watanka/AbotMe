import json
from typing import List

from app.llm.vector_store.base import VectorStore
from app.database.uow import UnitOfWork
from app.database.models.chunk_group import ChunkGroup
from app.database.models.chunk import Chunk
from .base import VectorStoreWriter


class ChromaVectorStoreWriter(VectorStoreWriter):
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def save(self, docs: List[str]):
        """단순 텍스트 chunk(str)만 저장"""
        for i, doc in enumerate(docs):
            self.vector_store.add_documents(documents=[doc], ids=[f"resume-{i}"])


class ChromaMetadataVectorStoreWriter(VectorStoreWriter):
    def __init__(self, vector_store: VectorStore, uow: UnitOfWork):
        self.vector_store = vector_store
        self.uow = uow

    def save(self, docs: List[dict], resume_id: str):
        """메타정보(dict) 포함 chunk 저장"""
        for chunk_list in docs:
            chunk_group = ChunkGroup()
            self.uow.chunk_groups.add(chunk_group)
            self.uow.session.flush()  # chunk_group.id 확보

            chunk_text = '\t'.join([chunk.get("chunk_text", "") for chunk in chunk_list])
            self.vector_store.add_documents(
                documents=[chunk_text],
                metadatas=[{"chunk_group_id": str(chunk_group.id)}],
                ids=[f"resume-{chunk_group.id}"],
            )

            for chunk in chunk_list:
                chunk = Chunk(
                    label_id=chunk.get("label"),
                    resume_id=resume_id,
                    text=chunk.get("chunk_text"),
                    x0=chunk.get("x0"),
                    x1=chunk.get("x1"),
                    top=chunk.get("top"),
                    bottom=chunk.get("bottom"),
                    page_id=chunk.get("page_id"),
                    chunk_group_id=chunk_group.id,
                )
                self.uow.chunks.upsert_by_label_id(chunk)
            self.uow.commit()
