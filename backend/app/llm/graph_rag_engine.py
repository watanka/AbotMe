import math
import traceback
from typing import Callable, Optional

from app.data_pipeline.prompts import (
    GraphComponent,
    find_graph_component_prompt,
    parser,
)
from app.database.uow import UnitOfWork
from app.llm.base_engine import BaseEngine
from app.llm.vector_store.embedding import GeminiEmbeddingModel
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_neo4j import Neo4jGraph
from langfuse import get_client


class GraphRAGEngine(BaseEngine):
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
        self.llm = llm
        self.text2cypher_prompt = text2cypher_prompt
        self.text2cypher_runnable = self.text2cypher_prompt | self.llm
        self.qa_prompt = qa_prompt
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
        relationship_information = ""
        with self.graph_db._driver.session() as session:
            graph_results = self.graph_db.query(
                "MATCH (n) RETURN DISTINCT labels(n) AS labels"
            )
            for res in graph_results:
                node_information += ", ".join(res["labels"]) + "\n"
            relationship_information = self.graph_db.query(
                "MATCH ()-[r]->() RETURN DISTINCT type(r) AS type"
            )

        return node_information, relationship_information

    def retrieve_context_with_embedding(
        self, msg: str, callback: Optional[Callable] = None
    ):
        # msg에 따라 찾는 노드 나누기
        find_graph_component_prompt_runnable = (
            find_graph_component_prompt | self.llm | parser
        )
        graph_component: GraphComponent = find_graph_component_prompt_runnable.invoke(
            {
                "user_question": msg,
                "node_information": self.node_information,
                "relationship_information": self.relationship_information,
                "callback": callback,
            }
        )

        # type/name 기반 Cypher로 우선 조회
        cypher = self._cypher_for_graph_component(graph_component)
        try:
            query_result = self.graph_db.query(cypher)
        except Exception:
            traceback.print_exc()
            return []

        filtered_result = self.similarity_search(msg, query_result)
        return filtered_result

    def similarity_search(self, msg: str, results, top_k: int = 5):
        """
        Compare the embedding of the question (msg) to the embeddings of
        Neo4j query results and return top_k most similar items.
        """
        try:
            embeddings = GeminiEmbeddingModel().get_model()
        except Exception:
            traceback.print_exc()
            return []

        # Embed query
        try:
            q_vec = embeddings.embed_query(msg)
        except Exception:
            traceback.print_exc()
            return []

        def cosine(a, b):
            dot = sum(x * y for x, y in zip(a, b))
            na = math.sqrt(sum(x * x for x in a))
            nb = math.sqrt(sum(y * y for y in b))
            if na == 0.0 or nb == 0.0:
                return 0.0
            return dot / (na * nb)

        scored = []
        for item in results:
            try:
                score = cosine(q_vec, item.metadata["embedding"])
            except Exception:
                score = 0.0
            scored.append({"score": score, "text": item.page_content})
        scored.sort(key=lambda x: x["score"], reverse=True)

        return "\n".join([s["text"] for s in scored[:top_k]])

    def _cypher_for_graph_component(self, component: GraphComponent) -> str:
        """
        Build a Cypher query string based on the
        component's type and name.
        """
        safe_name = component.name.replace("`", "``")
        if component.type == "node":
            return f"MATCH (n:`{safe_name}`) RETURN n LIMIT 50"
        else:
            return "MATCH (a)-[r:`" + safe_name + "`]- (b) " "RETURN a, r, b LIMIT 50"

    def retrieve_context(self, msg: str, callback: Optional[Callable] = None):
        print("query에 들어가는 노드 정보들: ", self.node_information)

        query_cypher = self.text2cypher_runnable.invoke(
            {
                "node_information": self.node_information,
                "user_question": msg,
                "callback": callback,
            }
        )

        print("query_cypher: ", query_cypher.content)
        if "NO_CYPHER" in query_cypher.content:
            return "NO_CYPHER"

        try:
            query_result = self.graph_db.query(query_cypher.content)
            return query_result
        except Exception as e:
            traceback.print_exc()
            return ""

    def _parse_label_id(self, context: dict):
        label_id_list = []
        for c in context:
            # label_id list가 str형식으로 저장. e.g) '["1-1", "1-2"]' : Str
            labels = c["label_id"]
            if labels.startswith("[") and labels.endswith("]"):
                label_id_list.extend(eval(labels))
            else:
                label_id_list.extend(labels.split(","))
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
        print("filled_prompt: ", filled_prompt)
        for chunk in self.llm.stream(filled_prompt, config={"callbacks": [callback]}):
            yield chunk.content
