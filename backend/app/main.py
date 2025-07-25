from app.middleware.cors import setup_cors
from app.routers import chat, faq, history, resume, token, vector_store
from fastapi import FastAPI
from fastapi.middleware.proxy_headers import ProxyHeadersMiddleware


def create_app():
    app = FastAPI(redirect_slashes=False)

    setup_cors(app)

    app.include_router(chat.router, prefix="/chat", tags=["chat"])
    app.include_router(faq.router, prefix="/faq", tags=["faq"])
    app.include_router(history.router, prefix="/history", tags=["history"])
    app.include_router(
        vector_store.router, prefix="/vector-store", tags=["vector-store"]
    )
    app.include_router(resume.router, prefix="/resume", tags=["resume"])
    app.include_router(token.router, prefix="/token", tags=["token"])
    app.add_middleware(ProxyHeadersMiddleware)
    return app


app = create_app()


@app.get("/")
def root():
    return {"message": "AbotMe 백엔드에 오신 것을 환영합니다!"}
