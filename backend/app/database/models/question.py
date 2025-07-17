import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Question(Base):
    __tablename__ = "questions"
    question_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(
        UUID(as_uuid=True), ForeignKey("resumes.resume_id"), nullable=False
    )
    label_id = Column(String)
    question = Column(String, nullable=False)
