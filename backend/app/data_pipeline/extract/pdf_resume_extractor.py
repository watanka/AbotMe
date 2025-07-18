from PyPDF2 import PdfReader

from .base import Extractor


class PDFResumeExtractor(Extractor):
    def extract(self, pdf_url: str) -> str:
        reader = PdfReader(pdf_url)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
