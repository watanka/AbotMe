import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Resume(Base):
    __tablename__ = "resumes"
    resume_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pdf_url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
