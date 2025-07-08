from fastapi import APIRouter, UploadFile, File
from app.services.data_service import run_resume_pipeline
from app.data_pipeline.utils import save_binary_to_file
import os

router = APIRouter()


@router.post("/pdf")
def pdf_to_vector_store(pdf: UploadFile = File(...)):
    """
    PDF 파일을 벡터 스토어에 업데이트합니다.
    """
    # 업로드 파일을 임시 경로에 저장
    save_path = f"/tmp/{pdf.filename}"
    save_binary_to_file(pdf.file, save_path)
    # 벡터스토어 파이프라인 실행
    run_resume_pipeline(save_path)
    # 필요하다면 파일 삭제
    os.remove(save_path)
    return {"message": "PDF가 벡터스토어에 저장되었습니다."}
