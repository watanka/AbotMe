from app.database.models.tag import Tag
from app.database.repositories.base import BaseRepository


class TagRepository(BaseRepository[Tag]):
    def __init__(self, session):
        super().__init__(session, Tag)
