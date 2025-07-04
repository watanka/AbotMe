from app.main import create_app
from fastapi.testclient import TestClient

app = create_app()
client = TestClient(app)

SESSION_ID = "test-session-history-test"


def test_history_accumulation():
    # 1. 첫 메시지 전송
    data1 = {"message": "안녕!", "session_id": SESSION_ID}
    client.post("/chat/", json=data1)

    # 2. 두 번째 메시지 전송
    data2 = {"message": "뭐해?", "session_id": SESSION_ID}
    client.post("/chat/", json=data2)

    # 3. 이력 조회
    response = client.get(f"/history/{SESSION_ID}")
    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)
    assert len(history) == 4  # user, bot, user, bot
    assert history[0]["role"] == "user"
    assert history[0]["message"] == "안녕!"
    assert history[1]["role"] == "bot"
    assert history[2]["role"] == "user"
    assert history[2]["message"] == "뭐해?"
    assert history[3]["role"] == "bot"
