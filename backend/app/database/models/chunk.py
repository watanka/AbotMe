import uuid

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class ResumeChunk(Base):
    __tablename__ = "resume_chunks"
    chunk_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(
        UUID(as_uuid=True), ForeignKey("resumes.resume_id"), nullable=False
    )
    label_id = Column(String, nullable=False)
    text = Column(String, nullable=False)
    x0 = Column(Float)
    x1 = Column(Float)
    top = Column(Float)
    bottom = Column(Float)
