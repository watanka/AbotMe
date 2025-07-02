from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_echo():
    data = {"message": "안녕!", "session_id": "test-session"}
    response = client.post("/chat/", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["answer"].startswith("(Echo)")
    assert result["session_id"] == "test-session"
