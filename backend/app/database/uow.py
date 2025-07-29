from app.database.models.base import Base
from app.database.repositories.answer_repository import AnswerRepository
from app.database.repositories.chunk_repository import ChunkRepository
from app.database.repositories.chunkgroup_repository import ChunkGroupRepository
from app.database.repositories.question_repository import QuestionRepository
from app.database.repositories.resume_repository import ResumeRepository
from app.database.repositories.tag_repository import TagRepository
from app.database.session import engine, get_session


class UnitOfWork:
    def __init__(self):
        self.session = None
        self.questions: QuestionRepository = None
        self.resumes: ResumeRepository = None
        self.chunks: ChunkRepository = None
        self.answers: AnswerRepository = None
        self.tags: TagRepository = None
        self.chunk_groups: ChunkGroupRepository = None

    def __enter__(self):
        self.session = get_session()
        self.questions = QuestionRepository(self.session)
        self.resumes = ResumeRepository(self.session)
        self.chunks = ChunkRepository(self.session)
        self.answers = AnswerRepository(self.session)
        self.tags = TagRepository(self.session)
        self.chunk_groups = ChunkGroupRepository(self.session)
        return self

    def __exit__(self, *args):
        if self.session:
            self.session.commit()
            self.session.close()

    def commit(self):
        if self.session:
            self.session.commit()

    def drop_table(self):
        try:
            Base.metadata.drop_all(engine)
        except:
            print("[INFO] 테이블 삭제X")

    def create_table(self):
        Base.metadata.create_all(engine)
