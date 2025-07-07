"""
RAGEngine: LLM + VectorStore 결합 추상화
- SOLID/단일 책임/확장성 원칙 반영
- 테스트/사용 예시는 별도 스크립트에서 import하여 실행
"""

from app.llm.llm_client import LLMClient
from app.llm.vector_store import VectorStore


class RAGEngine:
    """
    LLM과 벡터스토어(VectorStore)를 결합한 RAG 엔진
    """

    def __init__(self, vector_store: VectorStore, llm_client: LLMClient):
        self.vector_store = vector_store
        self.llm_client = llm_client

    def retrieve_context(self, query: str, k: int = 5):
        return self.vector_store.similarity_search(query, k=k)

    def generate_answer(self, query: str, k: int = 5):
        context_docs = self.retrieve_context(query, k)
        context = "\n".join(
            [getattr(doc, "page_content", str(doc)) for doc in context_docs]
        )
        prompt = f"다음 정보를 참고해서 답변해줘.\n정보:\n{context}\n\n질문: {query}"
        for chunk in self.llm_client.generate(prompt):
            yield chunk
