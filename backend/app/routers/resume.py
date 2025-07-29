import os
import uuid
from datetime import datetime
from typing import List

from app.database.models.answer import Answer
from app.database.models.question import Question
from app.database.models.resume import Resume
from app.database.uow import UnitOfWork
from app.dependencies import get_graph_db, get_llm, get_qna_service, get_uow
from app.llm.graph_rag_engine import GraphRAGEngine
from app.services.data_service import run_graph_resume_pipeline, run_resume_pipeline

# 기존 서비스 함수 재사용
from app.services.mappers import (
    convert_answer_dbmodel_to_pydantic,
    convert_question_dbmodel_to_pydantic,
    convert_resume_dbmodel_to_pydantic,
)
from app.services.qna_service import QnAService
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from langchain_neo4j import Neo4jGraph

ASSETS_DIR = os.getenv("ASSETS_DIR", "./assets")
router = APIRouter()

# In-memory storage 예시 (실 서비스에서는 DB/파일시스템/벡터스토어 등으로 대체)


# Helper: edit_token 검증
def verify_edit_token(edit_token: str):
    if not edit_token:
        raise HTTPException(status_code=403, detail="권한 없음 또는 edit_token 불일치")


# 1. 이력서 업로드 (최초 등록)
@router.post("/")
def upload_resume(
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    llm=Depends(get_llm),
    graph_db: Neo4jGraph = Depends(get_graph_db),
    qna_service: QnAService = Depends(get_qna_service),
    uow: UnitOfWork = Depends(get_uow),
):

    # graph DB 초기화
    with graph_db._driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    print("[INFO] graph DB 초기화 완료")
    # rdb 초기화
    uow.drop_table()
    uow.create_table()
    print("[INFO] rdb 초기화 완료")

    # 실제 구현 시: 파일 저장, id/토큰 생성, DB 저장 등
    # TODO: 파일 저장 경로 수정
    save_path = f"{ASSETS_DIR}/{name}_{file.filename}"
    with open(save_path, "wb") as f:
        f.write(file.file.read())
    print("[INFO] pdf 파일 저장 완료")
    # 벡터스토어 저장 (기존 파이프라인 활용)
    # run_resume_pipeline(save_path)
    resume = Resume(
        resume_id=uuid.uuid4(),
        name=name,
        email=email,
        pdf_url=save_path,
    )
    resume_id = resume.resume_id
    with uow:
        uow.resumes.add(resume)
        uow.commit()
        # questions = qna_service.generate_questions(resume)
    print("[INFO] 질문 생성 완료")

    # TODO: 비동기, 모듈화

    run_graph_resume_pipeline(resume_id, llm, save_path, graph_db, uow)
    return {"public_url": os.path.basename(save_path)}


# 2. 이력서/질문/답변 데이터 조회 (공개)
@router.get("/")
def get_resume(uow: UnitOfWork = Depends(get_uow)):
    with uow:
        resumes: List[Resume] = uow.resumes.get_all()
        if not resumes:
            raise HTTPException(status_code=404, detail="존재하지 않는 이력서")
        # created_at 기준 최신
        latest_resume = max(resumes, key=lambda r: r.created_at)
        return convert_resume_dbmodel_to_pydantic(latest_resume)


# 3. 질문 자동 생성
@router.post("/generate-questions")
def generate_questions(
    qna_service: QnAService = Depends(get_qna_service),
    uow: UnitOfWork = Depends(get_uow),
):
    with uow:
        resumes: List[Resume] = uow.resumes.get_all()
        latest_resume = max(resumes, key=lambda r: r.created_at)
        if not latest_resume:
            raise HTTPException(status_code=400, detail="업로드된 이력서가 없습니다.")

        questions = qna_service.generate_questions(latest_resume)
    return {"questions": questions}


@router.get("/questions/")
def get_questions(uow: UnitOfWork = Depends(get_uow)):
    with uow:
        questions: List[Question] = uow.questions.get_all()
        return [convert_question_dbmodel_to_pydantic(q) for q in questions]


@router.get("/questions/{question_id}/")
def get_question(question_id: str, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        question: Question = uow.questions.get_by_id(question_id)
    return convert_question_dbmodel_to_pydantic(question)


@router.get("/answers/{question_id}/")
def get_answer(question_id: str, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        answer: Answer = uow.answers.get_by_id(question_id)
    return convert_answer_dbmodel_to_pydantic(answer)


# 4. 답변 저장 (질문별 1대1, edit_token 필요)
@router.post("/questions/{question_id}/answer/")
def save_answer(
    question_id: str,
    answer: str = Form(...),
    uow: UnitOfWork = Depends(get_uow),
    qna_service: QnAService = Depends(get_qna_service),
):
    with uow:
        question = uow.questions.get_by_id(question_id)
        if not question:
            raise HTTPException(status_code=404, detail="존재하지 않는 질문")
        uow.answers.add(
            Answer(
                question_id=question_id,
                answer=answer,
                created_at=datetime.utcnow(),
            )
        )
    qna_service.save_answer_to_vector_store(question_id)
    return {"success": True}
