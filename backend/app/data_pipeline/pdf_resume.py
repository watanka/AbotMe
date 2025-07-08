from typing import List, Optional
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings
from app.data_pipeline.base import Extractor, Chunker, VectorStoreSaver
from langfuse.langchain import CallbackHandler


class PDFResumeExtractor(Extractor):
    def extract(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text


class SimpleTextChunker(Chunker):
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str) -> List[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n", ".", " "],
        )
        return splitter.split_text(text)


class AgenticTextChunker(Chunker):
    def __init__(self, template: str, llm):
        self.prompt_template = template
        self.llm = llm

    def chunk(self, text: str, callback: Optional[CallbackHandler] = None) -> List[str]:
        runnable = self.prompt_template | self.llm
        runnable_output = runnable.invoke(
            {"input": text}, config={"callbacks": [callback]}
        ).content
        chunks = [chunk.strip() for chunk in runnable_output.split("-")]
        return chunks


class ChromaVectorStoreSaver(VectorStoreSaver):
    def __init__(
        self, persist_dir: str = "chroma_data", collection_name: str = "resume"
    ):
        self.persist_dir = persist_dir
        self.collection_name = collection_name

    def save(self, docs: List[str]):
        client = chromadb.PersistentClient(
            path=self.persist_dir, settings=Settings(allow_reset=True)
        )
        collection = client.get_or_create_collection(self.collection_name)
        for i, doc in enumerate(docs):
            collection.upsert(documents=[doc], ids=[f"resume-{i}"])
