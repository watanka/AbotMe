import sys
from unittest.mock import MagicMock
from dotenv import load_dotenv

load_dotenv()


def pytest_configure():
    # langfuse 모듈 및 하위 모듈 mock 처리
    mock_client = MagicMock()
    mock_client.get_prompt.return_value = "mocked_prompt"
    langfuse_mock = MagicMock(get_client=lambda: mock_client)
    sys.modules["langfuse"] = langfuse_mock

    # langfuse.langchain 서브모듈도 mock 처리
    langchain_mock = MagicMock()
    sys.modules["langfuse.langchain"] = langchain_mock
