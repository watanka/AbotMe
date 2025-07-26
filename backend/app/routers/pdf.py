import os
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Query, Response

router = APIRouter()

load_dotenv()

GCS_FILE_STORAGE_URL = os.getenv("GCS_FILE_STORAGE_URL")


@router.get("/")
def get_pdf(fname: str = Query(...)):
    url = urljoin(GCS_FILE_STORAGE_URL + "/", fname)

    gcs_response = requests.get(url)
    if gcs_response.status_code != 200:
        return Response(content="File not found", status_code=404)

    return Response(
        content=gcs_response.content,
        media_type="application/pdf",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Content-Disposition": f'inline; filename="{fname}"',
        },
    )
