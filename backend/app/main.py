from fastapi import FastAPI
from app.routers import chat

app = FastAPI()

app.include_router(chat.router, prefix="/chat", tags=["chat"])


@app.get("/")
def root():
    return {"message": "AbotMe 백엔드에 오신 것을 환영합니다!"}
