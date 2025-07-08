import os
from pathlib import Path

from app.data_pipeline.pdf_resume import (
    AgenticTextChunker,
    ChromaVectorStoreSaver,
    PDFResumeExtractor,
)
from app.data_pipeline.prompts import resume_prompt
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
vector_store_dir = os.getenv("VECTOR_STORE_DIR", "/vector-db")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")


def run_resume_pipeline(
    pdf_path: str, persist_dir: str = vector_store_dir, collection_name: str = "resume"
):
    extractor = PDFResumeExtractor()
    chunker = AgenticTextChunker(template=resume_prompt, llm=llm)
    saver = ChromaVectorStoreSaver(
        persist_dir=persist_dir, collection_name=collection_name
    )

    assert Path(pdf_path).exists(), f"PDF not found: {pdf_path}"
    text = extractor.extract(pdf_path)
    print("[INFO] PDF 텍스트 추출 완료")
    chunks = chunker.chunk(text)
    print(f"[INFO] {len(chunks)}개 청크로 분할 완료")
    saver.save(chunks)
    print(f"[INFO] ChromaDB에 저장 완료: {persist_dir}/{collection_name}")


if __name__ == "__main__":
    RESUME_PATH = os.environ.get("RESUME_PATH", "resume.pdf")
    run_resume_pipeline(RESUME_PATH)
