from app.models.schemas import ChatRequest, ChatResponse


def get_chat_response(request: ChatRequest) -> ChatResponse:
    # 실제 LLM 연동 전까지는 에코 응답
    return ChatResponse(
        answer=f"(Echo) {request.message}", session_id=request.session_id
    )
