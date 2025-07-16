from app.dependencies import get_rag_engine, get_user_message_handler
from app.llm.rag_engine import RAGEngine
from app.llm.user_message_handler import UserMessageHandler
from app.models.schemas import ChatRequest
from app.services.chat_service import stream_chat_response
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/")
async def chat(
    request: ChatRequest,
    user_message_handler: UserMessageHandler = Depends(get_user_message_handler),
    rag_engine: RAGEngine = Depends(get_rag_engine),
):
    return stream_chat_response(rag_engine, user_message_handler, request)
