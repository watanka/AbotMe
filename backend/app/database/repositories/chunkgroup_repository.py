from app.database.models.chunk_group import ChunkGroup
from app.database.repositories.base import BaseRepository


class ChunkGroupRepository(BaseRepository[ChunkGroup]):
    def __init__(self, session):
        super().__init__(session, ChunkGroup)
