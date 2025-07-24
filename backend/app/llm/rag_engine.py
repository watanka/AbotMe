"""
RAGEngine: LLM + VectorStore 결합 추상화
- SOLID/단일 책임/확장성 원칙 반영
- 테스트/사용 예시는 별도 스크립트에서 import하여 실행
"""

from typing import Callable, Optional

from app.llm.llm_client import LLMClient
from app.llm.vector_store import VectorStore
from langchain_core.prompts import ChatPromptTemplate


class RAGEngine:
    """
    LLM과 벡터스토어(VectorStore)를 결합한 RAG 엔진
    """

    def __init__(self, vector_store: VectorStore, prompt: ChatPromptTemplate, llm):
        self.vector_store = vector_store
        self.prompt = prompt
        self.llm = llm

    def retrieve_context(self, msg: dict, k: int = 5):
        return self.vector_store.query_with_metadata(msg, k=k)

    def generate_answer(self, msg: str, context, callback: Optional[Callable] = None):
        filled_prompt = self.prompt.format_messages(msg=msg, context=context)

        for chunk in self.llm.stream(
            filled_prompt, config={"callbacks": [callback] if callback else []}
        ):
            yield chunk.content
