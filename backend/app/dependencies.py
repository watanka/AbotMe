import os

from app.data_pipeline.extract.base import Extractor
from app.data_pipeline.extract.pdf_resume_metadata_extractor import (
    PDFResumeMetadataExtractor,
)
from langchain_neo4j import Neo4jGraph
from app.data_pipeline.prompts import chat_prompt, qna_prompt, user_query_prompt, text2cypher_prompt
from app.database.uow import UnitOfWork
from app.llm.rag_engine import RAGEngine
from app.llm.user_message_handler import UserMessageHandler
from app.llm.vector_store import VectorStore
from app.llm.vector_store.chroma import ChromaVectorStore
from app.llm.vector_store.embedding import GeminiEmbeddingModel
from app.services.qna_service import QnAService
from dotenv import load_dotenv
from fastapi import Depends
from langchain_google_genai import ChatGoogleGenerativeAI
from app.llm.graph_rag_engine import GraphRAGEngine

load_dotenv()
vector_store_dir = os.getenv("VECTOR_STORE_DIR", "./vector-db")


def get_uow() -> UnitOfWork:
    return UnitOfWork()


def get_llm():
    # llm = ChatOpenAI(
    #     openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    #     openai_api_base=os.getenv("OPENROUTER_BASE_URL"),
    #     model_name="deepseek/deepseek-r1-0528-qwen3-8b:free",
    # )
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API_KEY")
    )

    # llm = LangChainGeminiClient().llm
    return llm


def get_extractor():
    return PDFResumeMetadataExtractor()


def get_vector_store() -> VectorStore:
    vector_store = ChromaVectorStore(vector_store_dir, GeminiEmbeddingModel())
    return vector_store


def get_graph_db():

    return Neo4jGraph(refresh_schema=False)


def get_rag_engine(
    vector_store: VectorStore = Depends(get_vector_store),
    llm=Depends(get_llm),
) -> RAGEngine:
    return RAGEngine(vector_store, chat_prompt, llm)


def get_graph_rag_engine(
    graph_db: Neo4jGraph = Depends(get_graph_db),
    llm=Depends(get_llm),
) -> GraphRAGEngine:
    return GraphRAGEngine(graph_db=graph_db, text2cypher_prompt=text2cypher_prompt, qa_prompt=chat_prompt, llm=llm)


def get_user_message_handler(
    llm=Depends(get_llm),
) -> UserMessageHandler:
    return UserMessageHandler(llm, user_query_prompt)


def get_qna_service(
    extractor: Extractor = Depends(get_extractor),
    vector_store: VectorStore = Depends(get_vector_store),
    llm=Depends(get_llm),
    uow: UnitOfWork = Depends(get_uow),
) -> QnAService:
    return QnAService(extractor, vector_store, qna_prompt, uow, llm)