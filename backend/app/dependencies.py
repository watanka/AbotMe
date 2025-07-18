import os

from app.data_pipeline.prompts import user_query_prompt
from app.llm.llm_client import LLMClient
from app.llm.llm_client.langchain_deepseek import LangChainDeepseekClient
from app.llm.rag_engine import RAGEngine
from app.llm.user_message_handler import UserMessageHandler
from app.llm.vector_store import VectorStore
from app.llm.vector_store.chroma import ChromaVectorStore
from app.llm.vector_store.embedding import GeminiEmbeddingModel
from dotenv import load_dotenv
from fastapi import Depends
from langchain_openai import ChatOpenAI

load_dotenv()
vector_store_dir = os.getenv("VECTOR_STORE_DIR", "./vector-db")


def get_llm():
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE_URL"),
        model_name="deepseek/deepseek-chat:free",
    )

    # llm = LangChainGeminiClient().llm
    return llm


def get_vector_store() -> VectorStore:
    vector_store = ChromaVectorStore(vector_store_dir, GeminiEmbeddingModel())
    return vector_store


def get_llm_client() -> LLMClient:
    return LangChainDeepseekClient()


def get_rag_engine(
    vector_store: VectorStore = Depends(get_vector_store),
    llm_client: LLMClient = Depends(get_llm_client),
) -> RAGEngine:
    return RAGEngine(vector_store, llm_client)


def get_user_message_handler(
    llm_client: LLMClient = Depends(get_llm),
) -> UserMessageHandler:
    return UserMessageHandler(llm_client, user_query_prompt)
