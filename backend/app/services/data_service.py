import os
from pathlib import Path

from app.data_pipeline.chunk.agentic_chunker import AgenticMetadataChunker
from app.data_pipeline.extract import PDFResumeMetadataExtractor
from app.data_pipeline.prompts import resume_prompt
from app.data_pipeline.write.chroma_writer import ChromaMetadataVectorStoreWriter
from app.llm.vector_store.chroma import ChromaVectorStore
from app.llm.vector_store.embedding import GeminiEmbeddingModel
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langfuse.langchain import CallbackHandler

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
vector_store_dir = os.getenv("VECTOR_STORE_DIR", "/vector-db")


def run_resume_pipeline(
    llm,
    pdf_path: str,
    persist_dir: str = vector_store_dir,
    collection_name: str = "resume",
):
    print("[INFO] 업로드한 이력서 분석 시작")
    extractor = PDFResumeMetadataExtractor()

    langfuse_callback_handler = CallbackHandler()
    chunker = AgenticMetadataChunker(prompt_template=resume_prompt, llm=llm)
    vector_store = ChromaVectorStore(persist_dir, GeminiEmbeddingModel())
    writer = ChromaMetadataVectorStoreWriter(vector_store)

    assert Path(pdf_path).exists(), f"PDF not found: {pdf_path}"
    meta_list = extractor.extract(pdf_path)
    print("[INFO] PDF 텍스트 추출 완료")
    chunks = chunker.chunk(meta_list, callback=langfuse_callback_handler)
    print(f"[INFO] {len(chunks)}개 청크로 분할 완료")

    writer.save(chunks)
    print(f"[INFO] ChromaDB에 저장 완료: {persist_dir}/{collection_name}")


if __name__ == "__main__":
    RESUME_PATH = os.environ.get("RESUME_PATH", "resume.pdf")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
    run_resume_pipeline(llm, RESUME_PATH)
