"""
LLMClient 추상화 (Base)
"""

from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    다양한 LLM(대형 언어 모델) 제공자를 추상화하는 인터페이스
    """

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        주어진 프롬프트에 대해 LLM의 응답을 반환합니다.
        :param prompt: 사용자 입력 또는 시스템 메시지
        :param kwargs: 추가 파라미터(옵션)
        :return: LLM의 응답 텍스트
        """
        pass
