from pydantic import BaseModel
from typing import Optional, Literal


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