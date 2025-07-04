"""
Google Vertex AI Embedding 구현 및 인증/셋팅
"""

import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from .base import EmbeddingModel

load_dotenv()


class GeminiEmbeddingModel(EmbeddingModel):
    def __init__(
        self,
        model_name: str = "models/embedding-001",
    ):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY 환경변수가 설정되어 있지 않습니다.")
        self.model_name = model_name

    def get_model(self):
        return GoogleGenerativeAIEmbeddings(model=self.model_name)
