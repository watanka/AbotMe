from app.database.models.chunk import ResumeChunk
from app.database.repositories.base import BaseRepository


class ChunkRepository(BaseRepository[ResumeChunk]):
    def __init__(self, session):
        super().__init__(session, ResumeChunk)
