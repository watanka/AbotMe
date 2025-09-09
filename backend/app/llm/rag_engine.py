"""
RAGEngine: LLM + VectorStore 결합 추상화
- SOLID/단일 책임/확장성 원칙 반영
- 테스트/사용 예시는 별도 스크립트에서 import하여 실행
"""

from typing import Callable, List, Optional

from app.llm.base_engine import BaseEngine
from app.llm.vector_store import VectorStore
from app.services.history_service import HistoryItem
from langchain_core.prompts import ChatPromptTemplate


class RAGEngine(BaseEngine):
    """
    LLM과 벡터스토어(VectorStore)를 결합한 RAG 엔진
    """

    def __init__(self, vector_store: VectorStore, prompt: ChatPromptTemplate, llm):
        self.vector_store = vector_store
        self.prompt = prompt
        self.llm = llm

    def retrieve_context(self, msg: dict, k: int = 5, filter_dict: dict = None):
        return self.vector_store.search(msg, k=k, filter_dict=filter_dict)

    def generate_answer(
        self,
        question: str,
        context: str,
        chat_history: List[HistoryItem] = [],
        callback: Optional[Callable] = None,
    ):
        filled_prompt = self.prompt.format_messages(
            question=question,
            context=context,
            chat_history="\n-".join([c.format() for c in chat_history]),
        )

        for chunk in self.llm.stream(
            filled_prompt, config={"callbacks": [callback] if callback else []}
        ):
            if hasattr(chunk, "content"):
                yield chunk.content
            else:
                yield str(chunk)
