from typing import List, Dict
from app.models.schemas import HistoryItem

# session_id별 대화 이력 저장 (인메모리)
_history: Dict[str, List[HistoryItem]] = {}


def add_history(session_id: str, item: HistoryItem):
    if session_id not in _history:
        _history[session_id] = []
    _history[session_id].append(item)


def get_history(session_id: str) -> List[HistoryItem]:
    return _history.get(session_id, [])
