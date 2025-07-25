from typing import Callable, Dict, List, Optional

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel

from .base import Chunker


class ResumeChunk(BaseModel):
    labels: List[str]
    tags: List[str]
    name: str


class ResumeChunkList(BaseModel):
    root: List[ResumeChunk]


class AgenticTextChunker(Chunker):
    def __init__(self, template: str, llm):
        self.prompt_template = template
        self.llm = llm

    def chunk(self, text: str, callback: Optional[Callable] = None) -> List[str]:
        runnable = self.prompt_template | self.llm
        if callback:
            runnable_output = runnable.invoke(
                {"input": text}, config={"callbacks": [callback]}
            ).content
        else:
            runnable_output = runnable.invoke({"input": text}).content
        chunks = [chunk.strip() for chunk in runnable_output.split("-")]
        return chunks


class AgenticMetadataChunker(Chunker):
    """
    LLM을 이용해 label_id 단위로 청킹 및 태깅을 수행하고, chunk별로 메타정보와 tags를 반환
    """

    def __init__(self, prompt_template, llm):
        self.prompt_template = prompt_template
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=ResumeChunkList)

    def chunk(
        self, meta_list: List[Dict], callback: Optional[Callable] = None
    ) -> List[Dict]:
        # 1. LLM 입력용 label_id + text 리스트 생성
        llm_input_lines = [
            f"[{label_id}] {metadata['text']}"
            for label_id, metadata in meta_list.items()
        ]
        llm_input = "\n".join(llm_input_lines)

        # 3. LLM 호출
        runnable = self.prompt_template | self.llm | self.parser
        if callback:
            llm_output = runnable.invoke(
                {"input": llm_input}, config={"callbacks": [callback]}
            )
        else:
            llm_output = runnable.invoke({"input": llm_input})

        result_chunks = [
            [
                {
                    "label": label,
                    "tags": t.tags,
                    "name": t.name,
                    "chunk_text": meta_list[label]["text"],
                    "x0": meta_list[label]["x0"],
                    "top": meta_list[label]["top"],
                    "x1": meta_list[label]["x1"],
                    "bottom": meta_list[label]["bottom"],
                    "page_id": meta_list[label]["page_id"],
                }
                for label in t.labels
            ]
            for t in llm_output.root
        ]
        return result_chunks
