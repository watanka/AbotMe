import os

from app.data_pipeline.extract.base import Extractor
from app.data_pipeline.extract import PDFResumeExtractor

from app.data_pipeline.chunk import AgenticTextChunker
from app.data_pipeline.prompts import (
    chat_prompt,
    qna_prompt,
    text2cypher_prompt,
    user_query_prompt,
    resume_prompt,
)
from app.database.uow import UnitOfWork
from app.llm.graph_rag_engine import GraphRAGEngine
from app.llm.rag_engine import RAGEngine
from app.llm.user_message_handler import UserMessageHandler
from app.llm.vector_store import VectorStore
from app.llm.vector_store.chroma import ChromaVectorStore
from app.llm.vector_store.embedding import GeminiEmbeddingModel
from app.data_pipeline.write.chroma_writer import ChromaVectorStoreWriter
from app.data_pipeline.write.neo4j_writer import GraphDBWriter
from app.services.qna_service import QnAService
from dotenv import load_dotenv
from fastapi import Depends
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_neo4j import Neo4jGraph

load_dotenv()
vector_store_dir = os.getenv("ASSETS_DIR", "./assets")


def get_uow() -> UnitOfWork:
    return UnitOfWork()


def get_llm():
    # llm = ChatOpenAI(
    #     openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    #     openai_api_base=os.getenv("OPENROUTER_BASE_URL"),
    #     model_name="deepseek/deepseek-r1-0528-qwen3-8b:free",
    # )
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY")
    )

    # llm = LangChainGeminiClient().llm
    return llm


def get_extractor() -> Extractor:
    # QnA 서비스 호환을 위해 label_id 기반 메타 추출기를 유지
    return PDFResumeMetadataExtractor()


def get_text_extractor() -> Extractor:
    # 파이프라인 전용: 텍스트만 추출
    return PDFResumeExtractor()


def get_resume_chunker(llm=Depends(get_llm)):
    # 이력서 청킹 프롬프트 사용
    return AgenticTextChunker(template=resume_prompt, llm=llm)


def get_vector_store() -> VectorStore:
    vector_store = ChromaVectorStore(vector_store_dir, GeminiEmbeddingModel())
    return vector_store


def get_vector_store_writer(vector_store: VectorStore = Depends(get_vector_store)):
    return ChromaVectorStoreWriter(vector_store)


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
    uow=Depends(get_uow),
) -> GraphRAGEngine:
    return GraphRAGEngine(
        graph_db=graph_db,
        text2cypher_prompt=text2cypher_prompt,
        qa_prompt=chat_prompt,
        llm=llm,
        uow=uow,
    )


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


def get_graph_db_writer(
    graph_db: Neo4jGraph = Depends(get_graph_db),
    llm=Depends(get_llm),
):
    return GraphDBWriter(graph_db, llm, GeminiEmbeddingModel().get_model())
