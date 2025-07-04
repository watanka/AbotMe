from app.main import create_app
from fastapi.testclient import TestClient

app = create_app()
client = TestClient(app)


def test_get_faqs():
    response = client.get("/faq/")
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) > 0
    assert "question" in result[0]
    assert "answer" in result[0]
