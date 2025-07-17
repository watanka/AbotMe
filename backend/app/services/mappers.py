import uuid
from datetime import datetime

from app.database.models.answer import Answer
from app.database.models.question import Question
from app.database.models.resume import Resume
from app.models.schemas import QnAAnswer, QnAQuestion, ResumeResponse

# ResumeResponse <-> Resume


def convert_resume_dbmodel_to_pydantic(resume: Resume) -> ResumeResponse:
    return ResumeResponse(
        resume_id=str(resume.resume_id),
        pdf_url=resume.pdf_url,
        name=resume.name,
        email=resume.email,
        created_at=resume.created_at.isoformat() if resume.created_at else None,
    )


# QnAQuestion <-> Question


def convert_question_pydantic_to_dbmodel(q: QnAQuestion, resume_id: str) -> Question:
    return Question(
        question_id=uuid.UUID(q.question_id),
        resume_id=resume_id,
        label_id=q.label_id,
        question=q.question,
    )


def convert_question_dbmodel_to_pydantic(q: Question) -> QnAQuestion:
    return QnAQuestion(
        question_id=str(q.question_id),
        label_id=q.label_id,
        question=q.question,
    )


# QnAAnswer <-> Answer


def convert_answer_pydantic_to_dbmodel(a: QnAAnswer) -> Answer:
    return Answer(
        question_id=uuid.UUID(a.question_id),
        answer=a.answer,
        created_at=(
            datetime.fromisoformat(a.created_at) if a.created_at else datetime.utcnow()
        ),
    )


def convert_answer_dbmodel_to_pydantic(a: Answer) -> QnAAnswer:
    return QnAAnswer(
        question_id=str(a.question_id),
        answer=a.answer,
        created_at=a.created_at.isoformat() if a.created_at else None,
    )
