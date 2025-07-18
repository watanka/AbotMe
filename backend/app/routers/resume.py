from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
import uuid

# 기존 서비스 함수 재사용
from app.services.data_service import run_resume_pipeline
from app.dependencies import get_llm

router = APIRouter()

# In-memory storage 예시 (실 서비스에서는 DB/파일시스템/벡터스토어 등으로 대체)
RESUME = {}


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
):
    global RESUME
    # 실제 구현 시: 파일 저장, id/토큰 생성, DB 저장 등
    # TODO: 파일 저장 경로 수정
    save_path = f"/home/silver/workspace/AbotMe/frontend/public/{name}_{file.filename}"
    with open(save_path, "wb") as f:
        f.write(file.file.read())
    # 벡터스토어 저장 (기존 파이프라인 활용)
    # run_resume_pipeline(save_path)
    RESUME = {
        "pdf_path": save_path,
        "questions": {},
        "answers": {},
        "name": name,
        "email": email,
    }
    public_url = f"/{name}_{file.filename}"
    run_resume_pipeline(llm, save_path)
    return {"public_url": public_url}


# 2. 이력서/질문/답변 데이터 조회 (공개)
@router.get("/")
def get_resume():
    if not RESUME:
        raise HTTPException(status_code=404, detail="존재하지 않는 이력서")

    return {
        "pdf_url": RESUME.get("pdf_path").split("/")[-1],  # /public 기준으로 변경
        "questions": RESUME.get("questions", []),
        "answers": RESUME.get("answers", {}),
        "name": RESUME.get("name"),
        "email": RESUME.get("email"),
    }


# 3. 질문 자동 생성 (edit_token 필요)


@router.post("/generate-questions")
def generate_questions():
    pdf_path = RESUME.get("pdf_path")
    if not pdf_path:
        raise HTTPException(status_code=400, detail="업로드된 이력서가 없습니다.")
    # TODO: LLM 기반 질문 생성 로직 (임시 예시)
    questions = [
        {str(uuid.uuid4()): "이 프로젝트에서 가장 어려웠던 점은?"},
        {str(uuid.uuid4()): "협업 경험을 구체적으로 설명해주세요."},
    ]
    RESUME["questions"] = questions
    return {"questions": questions}


@router.get("/questions/{question_id}")
def get_question(question_id: str):
    return RESUME.get("questions").get(question_id)


@router.get("/answers/{question_id}")
def get_answer(question_id: str):
    return RESUME.get("answers").get(question_id, "")


# 4. 답변 저장 (질문별 1대1, edit_token 필요)
@router.post("/questions/{question_id}/answer")
def save_answer(question_id: str, answer: str = Form(...)):
    if "questions" not in RESUME or not any(
        q.get(question_id) for q in RESUME["questions"]
    ):
        raise HTTPException(status_code=404, detail="존재하지 않는 질문")

    RESUME["answers"][question_id] = answer
    return {"success": True}
