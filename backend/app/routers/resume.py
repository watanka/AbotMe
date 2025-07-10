from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import uuid
# 기존 서비스 함수 재사용
from app.services.data_service import run_resume_pipeline
# from app.llm.rag_engine import ... # 필요시 추가

router = APIRouter()

# In-memory storage 예시 (실 서비스에서는 DB/파일시스템/벡터스토어 등으로 대체)
RESUMES = {}  # resume_id: {pdf_path, edit_token, questions, answers}

# Helper: edit_token 검증
def verify_edit_token(edit_token: str):
    if not edit_token:
        raise HTTPException(status_code=403, detail="권한 없음 또는 edit_token 불일치")

# 1. 이력서 업로드 (최초 등록)
@router.post("/")
def upload_resume(file: UploadFile = File(...), name: str = Form(...), email: str = Form(...)):
    # 실제 구현 시: 파일 저장, id/토큰 생성, DB 저장 등
    import uuid
    edit_token = str(uuid.uuid4())
    save_path = f"/tmp/{name}_{file.filename}"
    with open(save_path, "wb") as f:
        f.write(file.file.read())
    # 벡터스토어 저장 (기존 파이프라인 활용)
    run_resume_pipeline(save_path)
    RESUMES[edit_token] = {
        'pdf_path': save_path,
        'edit_token': edit_token,
        'questions': [],
        'answers': [],
        'name': name,
        'email': email
    }
    public_url = f"/resume"
    return {"edit_token": edit_token, "public_url": public_url}


# 2. 이력서/질문/답변 데이터 조회 (공개)
@router.get("/")
def get_resume():
    resume = RESUMES.get(edit_token)
    if not resume:
        raise HTTPException(status_code=404, detail="존재하지 않는 이력서")
    return {
        "resume_pdf_url": resume['pdf_path'],
        "questions": resume.get('questions', []),
        "answers": resume.get('answers', {}),
        "name": resume.get('name'),
        "email": resume.get('email')
    }


# 3. 질문 자동 생성 (edit_token 필요)


@router.post("/generate-questions")
def generate_questions(edit_token: str = Form(...)):
    verify_edit_token(edit_token)
    pdf_path = RESUMES[edit_token].get('pdf_path')
    if not pdf_path:
        raise HTTPException(status_code=400, detail="업로드된 이력서가 없습니다.")
    # TODO: LLM 기반 질문 생성 로직 (임시 예시)
    questions = [
        {str(uuid.uuid4()): "이 프로젝트에서 가장 어려웠던 점은?"},
        {str(uuid.uuid4()): "협업 경험을 구체적으로 설명해주세요."}
    ]
    RESUMES[edit_token]['questions'] = questions
    RESUMES[edit_token]['answers'] = {}  # question_id: answer
    return {"questions": questions}

@router.get("/questions/{question_id}")
def get_question(question_id: str, edit_token: str = Form(...)):
    verify_edit_token(edit_token)
    return RESUMES[edit_token].get('questions').get(question_id)



# 4. 답변 저장 (질문별 1대1, edit_token 필요)
@router.post("/questions/{question_id}/answer")
def save_answer(question_id: str, edit_token: str = Form(...), answer: str = Form(...)):
    verify_edit_token(edit_token)
    if 'questions' not in RESUMES[edit_token] or not any(q.get(question_id) for q in RESUMES[edit_token]['questions']):
        raise HTTPException(status_code=404, detail="존재하지 않는 질문")
    if 'answers' not in RESUMES[edit_token]:
        RESUMES[edit_token]['answers'] = {}
    RESUMES[edit_token]['answers'][question_id] = answer
    return {"success": True}

