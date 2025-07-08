from fastapi import FastAPI

from app.middleware.cors import setup_cors
from app.routers import chat, faq, history, vector_store


def create_app():
    app = FastAPI()

    setup_cors(app)

    app.include_router(chat.router, prefix="/chat", tags=["chat"])
    app.include_router(faq.router, prefix="/faq", tags=["faq"])
    app.include_router(history.router, prefix="/history", tags=["history"])
    app.include_router(
        vector_store.router, prefix="/vector-store", tags=["vector-store"]
    )

    @app.get("/")
    def root():
        return {"message": "AbotMe 백엔드에 오신 것을 환영합니다!"}

    return app


app = create_app()


@app.get("/")
def root():
    return {"message": "AbotMe 백엔드에 오신 것을 환영합니다!"}
