from fastapi import FastAPI
from backend.app.routers import chat, faq, history

app = FastAPI()

app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(faq.router, prefix="/faq", tags=["faq"])
app.include_router(history.router, prefix="/history", tags=["history"])


@app.get("/")
def root():
    return {"message": "AbotMe 백엔드에 오신 것을 환영합니다!"}
