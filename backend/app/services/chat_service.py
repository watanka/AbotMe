import json

from app.database.uow import UnitOfWork
from app.llm.graph_rag_engine import GraphRAGEngine
from app.llm.rag_engine import RAGEngine
from app.llm.user_message_handler import UserMessageHandler
from app.models.schemas import ChatRequest, ChatResponse, HistoryItem
from app.services.history_service import add_history, get_history
from fastapi.responses import StreamingResponse
from langfuse.langchain import CallbackHandler

langfuse_callback_handler = CallbackHandler()


def get_chat_response(
    rag_engine: RAGEngine,
    request: ChatRequest,
) -> ChatResponse:
    """
    사용자의 메시지를 받아 Gemini LLM을 통해 응답을 생성합니다.
    예외 발생 시 에러 메시지를 반환합니다.
    """
    if request.session_id:
        add_history(
            request.session_id, HistoryItem(role="user", message=request.message)
        )
    try:
        answer = rag_engine.generate_answer(
            request.message, callback=langfuse_callback_handler
        )
    except Exception as e:
        answer = f"[ERROR: LLM 호출 실패] {str(e)}"
    if request.session_id:
        add_history(request.session_id, HistoryItem(role="bot", message=answer))
    return ChatResponse(answer=answer, session_id=request.session_id)


def stream_chat_response(
    rag_engine: RAGEngine,
    request: ChatRequest,
):
    """
    사용자의 메시지를 받아 Gemini LLM을 통해 응답을 스트림으로 생성합니다.
    """

    def answer_stream():
        if request.session_id:
            add_history(
                request.session_id, HistoryItem(role="user", message=request.message)
            )
        try:
            answer = []

            # metadata 정보 기반 분기: 사용자 답변 and PDF 하이라이트
            context_docs_metadata = rag_engine.retrieve_context(request.message)
            context = "\n".join(
                [
                    getattr(doc, "page_content", str(doc))
                    for doc in context_docs_metadata
                ]
            )
            answer = []
            chat_history = get_history(request.session_id)
            for chunk in rag_engine.generate_answer(
                request.message,
                context,
                chat_history,
                callback=langfuse_callback_handler,
            ):
                answer.append(chunk)
                yield json.dumps({"type": "chunk", "data": chunk})
            if request.session_id:
                add_history(
                    request.session_id, HistoryItem(role="bot", message="".join(answer))
                )
        except Exception as e:
            import traceback

            traceback.print_exc()
            yield json.dumps(
                {"type": "error", "data": f"[ERROR: LLM 호출 실패] {str(e)}"}
            )

    return StreamingResponse(answer_stream(), media_type="text/plain")


def stream_graph_chat_response(
    graph_rag_engine: GraphRAGEngine,
    request: ChatRequest,
):
    """
    사용자의 메시지를 받아 Gemini LLM을 통해 응답을 스트림으로 생성합니다.
    """

    def answer_stream():
        if request.session_id:
            add_history(
                request.session_id, HistoryItem(role="user", message=request.message)
            )
        try:
            answer = []
            # text2cypher
            context = graph_rag_engine.retrieve_context(request.message)
            for chunk in graph_rag_engine.generate_answer(
                request.message,
                context,
                chat_history=get_history(request.session_id),
                callback=langfuse_callback_handler,
            ):
                answer.append(chunk)
                yield json.dumps({"type": "chunk", "data": chunk})
        except Exception as e:
            import traceback

            traceback.print_exc()
            yield json.dumps(
                {"type": "error", "data": f"[ERROR: LLM 호출 실패] {str(e)}"}
            )
        if request.session_id:
            # 비동기 호출
            add_history(
                request.session_id, HistoryItem(role="bot", message="".join(answer))
            )

    return StreamingResponse(answer_stream(), media_type="text/plain")
