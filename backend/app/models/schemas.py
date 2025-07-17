from typing import List, Literal, Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    session_id: Optional[str] = None


class FAQ(BaseModel):
    question: str
    answer: str


class HistoryItem(BaseModel):
    role: Literal["user", "bot"]
    message: str


class TokenVerifyRequest(BaseModel):
    token: str


class TokenVerifyResponse(BaseModel):
    success: bool


class QnAQuestion(BaseModel):
    """
    이력서 QnA 질문 데이터 모델
    """

    question_id: str | None = None
    label_id: str
    question: str


class QnAQuestionList(BaseModel):
    root: List[QnAQuestion]


class QnAAnswer(BaseModel):
    """
    이력서 QnA 답변 데이터 모델
    """

    question_id: str
    answer: str
    created_at: Optional[str] = None
