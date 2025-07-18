from app.database.models.resume import Resume
from app.database.repositories.base import BaseRepository


class ResumeRepository(BaseRepository[Resume]):
    def __init__(self, session):
        super().__init__(session, Resume)
