import glob
import os
import sys
from unittest.mock import MagicMock

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def sample_pdf_paths():
    base_dir = os.path.join(os.path.dirname(__file__), "sample-pdf")
    pdf_files = glob.glob(os.path.join(base_dir, "*.pdf"))
    return pdf_files


def pytest_configure():
    # langfuse 모듈 및 하위 모듈 mock 처리
    mock_client = MagicMock()
    mock_client.get_prompt.return_value = "mocked_prompt"
    langfuse_mock = MagicMock(get_client=lambda: mock_client)
    sys.modules["langfuse"] = langfuse_mock

    # langfuse.langchain 서브모듈도 mock 처리
    langchain_mock = MagicMock()
    sys.modules["langfuse.langchain"] = langchain_mock
