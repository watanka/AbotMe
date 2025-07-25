import uuid

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base


class Chunk(Base):
    __tablename__ = "chunks"
    label_id = Column(String, primary_key=True, nullable=False)
    resume_id = Column(
        UUID(as_uuid=True), ForeignKey("resumes.resume_id"), nullable=False
    )
    text = Column(String, nullable=False)
    x0 = Column(Float)
    x1 = Column(Float)
    top = Column(Float)
    bottom = Column(Float)
    page_id = Column(Float)
    chunk_group_id = Column(UUID(as_uuid=True), ForeignKey("chunk_groups.id"))
    chunk_group = relationship("ChunkGroup", back_populates="chunks")
