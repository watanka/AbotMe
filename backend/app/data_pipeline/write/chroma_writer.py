from typing import List
import uuid
from app.llm.vector_store.base import VectorStore
from app.database.uow import UnitOfWork
from app.database.models.chunk_group import ChunkGroup
from app.database.models.chunk import Chunk
from .base import StoreWriter
from app.data_pipeline.chunk.agentic_chunker import ResumeChunk
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


class ChromaVectorStoreWriter(StoreWriter):
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def save(self, chunks: List[ResumeChunk]):
        """단순 텍스트 chunk(str)만 저장"""
        for i, chunk in enumerate(chunks):
            metadata = {
                "chunk_type": chunk.chunk_type.value,
                "search_summary": chunk.search_summary,
            }
            metadata.update(chunk.metadata)

            document = Document(page_content=chunk.content, metadata=metadata)
            self.vector_store.add_documents([document])


class ChromaMetadataVectorStoreWriter(StoreWriter):
    def __init__(self, vector_store: VectorStore, uow: UnitOfWork):
        self.vector_store = vector_store
        self.uow = uow

    def save(self, chunks: List[dict], meta_dict: List[dict], resume_id: uuid.UUID):
        """메타정보(dict) 포함 chunk 저장"""
        with self.uow:
            for chunk in chunks:
                for label in chunk.labels:
                    # 텍스트 추출
                    text = " ".join([meta_dict[label]["text"]])

                    self.vector_store.add_texts(
                        texts=[text],
                    )

            for _, meta in meta_dict.items():
                chunk = Chunk(
                    label_id=meta["label_id"],
                    resume_id=resume_id,
                    text=meta.get("text"),
                    x0=meta.get("x0"),
                    x1=meta.get("x1"),
                    top=meta.get("top"),
                    bottom=meta.get("bottom"),
                    page_id=meta.get("page_id"),
                )
                self.uow.chunks.upsert_by_label_id(chunk)
            self.uow.commit()
