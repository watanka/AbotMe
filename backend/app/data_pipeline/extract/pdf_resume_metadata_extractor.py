from typing import Dict, List

import pdfplumber

from .base import Extractor


class PDFResumeMetadataExtractor(Extractor):
    def extract(self, pdf_path: str) -> List[Dict]:
        """
        PDF에서 각 단어별로 page_id, label_id, text, bbox, has_space(띄어쓰기 포함 여부) 정보를 추출해 리스트로 반환
        """
        results = {}
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                words = page.extract_words(
                    x_tolerance=1, y_tolerance=1, keep_blank_chars=True
                )
                for idx, w in enumerate(words, 1):
                    text = w["text"].strip()
                    label_id = f"{page_num}-{idx}"
                    results[label_id] = {
                        "page_id": page_num,
                        "label_id": label_id,
                        "text": text,
                        "bbox": [w["x0"], w["top"], w["x1"], w["bottom"]],
                        # TODO: 좌표는 상대좌표 0 - 1 range로 변경 필요
                    }
        return results
