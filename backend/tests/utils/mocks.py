from unittest.mock import MagicMock

from app.llm.llm_client.base import LLMClient
from app.llm.rag_engine import RAGEngine
from app.llm.vector_store.chroma import ChromaVectorStore


class UserMessageMetadata:
    def __init__(self, content: str):
        self.content = content
        self.metadata = {}


class MockLLMClient(LLMClient):
    def generate(self, prompt: str, **kwargs) -> str:
        response = "MOCK LLM RESPONSE"
        for chunk in response:
            yield chunk


class MockVectorStore(ChromaVectorStore):
    def __init__(self):
        self.db = MagicMock()
        mock_doc = MagicMock(return_value=["mock context"])
        mock_doc.page_content = "MOCK LLM RESPONSE"
        mock_doc.metadata = {"page": 1, "info": "mock"}
        self.db.similarity_search = MagicMock(return_value=[mock_doc])

    def add_documents(self, documents, metadatas=None):

        return []

    def similarity_search(self, query: str, k: int = 5):
        mock_doc = MagicMock()
        mock_doc.page_content = "MOCK LLM RESPONSE"
        mock_doc.metadata = {"page": 1, "info": "mock"}
        return [mock_doc]

    def query_with_metadata(self, msg: dict, k: int = 5):
        mock_doc = MagicMock()
        mock_doc.page_content = "MOCK LLM RESPONSE"
        mock_doc.metadata = {
            "page_id": 1,
            "label_id": "mock",
            "x0": 1,
            "top": 1,
            "x1": 1,
            "bottom": 1,
            "tags": ["#sample"],
            "name": "subsample",
        }
        return [mock_doc]


class UserMockMessageHandler:
    def __init__(self):
        self.llm = MagicMock()
        self.prompt = MagicMock()

    def process(self, message: str):
        return UserMessageMetadata(content=message)


def get_mock_llm_client():
    return MockLLMClient()


def get_mock_user_message_handler():
    return UserMockMessageHandler()


def get_mock_vector_store():
    return MockVectorStore()


def get_mock_rag_engine(
    vector_store=get_mock_vector_store(), llm_client=get_mock_llm_client()
):
    mock_prompt = "사용자 질문에 답변하기 위한 RAG 프롬프트"
    return RAGEngine(vector_store, llm_client, prompt=mock_prompt)
