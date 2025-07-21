from app.database.models.question import Question
from app.database.repositories.base import BaseRepository


class QuestionRepository(BaseRepository[Question]):
    def __init__(self, session):
        super().__init__(session, Question)
