from app.main import create_app
from fastapi.testclient import TestClient
from app.dependencies import get_llm_client, get_vector_store, get_rag_engine
from tests.utils.mocks import (
    get_mock_llm_client,
    get_mock_vector_store,
    get_mock_rag_engine,
)


def test_chat_streaming():
    app.dependency_overrides[get_rag_engine] = get_mock_rag_engine
    app.dependency_overrides[get_vector_store] = get_mock_vector_store
    app.dependency_overrides[get_llm_client] = get_mock_llm_client

    data = {"message": "스트리밍 테스트", "session_id": "stream-session"}
    with client.stream("POST", "/chat/", json=data) as response:
        assert response.status_code == 200
        chunks = []
        for chunk in response.iter_text():
            if chunk:
                chunks.append(chunk)
        full = "".join(chunks)
        assert "MOCK LLM RESPONSE" in full
        assert "스트리밍 테스트" in full

    app.dependency_overrides = {}
