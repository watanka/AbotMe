import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Answer(Base):
    __tablename__ = "answers"
    answer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(
        UUID(as_uuid=True), ForeignKey("questions.question_id"), nullable=False
    )
    answer = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
