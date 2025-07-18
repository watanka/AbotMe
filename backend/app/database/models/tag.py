import enum
import uuid

from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class TagCategory(enum.Enum):
    personal = "#personal"
    education = "#education"
    experience = "#experience"
    project = "#project"
    tech_stack = "#tech_stack"
    achievement = "#achievement"
    certificate = "#certificate"
    award = "#award"
    timeline = "#timeline"
    summary = "#summary"


class Tag(Base):
    __tablename__ = "tags"
    tag_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.question_id"))
    tag_name = Column(Enum(TagCategory, name="tag_category"), nullable=False)
