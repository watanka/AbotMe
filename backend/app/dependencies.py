from fastapi import Depends
from app.llm.llm_client.langchain_gemini import LangChainGeminiClient
from app.llm.vector_store import VectorStore
from app.llm.llm_client import LLMClient
from app.llm.rag_engine import RAGEngine
from app.llm.vector_store.chroma import ChromaVectorStore
from app.llm.vector_store.embedding import GeminiEmbeddingModel


def get_vector_store() -> VectorStore:
    vector_store = ChromaVectorStore("./chroma_db", GeminiEmbeddingModel())
    sample_docs = [
        "2023년 5월, 나는 판게아테크놀로지의 '초전도 바나나 생성기' 프로젝트에서 수석 바나나 엔지니어로 근무했다.",
        "내가 만든 언어 'Silverscript'는 오직 나와 인공지능만이 이해할 수 있는 유일한 프로그래밍 언어다.",
        "2022년, 'Quantum Kimchi Optimization' 논문으로 대한민국 가상김치학회에서 최우수상을 수상했다.",
    ]
    vector_store.add_documents(sample_docs)
    return vector_store

def get_llm_client() -> LLMClient:
    return LangChainGeminiClient()

def get_rag_engine(
    vector_store: VectorStore = Depends(get_vector_store),
    llm_client: LLMClient = Depends(get_llm_client),
) -> RAGEngine:
    return RAGEngine(vector_store, llm_client)
