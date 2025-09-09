import os
from pathlib import Path

from app.data_pipeline.chunk.base import Chunker
from app.data_pipeline.extract.base import Extractor
from app.data_pipeline.write.base import StoreWriter
from app.data_pipeline.write.neo4j_writer import GraphDBWriter
from app.models.schemas import ResumeResponse
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langfuse.langchain import CallbackHandler

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


def run_resume_pipeline(
    resume: ResumeResponse,
    extractor: Extractor,
    chunker: Chunker,
    writer: StoreWriter,
):
    print("[INFO] 업로드한 이력서 분석 시작")
    langfuse_callback_handler = CallbackHandler()

    assert Path(resume.pdf_url).exists(), f"PDF not found: {resume.pdf_url}"
    extracted = extractor.extract(resume.pdf_url)
    print("[INFO] PDF 텍스트 추출 완료")
    chunks = chunker.chunk(extracted, callback=langfuse_callback_handler)
    print("chunk", chunks)
    print(f"[INFO] {len(chunks)}개 청크로 분할 완료")

    # Writer는 텍스트 청크 리스트를 저장한다고 가정
    writer.save(chunks)
    print(f"[INFO] 청크 저장 완료")


def run_graph_resume_pipeline(
    resume: ResumeResponse,
    extractor: Extractor,
    chunker: Chunker,
    graph_db_writer: GraphDBWriter,
):
    print("[INFO] 업로드한 이력서 분석 시작")
    extracted = extractor.extract(resume.pdf_url)
    print("[INFO] PDF 텍스트 추출 완료")
    print("[INFO] 메타정보 RDB 저장")
    langfuse_callback_handler = CallbackHandler()

    chunks = chunker.chunk(extracted, callback=langfuse_callback_handler)
    print("chunks: ", chunks)
    # 단순 텍스트 청커 출력 가정
    processed_text = "\n".join(chunks)  # type: ignore[arg-type]

    graph_documents_filtered = graph_db_writer.convert_text_to_graph(processed_text)
    graph_db_writer.save(graph_documents_filtered)
    print("[INFO] GraphDB 저장 완료")


if __name__ == "__main__":
    RESUME_PATH = os.environ.get("RESUME_PATH", "resume.pdf")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
