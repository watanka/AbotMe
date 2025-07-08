"""
RAGEngine: LLM + VectorStore 결합 추상화
- SOLID/단일 책임/확장성 원칙 반영
- 테스트/사용 예시는 별도 스크립트에서 import하여 실행
"""

from app.llm.llm_client import LLMClient
from app.llm.vector_store import VectorStore
from langfuse.langchain import CallbackHandler
from typing import Optional


class RAGEngine:
    """
    LLM과 벡터스토어(VectorStore)를 결합한 RAG 엔진
    """

    def __init__(self, vector_store: VectorStore, llm_client: LLMClient):
        self.vector_store = vector_store
        self.llm_client = llm_client

    def retrieve_context(self, query: str, k: int = 5):
        return self.vector_store.similarity_search(query, k=k)

    def generate_answer(self, query: str, k: int = 5, callback: Optional[CallbackHandler] = None):
        context_docs = self.retrieve_context(query, k)
        context = "\n".join(
            [getattr(doc, "page_content", str(doc)) for doc in context_docs]
        )
        prompt = f"""
        아래는 사용자의 질문과 참고할 정보 목록입니다.
[참고 정보]
{context}
[질문]
{query}
위 정보를 우선적으로 참고해서 답변해 주세요.
만약 정보가 부족하거나 직접적으로 답이 없으면, 당신이 알고 있는 일반적인 지식이나 상식을 바탕으로 합리적으로 추론해서 답변해 주세요.
여러 정보가 있다면 핵심만 자연스럽게 통합해서 설명해 주세요.
친근하고 부드러운 말투로, 상대방이 이해하기 쉽게 답변해 주세요.
답변이 추정이나 일반 상식에 근거한 경우, 그 점도 함께 밝혀 주세요.
만약 답변하기 어렵거나 모르는 정보라면, 모른다고 해도 괜찮아요.
"""
        for chunk in self.llm_client.generate(prompt, callback=callback):
            yield chunk
