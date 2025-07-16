"""
RAGEngine: LLM + VectorStore 결합 추상화
- SOLID/단일 책임/확장성 원칙 반영
- 테스트/사용 예시는 별도 스크립트에서 import하여 실행
"""

from typing import Callable, Optional

from app.llm.llm_client import LLMClient
from app.llm.vector_store import VectorStore


class RAGEngine:
    """
    LLM과 벡터스토어(VectorStore)를 결합한 RAG 엔진
    """

    def __init__(self, vector_store: VectorStore, llm_client: LLMClient):
        self.vector_store = vector_store
        self.llm_client = llm_client

    def retrieve_context(self, msg: dict, k: int = 5):
        return self.vector_store.query_with_metadata(msg, k=k)

    def generate_answer(self, msg: str, context, callback: Optional[Callable] = None):
        prompt = f"""
당신은 이력서를 보고 질문하는 사용자들에게 답변을 해줘야해요. 아래는 사용자의 질문과 참고할 정보입니다. 이 참고 정보는 벡터스토어에서 꺼내온 거예요.
사용자들은 당신이 이력서에 대한 모든 정보를 다 알고 있다고 가정해요. 그러니까 사용자에게 이력서 정보를 알려주는 역할이예요. 다음 참고 정보를 기반으로 사용자에게 정보를 알려주세요. 
참고 정보를 있는 그대로 말하는 것보다는, 사용자의 질문에 적절하게 답하는 게 중요해요.
[참고 정보]
{context}
[질문]
{msg}
위 정보를 우선적으로 참고해서 답변해 주세요.
만약 정보가 부족하거나 직접적으로 답이 없으면, 당신이 알고 있는 일반적인 지식이나 상식을 바탕으로 합리적으로 추론해서 답변해 주세요.
여러 정보가 있다면 핵심만 자연스럽게 통합해서 설명해 주세요.
친근하고 부드러운 말투로, 상대방이 이해하기 쉽게 답변해 주세요.
답변이 추정이나 일반 상식에 근거한 경우, 그 점도 함께 밝혀 주세요.
만약 답변하기 어렵거나 모르는 정보라면, 모른다고 해도 괜찮아요.
참고 정보를 기반으로 꼬리 질문을 추천해주어도 좋아요.
"""
        for chunk in self.llm_client.generate(prompt, callback=callback):
            yield chunk
