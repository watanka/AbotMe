import os

import pytest
from app.main import create_app
from fastapi.testclient import TestClient


# 테스트 클라이언트 생성
@pytest.fixture
def client():
    os.environ["FRONTEND_URL"] = "https://watanka.github.io"
    app = create_app()
    return TestClient(app)


# CORS 테스트
def test_cors(client):
    # 실제 GET 요청 테스트
    response = client.get("/", headers={"Origin": "https://watanka.github.io"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert (
        response.headers["access-control-allow-origin"] == "https://watanka.github.io"
    )
    assert response.json() == {"message": "AbotMe 백엔드에 오신 것을 환영합니다!"}


# API 테스트
def test_cors_api_endpoint(client):
    response = client.options(
        "/chat/",
        headers={
            "Origin": "https://watanka.github.io",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
