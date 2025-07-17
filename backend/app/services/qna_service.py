import uuid
from datetime import datetime
from typing import Dict, List

from app.data_pipeline.extract.base import Extractor
from app.database.models.resume import Resume
from app.database.uow import UnitOfWork
from app.llm.vector_store.base import VectorStore
from app.models.schemas import QnAQuestion, QnAQuestionList
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate


class QnAService:
    """
    이력서 기반 QnA 생성/조회/저장 서비스
    """

    def __init__(
        self,
        extractor: Extractor,
        vector_store: VectorStore,
        prompt_template: ChatPromptTemplate,
        uow: UnitOfWork,
        llm=None,
    ):
        self.extractor = extractor
        self.vector_store = vector_store
        self.prompt_template = prompt_template
        self.uow = uow
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=QnAQuestionList)

    @property
    def _runnable(self):
        runnable = self.prompt_template | self.llm | self.parser
        return runnable

    def generate_questions(self, pdf_path: str) -> List[QnAQuestion]:
        """
        PDF에서 메타데이터를 추출하고, 각 label_id별로 질문을 생성한다.
        Returns: 질문 dict 리스트
        """
        meta_list = self.extractor.extract(pdf_path)
        llm_input_lines = [
            f"[{label_id}] {metadata['text']}"
            for label_id, metadata in meta_list.items()
        ]
        llm_input = "[" + "\n".join(llm_input_lines) + "]"
        runnable = self._runnable
        llm_output = runnable.invoke({"input": llm_input})

        questions = []
        with self.uow:
            for llm_question in llm_output.root:
                llm_question.question_id = str(uuid.uuid4())

                questions.append(llm_question)
                self.uow.questions.add(
                    convert_question_pydantic_to_dbmodel(llm_question, resume.resume_id)
                )

        return questions

    def get_questions(self) -> List[QnAQuestion]:
        with self.uow:
            return [
                convert_question_dbmodel_to_pydantic(q)
                for q in self.uow.questions.get_all()
            ]

    def answer_question(self, question_id: str, answer_text: str) -> bool:

        with self.uow:
            self.uow.answers.add(
                convert_answer_pydantic_to_dbmodel(
                    QnAAnswer(
                        question_id=question_id,
                        answer=answer_text,
                        created_at=datetime.utcnow(),
                    )
                )
            )
        return True

    def save_answer_to_vector_store(self, question_id: str) -> bool:
        """
        답변이 달린 질문을 벡터스토어에 저장한다.
        Returns: 성공 여부
        """
        pass
