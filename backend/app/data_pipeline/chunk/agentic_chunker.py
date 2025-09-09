from typing import Callable, Dict, List, Optional

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from enum import Enum
from .base import Chunker


class ChunkType(Enum):
    personal_info = "personal_info"
    education = "education"
    experience = "experience"
    skills = "skills"
    certification = "certification"

class ResumeChunk(BaseModel):
    content: str
    chunk_type: ChunkType
    metadata: Dict
    search_summary: str
      
class ResumeChunkList(BaseModel):
    chunks: List[ResumeChunk]


class AgenticTextChunker(Chunker):

    def __init__(self, template, llm):
        self.template = template
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=ResumeChunkList)

    def chunk(
        self, parsed_text: str, callback: Optional[Callable] = None
    ) -> List[Dict]:
        
        # 3. LLM 호출
        runnable = self.template | self.llm | self.parser
        if callback:
            llm_output = runnable.invoke(
                {"input": parsed_text}, config={"callbacks": [callback]}
            )
        else:
            llm_output = runnable.invoke({"input": parsed_text})

        return llm_output.chunks
