import os
from pathlib import Path

from app.data_pipeline.chunk.agentic_chunker import AgenticMetadataChunker
from app.data_pipeline.extract import PDFResumeMetadataExtractor
from app.data_pipeline.prompts import resume_prompt
from app.data_pipeline.write.chroma_writer import ChromaMetadataVectorStoreWriter
from app.data_pipeline.write.neo4j_writer import GraphDBWriter
from app.database.models.chunk import Chunk
from app.database.models.resume import Resume
from app.database.uow import UnitOfWork
from app.llm.vector_store.chroma import ChromaVectorStore
from app.llm.vector_store.embedding import GeminiEmbeddingModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_neo4j import Neo4jGraph
from langfuse.langchain import CallbackHandler

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
vector_store_dir = os.getenv("VECTOR_STORE_DIR", "/vector-db")


def run_resume_pipeline(
    llm,
    resume: Resume,
    uow: UnitOfWork,
    persist_dir: str = vector_store_dir,
    collection_name: str = "resume",
):
    print("[INFO] 업로드한 이력서 분석 시작")
    extractor = PDFResumeMetadataExtractor()

    langfuse_callback_handler = CallbackHandler()
    chunker = AgenticMetadataChunker(prompt_template=resume_prompt, llm=llm)
    vector_store = ChromaVectorStore(persist_dir, GeminiEmbeddingModel())
    writer = ChromaMetadataVectorStoreWriter(vector_store, uow)

    assert Path(resume.pdf_url).exists(), f"PDF not found: {resume.pdf_url}"
    meta_list = extractor.extract(resume.pdf_url)
    print("[INFO] PDF 텍스트 추출 완료")
    chunks = chunker.chunk(meta_list, callback=langfuse_callback_handler)
    print("chunk", chunks)
    print(f"[INFO] {len(chunks)}개 청크로 분할 완료")

    writer.save(
        chunks,
    )
    print(f"[INFO] ChromaDB에 저장 완료: {persist_dir}/{collection_name}")


def run_graph_resume_pipeline(
    resume_id,
    llm,
    pdf_url: str,
    graph_db: Neo4jGraph,
    uow: UnitOfWork,
):
    print("[INFO] 업로드한 이력서 분석 시작")
    extractor = PDFResumeMetadataExtractor()
    agentic_chunker = AgenticMetadataChunker(prompt_template=resume_prompt, llm=llm)
    meta_dict = extractor.extract(pdf_url)
    print("[INFO] PDF 텍스트 추출 완료")
    with uow:
        for _, meta in meta_dict.items():
            uow.chunks.add(
                Chunk(
                    label_id=meta["label_id"],
                    resume_id=resume_id,
                    text=meta["text"],
                    x0=meta["x0"],
                    x1=meta["x1"],
                    top=meta["top"],
                    bottom=meta["bottom"],
                    page_id=meta["page_id"],
                )
            )
    print("[INFO] 메타정보 RDB 저장")
    graph_db_writer = GraphDBWriter(graph_db, llm)
    langfuse_callback_handler = CallbackHandler()

    chunks = agentic_chunker.chunk(meta_dict, callback=langfuse_callback_handler)
    # postprocess chunks
    # llm 결과로 text를 리턴하면 비용이 증가하기 때문에, meta_list에서 text 불러옴.
    processed_chunks = str(
        [
            (
                ",".join(c.labels),
                " ".join([meta_dict[label]["text"] for label in c.labels]),
            )
            for c in chunks
        ]
    )

    graph_documents_filtered = graph_db_writer.convert_text_to_graph(processed_chunks)
    graph_db_writer.save(graph_documents_filtered)
    print("[INFO] GraphDB 저장 완료")


if __name__ == "__main__":
    RESUME_PATH = os.environ.get("RESUME_PATH", "resume.pdf")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
