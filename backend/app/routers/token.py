from fastapi import APIRouter
from app.models.schemas import TokenVerifyRequest, TokenVerifyResponse
import os

router = APIRouter()

# 환경변수에서 SECRET_TOKEN을 읽고, 없으면 기본값 사용
SECRET_TOKEN = os.environ.get("SECRET_TOKEN", "SECRET_TOKEN")


@router.post("/verify", response_model=TokenVerifyResponse)
def verify_token(payload: TokenVerifyRequest):
    return {"success": payload.token == SECRET_TOKEN}
