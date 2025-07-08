"""
LangChain 기반 Gemini LLMClient 구현
"""

import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from .base import LLMClient


class LangChainGeminiClient(LLMClient):
    def __init__(self, model: str = "gemini-2.0-flash-exp"):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY 환경변수가 설정되어 있지 않습니다.")
        self.llm = init_chat_model(model, model_provider="google_genai")

    def generate(self, prompt: str, **kwargs) -> str:
        callback = kwargs.get("callback", None)
        for chunk in self.llm.stream(
            prompt, config={"callbacks": [callback] if callback else []}
        ):
            yield chunk.content
