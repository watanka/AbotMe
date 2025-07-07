from fastapi import APIRouter, Depends
from app.dependencies import get_rag_engine
from app.models.schemas import ChatRequest
from app.services.chat_service import stream_chat_response

router = APIRouter()


@router.post("/")
async def chat(request: ChatRequest, rag_engine=Depends(get_rag_engine)):
    return stream_chat_response(rag_engine, request)