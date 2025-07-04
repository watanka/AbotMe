"""
Google Vertex AI Embedding 구현 및 인증/셋팅
"""

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from .base import EmbeddingModel


class GeminiEmbeddingModel(EmbeddingModel):
    def __init__(
        self,
        model_name: str = "models/embedding-001",
    ):
        self.model_name = model_name

    def get_model(self):
        return GoogleGenerativeAIEmbeddings(model=self.model_name)
