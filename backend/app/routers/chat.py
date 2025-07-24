from app.dependencies import get_rag_engine, get_user_message_handler
from app.llm.rag_engine import RAGEngine
from app.llm.user_message_handler import UserMessageHandler
from app.models.schemas import ChatRequest
from app.services.chat_service import stream_chat_response
from fastapi import APIRouter, Depends
from app.llm.graph_rag_engine import GraphRAGEngine
from app.dependencies import get_graph_rag_engine, get_uow
from app.services.chat_service import stream_graph_chat_response
from app.database.uow import UnitOfWork

router = APIRouter()


@router.post("/")
async def chat(
    request: ChatRequest,
    user_message_handler: UserMessageHandler = Depends(get_user_message_handler),
    rag_engine: RAGEngine = Depends(get_rag_engine),
    uow: UnitOfWork = Depends(get_uow),
):
    return stream_chat_response(rag_engine, user_message_handler, uow, request)


@router.post("/graph")
async def graph_chat(
    request: ChatRequest,
    graph_rag_engine: GraphRAGEngine = Depends(get_graph_rag_engine),
):
    return stream_graph_chat_response(graph_rag_engine, request)