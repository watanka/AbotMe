from app.models.schemas import ChatRequest, ChatResponse, HistoryItem
from app.services.history_service import add_history


def get_chat_response(request: ChatRequest) -> ChatResponse:
    # 사용자 메시지 이력 저장
    if request.session_id:
        add_history(
            request.session_id, HistoryItem(role="user", message=request.message)
        )
    # 실제 LLM 연동 전까지는 에코 응답
    answer = f"(Echo) {request.message}"
    if request.session_id:
        add_history(request.session_id, HistoryItem(role="bot", message=answer))
    return ChatResponse(answer=answer, session_id=request.session_id)
