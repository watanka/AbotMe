from app.database.models.answer import Answer
from app.database.repositories.base import BaseRepository


class AnswerRepository(BaseRepository[Answer]):
    def __init__(self, session):
        super().__init__(session, Answer)
