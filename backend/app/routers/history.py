from fastapi import APIRouter
from app.models.schemas import HistoryItem
from app.services.history_service import get_history
from typing import List

router = APIRouter()


@router.get("/{session_id}", response_model=List[HistoryItem])
def get_history_api(session_id: str):
    return get_history(session_id)
