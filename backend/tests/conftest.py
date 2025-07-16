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
    pass