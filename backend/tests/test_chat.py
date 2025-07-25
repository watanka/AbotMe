import json

from app.dependencies import (
    get_llm,
    get_rag_engine,
    get_uow,
    get_user_message_handler,
    get_vector_store,
)
from app.main import create_app
from fastapi.testclient import TestClient
from tests.utils.mocks import (
    get_mock_llm,
    get_mock_rag_engine,
    get_mock_uow,
    get_mock_user_message_handler,
    get_mock_vector_store,
)

app = create_app()
client = TestClient(app)


def test_chat_streaming():
    app.dependency_overrides[get_rag_engine] = get_mock_rag_engine
    app.dependency_overrides[get_uow] = get_mock_uow
    app.dependency_overrides[get_vector_store] = get_mock_vector_store
    app.dependency_overrides[get_llm] = get_mock_llm
    app.dependency_overrides[get_user_message_handler] = get_mock_user_message_handler
    import re

    data = {"message": "스트리밍 테스트", "session_id": "stream-session"}
    with client.stream("POST", "/chat/", json=data) as response:
        assert response.status_code == 200
        chunk_text = ""
        metadata_obj = None
        buffer = ""

        def extract_json_objects(buf):
            objs = []
            last_end = 0
            for match in re.finditer(r"({.*?})(?={|$)", buf):
                try:
                    obj = json.loads(match.group(1))
                    objs.append((obj, match.end()))
                except Exception:
                    pass
            return objs

        for chunk in response.iter_text():
            if chunk:
                buffer += chunk
                objs = extract_json_objects(buffer)
                last_parsed_end = 0
                for obj, end_pos in objs:
                    last_parsed_end = max(last_parsed_end, end_pos)
                    if obj.get("type") == "chunk":
                        chunk_text += obj.get("data", "")
                    elif obj.get("type") == "metadata":
                        metadata_obj = obj.get("data")
                # 이미 파싱한 부분 제거 (마지막 '}' 이후부터 남김)
                buffer = buffer[last_parsed_end:]
        assert "MOCK LLM RESPONSE" in chunk_text
        # assert metadata_obj is not None
        # assert metadata_obj and "page_id" in metadata_obj[0]

    app.dependency_overrides = {}
