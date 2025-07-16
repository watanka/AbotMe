import pdfplumber
import pytest


@pytest.mark.skip
def test_pdfplumber_bbox_all(sample_pdf_paths):
    """
    sample_pdf_paths fixture를 사용하여 sample-pdf 폴더 내 모든 PDF 파일의
    각 단어별 bbox, page_id, label_id, text를 출력 및 구조 검증
    """
    for pdf_path in sample_pdf_paths:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                words = page.extract_words(
                    x_tolerance=1, y_tolerance=1, keep_blank_chars=True
                )
                for idx, w in enumerate(words, 1):
                    text = w["text"].strip()
                    label_id = f"{page_num}-{idx}"
                    has_space = " " in text

                    # 최소 구조 체크(assert)
                    assert isinstance(w["text"], str)
                    assert all(
                        isinstance(coord, (int, float))
                        for coord in [w["x0"], w["top"], w["x1"], w["bottom"]]
                    )
                    # 띄어쓰기 단위 분리 확인
                    if has_space:
                        print(
                            f"⚠️ 띄어쓰기가 포함된 단어 발견: '{w['text']}' (label_id={label_id})"
                        )

                        print(
                            {
                                "pdf_file": pdf_path,
                                "page_id": page_num,
                                "label_id": label_id,
                                "text": text,
                                "bbox": [w["x0"], w["top"], w["x1"], w["bottom"]],
                                "has_space": has_space,
                            }
                        )
