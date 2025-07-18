from app.database.repositories.answer_repository import AnswerRepository
from app.database.repositories.chunk_repository import ChunkRepository
from app.database.repositories.question_repository import QuestionRepository
from app.database.repositories.resume_repository import ResumeRepository
from app.database.repositories.tag_repository import TagRepository
from app.database.session import get_session


class UnitOfWork:
    def __init__(self):
        self.session = None
        self.questions: QuestionRepository = None
        self.resumes: ResumeRepository = None
        self.chunks: ChunkRepository = None
        self.answers: AnswerRepository = None
        self.tags: TagRepository = None

    def __enter__(self):
        self.session = get_session()
        self.questions = QuestionRepository(self.session)
        self.resumes = ResumeRepository(self.session)
        self.chunks = ChunkRepository(self.session)
        self.answers = AnswerRepository(self.session)
        self.tags = TagRepository(self.session)
        return self

    def __exit__(self, *args):
        if self.session:
            self.session.commit()
            self.session.close()

    def commit(self):
        if self.session:
            self.session.commit()
