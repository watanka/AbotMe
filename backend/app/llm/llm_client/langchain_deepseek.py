"""
LangChain 기반 Gemini LLMClient 구현
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from .base import LLMClient


class LangChainDeepseekClient(LLMClient):
    def __init__(self, model: str = "deepseek/deepseek-chat:free"):
        load_dotenv()
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY 환경변수가 설정되어 있지 않습니다.")
        self.llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE_URL"),
        model_name=model,
    )

    def generate(self, prompt: str, **kwargs) -> str:
        callback = kwargs.get("callback", None)
        for chunk in self.llm.stream(
            prompt, config={"callbacks": [callback] if callback else []}
        ):
            yield chunk.content
