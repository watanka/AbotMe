import os

from dotenv import load_dotenv
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app):
    load_dotenv()

    frontend_url = os.getenv("FRONTEND_URL", "https://watanka.github.io")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_url],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
