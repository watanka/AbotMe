from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import get_chat_response

router = APIRouter()


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = get_chat_response(request)
    return response
