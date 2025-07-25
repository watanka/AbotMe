from app.database.models.chunk import Chunk
from app.database.repositories.base import BaseRepository


class ChunkRepository(BaseRepository[Chunk]):
    def __init__(self, session):
        super().__init__(session, Chunk)

    def get_by_chunk_group_id(self, chunk_group_id: int):
        return (
            self.session.query(self.model)
            .filter_by(chunk_group_id=chunk_group_id)
            .all()
        )

    def upsert_by_label_id(self, chunk: Chunk):
        obj = self.session.merge(chunk)
        return obj
