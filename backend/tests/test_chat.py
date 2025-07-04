from app.main import create_app
from fastapi.testclient import TestClient

app = create_app()
client = TestClient(app)


def test_chat_echo():
    data = {"message": "안녕!", "session_id": "test-session"}
    response = client.post("/chat/", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["session_id"] == "test-session"
