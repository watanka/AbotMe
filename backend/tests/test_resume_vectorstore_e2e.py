import os

from app.data_pipeline.chunk.agentic_chunker import AgenticMetadataChunker
from app.data_pipeline.extract import PDFResumeMetadataExtractor
from app.data_pipeline.prompts import resume_prompt
from app.data_pipeline.write.chroma_writer import ChromaMetadataVectorStoreWriter
from app.llm.vector_store.chroma import ChromaVectorStore
from app.llm.vector_store.embedding.gemini import GeminiEmbeddingModel
from langchain_openai import ChatOpenAI

from backend.app.services.data_service import run_resume_pipeline


def test_resume_e2e_vectorstore_qa(sample_pdf_paths):
    """
    PDF → meta_list → chunk(dict) → ChromaMetadataVectorStoreWriter 저장 →
    (질문→답변) end-to-end 테스트
    """

    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE_URL"),
        model_name="deepseek/deepseek-chat:free",
    )
    vectorstore_dir = "./chroma_test_store"
    vector_store = ChromaVectorStore(vectorstore_dir, GeminiEmbeddingModel())
    for pdf_path in sample_pdf_paths:
        run_resume_pipeline(llm, pdf_path, vectorstore_dir)
        break  # 하나만 수행
    # 벡터스토어로부터 QA
    questions = [
        "재직한 회사들을 전부 다 알려줘",
        "개발자로써 일을 하기 시작한 건 언제부터야?",
        "수상내역은 어떤 게 있어?",
        "기술 스택은 어떻게 구성되어있어?",
        "문제를 해결해본 경험이 있어?",
    ]
    for q in questions:
        docs = vector_store.similarity_search(q, k=3)
        print(f"[질문] {q}")
        for doc in docs:
            print(f"[답변 chunk] {doc.page_content}")
        assert len(docs) > 0
