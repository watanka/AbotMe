from typing import Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def get_by_id(self, id_):
        pk = self.model.__mapper__.primary_key[0].name
        stmt = select(self.model).filter_by(**{pk: id_})
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def add(self, obj: T):
        self.session.add(obj)
        return obj

    def get_all(self):
        stmt = select(self.model)
        result = self.session.execute(stmt)
        return result.scalars().all()
