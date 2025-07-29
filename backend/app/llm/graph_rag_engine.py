from typing import Callable, Optional

from app.database.uow import UnitOfWork
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_neo4j import Neo4jGraph
from langfuse import get_client


class GraphRAGEngine:
    """
    LLM과 GraphDB(Neo4J)를 결합한 RAG 엔진
    """

    def __init__(
        self,
        graph_db: Neo4jGraph,
        text2cypher_prompt: ChatPromptTemplate,
        qa_prompt: ChatPromptTemplate,
        llm,
        uow: UnitOfWork,
    ):
        self.graph_db = graph_db

        self.text2cypher_prompt = text2cypher_prompt
        self.qa_prompt = qa_prompt
        self.llm = llm
        self.node_information = self._get_node_information()
        self.uow = uow

    def _get_node_information(self):
        node_list = [
            "Applicant",
            "Company",
            "Project",
            "School",
            "Activity",
            "Certificate",
            "TechStack",
        ]
        node_information = ""
        with self.graph_db._driver.session() as session:
            for node in node_list:
                node_information += (
                    f'{node}: {str(session.run(f"MATCH (n:{node}) RETURN n.name"))}\n'
                )
            session.close()

        return node_information

    def retrieve_context(self, msg: str, callback: Optional[Callable] = None):
        _text2cypher_runnable = self.text2cypher_prompt | self.llm
        query_cypher = _text2cypher_runnable.invoke(
            {
                "node_information": self.node_information,
                "user_question": msg,
                "callback": callback,
            }
        )
        if "NO_CYPHER" in query_cypher.content:
            return "NO_CYPHER"

        print("query_cypher: ", query_cypher.content)
        return self.graph_db.query(query_cypher.content)

    def _parse_label_id(self, context: dict):
        label_id_list = []
        for c in context:
            # label_id list가 str형식으로 저장. e.g) '["1-1", "1-2"]' : Str
            label_id_list.extend(eval(c["label_id"]))
        return label_id_list

    def get_metadata(self, context: dict):
        label_id_list = self._parse_label_id(context)

        metadata_result = []
        with self.uow:
            for label_id in label_id_list:
                chunk = self.uow.chunks.get_by_id(label_id)
                if not chunk:
                    continue
                metadata_result.append(
                    {
                        "x0": chunk.x0,
                        "x1": chunk.x1,
                        "top": chunk.top,
                        "bottom": chunk.bottom,
                        "page_id": chunk.page_id,
                    }
                )
        return metadata_result

    def generate_answer(
        self, msg: str, context: dict, callback: Optional[Callable] = None
    ):
        filled_prompt = self.qa_prompt.format_messages(msg=msg, context=str(context))
        for chunk in self.llm.stream(filled_prompt, config={"callbacks": [callback]}):
            yield chunk.content
            yield chunk.content
