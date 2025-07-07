from app.llm.llm_client.base import LLMClient
from app.llm.vector_store.chroma import ChromaVectorStore
from app.llm.rag_engine import RAGEngine


class MockLLMClient(LLMClient):
    def generate(self, prompt: str, **kwargs) -> str:
        response = "MOCK LLM RESPONSE: " + prompt
        for chunk in response:
            yield chunk


class MockVectorStore(ChromaVectorStore):
    def __init__(self):
        pass

    def add_documents(self, documents, metadatas=None):

        return []

    def similarity_search(self, query: str, k: int = 5):

        return ["mock context"]


def get_mock_llm_client():
    return MockLLMClient()


def get_mock_vector_store():
    return MockVectorStore()


def get_mock_rag_engine(
    vector_store=get_mock_vector_store(), llm_client=get_mock_llm_client()
):
    return RAGEngine(vector_store, llm_client)