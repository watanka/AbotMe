from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter

from .base import Chunker


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
