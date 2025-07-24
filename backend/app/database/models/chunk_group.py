import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base


class ChunkGroup(Base):
    __tablename__ = "chunk_groups"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # 관계: label_id로 연결
    chunks = relationship("Chunk", back_populates="chunk_group")
