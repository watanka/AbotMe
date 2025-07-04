from app.llm.rag_engine import RAGEngine
from app.models.schemas import ChatRequest, ChatResponse, HistoryItem
from app.services.history_service import add_history


def get_chat_response(rag_engine: RAGEngine, request: ChatRequest) -> ChatResponse:
    """
    사용자의 메시지를 받아 Gemini LLM을 통해 응답을 생성합니다.
    예외 발생 시 에러 메시지를 반환합니다.
    """
    if request.session_id:
        add_history(
            request.session_id, HistoryItem(role="user", message=request.message)
        )
    try:
        answer = rag_engine.generate_answer(request.message)
    except Exception as e:
        answer = f"[ERROR: LLM 호출 실패] {str(e)}"
    if request.session_id:
        add_history(request.session_id, HistoryItem(role="bot", message=answer))
    return ChatResponse(answer=answer, session_id=request.session_id)
