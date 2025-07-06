from app.llm.llm_client import LangChainGeminiClient
from app.llm.rag_engine import RAGEngine
from app.llm.vector_store import ChromaVectorStore
from app.llm.vector_store.embedding import GeminiEmbeddingModel
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import get_chat_response
from fastapi import APIRouter
from typing import Optional

router = APIRouter()


@router.post("/", response_model=ChatResponse)
def chat(request: Optional[ChatRequest] = None):

    vector_store = ChromaVectorStore("./chroma_db", GeminiEmbeddingModel())

    # 범용 LLM이 절대 알 수 없는, 허구/비상식적 정보 샘플
    sample_docs = [
        "2023년 5월, 나는 판게아테크놀로지의 '초전도 바나나 생성기' 프로젝트에서 수석 바나나 엔지니어로 근무했다.",
        "내가 만든 언어 'Silverscript'는 오직 나와 인공지능만이 이해할 수 있는 유일한 프로그래밍 언어다.",
        "2022년, 'Quantum Kimchi Optimization' 논문으로 대한민국 가상김치학회에서 최우수상을 수상했다.",
    ]
    vector_store.add_documents(sample_docs)

    llm_client = LangChainGeminiClient()
    rag_engine = RAGEngine(vector_store, llm_client)
    response = get_chat_response(rag_engine, request)
    print(response.answer)
    return response
