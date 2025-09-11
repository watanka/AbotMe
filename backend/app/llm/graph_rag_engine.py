import traceback
from typing import Callable, Dict, List, Optional

from app.data_pipeline.prompts import (
    GraphComponent,
    find_graph_component_prompt,
    parser,
)
from app.database.uow import UnitOfWork
from app.llm.base_engine import BaseEngine
from app.llm.vector_store.embedding import GeminiEmbeddingModel
from app.models.schemas import HistoryItem
from langchain_core.prompts import ChatPromptTemplate
from langchain_neo4j import Neo4jGraph


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
        self.embed_model = GeminiEmbeddingModel().get_model()

        # LLM에게 넘겨줄 graphDB 내 정보들(node, relationship) 파싱 후 초기화
        self.node_information, self.relationship_information = (
            self._get_graph_information()
        )
        self.uow = uow

    def _get_graph_information(self):
        # node_list = [
        #     "Applicant",
        #     "Company",
        #     "Project",
        #     "School",
        #     "Activity",
        #     "Certificate",
        #     "TechStack",
        # ]
        node_information = ""
        relationship_information = ""
        with self.graph_db._driver.session() as session:
            node_result = session.run(
                "MATCH (n) RETURN DISTINCT labels(n) AS labels"
            )  # node id와 label 리턴. id에는 각각 고유명사가 들어있음. WHERE {} = "{}"할 시에 활용
            node_information += "node name: "
            for res in node_result:
                node_information += "," + res["labels"][0]
            entity_result = session.run("MATCH (n) RETURN DISTINCT n.id AS id")
            node_information += "\n entity: " + ",".join(
                [r["id"] for r in entity_result]
            )

            relationship_information = session.run(
                "MATCH ()-[r]->() RETURN DISTINCT type(r) AS type"
            )

        return node_information, relationship_information

    def retrieve_context_with_embedding(
        self,
        msg: str,
        callback: Optional[Callable] = None,
        top_k: int = 8,
        hops: int = 2,
    ) -> str:
        """
        HNSW 기반으로 Document 상위 top_k를 찾고, 각 문서에서 최대 hops 만큼 멀티홉 확장한
        이웃 엔티티 요약을 포함한 컨텍스트 문자열을 생성합니다.
        """
        # 1) 쿼리 임베딩
        try:
            embeddings = GeminiEmbeddingModel().get_model()
            q_vec = embeddings.embed_query(msg)
        except Exception:
            traceback.print_exc()
            return ""

        # 2) HNSW kNN on :Document
        try:
            docs = self._hnsw_documents(q_vec, k=top_k)
        except Exception:
            traceback.print_exc()
            return ""
        if not docs:
            return ""

        # 3) 멀티홉 확장(문서 → 엔티티)
        doc_ids = [d["id"] for d in docs if "id" in d]
        try:
            neighbors = self._expand_from_docs(doc_ids, max_hops=hops, max_neighbors=50)
        except Exception:
            traceback.print_exc()
            neighbors = []

        # 4) 컨텍스트 구성
        context = self._build_context(docs, neighbors)
        return context

    def similarity_search(self, msg: str, results, top_k: int = 5):
        """
        HNSW 기반 벡터 인덱스를 사용하여 :Document 노드에서
        질문(msg) 임베딩과 가장 유사한 상위 top_k 문서를 조회합니다.
        참고: results 인자는 더 이상 사용하지 않으며, 하위 호환을 위해 유지합니다.
        """
        # 1) 쿼리 임베딩 계산
        try:
            embeddings = GeminiEmbeddingModel().get_model()
            q_vec = embeddings.embed_query(msg)
        except Exception:
            traceback.print_exc()
            return []

        # 2) 벡터 인덱스(HNSW) 보장 및 질의
        try:
            self._ensure_document_vector_index(
                dimensions=len(q_vec), similarity="cosine"
            )
        except Exception:
            # 인덱스 생성이 실패하더라도 질의는 시도
            traceback.print_exc()

        try:
            cypher = (
                "CALL db.index.vector.queryNodes($indexName, $k, $qvec) "
                "YIELD node, score "
                "RETURN coalesce(node.text, node.content) AS text, score "
                "ORDER BY score DESC"
            )
            rows = self.graph_db.query(
                cypher,
                params={"indexName": "document_embedding", "k": top_k, "qvec": q_vec},
            )
        except Exception:
            traceback.print_exc()
            return []

        return "\n".join([r.get("text", "") for r in rows if r.get("text")])

    def _ensure_document_vector_index(
        self, dimensions: int, similarity: str = "cosine"
    ):
        """
        Document 임베딩 속성(d.embedding)에 대한 HNSW 벡터 인덱스를 보장합니다.
        """
        # 0) 존재 확인
        try:
            exists_rows = self.graph_db.query(
                "SHOW INDEXES YIELD name WHERE name = 'document_embedding' RETURN name"
            )
            if exists_rows:
                return
        except Exception:
            # SHOW INDEXES를 지원하지 않는 경우는 거의 없음. 무시하고 진행.
            pass

        # 1) 절차 기반 생성 우선 시도
        try:
            self.graph_db.query(
                "CALL db.index.vector.createNodeIndex($name, $label, $prop, $dim, $sim)",
                params={
                    "name": "document_embedding",
                    "label": "Document",
                    "prop": "embedding",
                    "dim": int(dimensions),
                    "sim": similarity,
                },
            )
            return
        except Exception:
            pass

        # 2) DDL 생성(버전 호환용) - VECTOR 키워드 없이 일반 CREATE INDEX 사용
        try:
            cypher = (
                f"CREATE INDEX document_embedding IF NOT EXISTS "
                f"FOR (d:Document) ON (d.embedding) "
                f"OPTIONS {{indexConfig: {{`vector.dimensions`: {int(dimensions)}, `vector.similarity_function`: '{similarity}'}}}}"
            )
            self.graph_db.query(cypher)
        except Exception:
            traceback.print_exc()

    def _hnsw_documents(self, q_vec: List[float], k: int = 8) -> List[Dict]:
        """
        HNSW 인덱스를 사용해 :Document 노드에서 상위 k개 반환
        반환 형식: [{id, text, score}]
        """
        # 인덱스 보장
        self._ensure_document_vector_index(dimensions=len(q_vec), similarity="cosine")

        cypher = (
            "CALL db.index.vector.queryNodes($indexName, $k, $qvec) "
            "YIELD node, score "
            "RETURN elementId(node) AS id, coalesce(node.text, '') AS text, score "
            "ORDER BY score DESC"
        )
        rows = self.graph_db.query(
            cypher,
            params={"indexName": "document_embedding", "k": k, "qvec": q_vec},
        )
        return rows

    def _expand_from_docs(
        self, doc_ids: List[str], max_hops: int = 2, max_neighbors: int = 50
    ) -> List[Dict]:
        """
        선택된 문서에서 최대 max_hops까지의 이웃 엔티티를 요약 정보로 수집
        반환 형식: [{docId, neighbors: [{labels, name, text}...]}]
        """
        cypher = (
            f"MATCH (d:Document) WHERE elementId(d) IN $docIds "
            f"OPTIONAL MATCH (d)-[*1..{max_hops}]-(n) "
            "WITH elementId(d) AS docId, n "
            "WHERE n IS NOT NULL "
            "WITH docId, collect(DISTINCT n) AS ns "
            "WITH docId, ns, CASE WHEN size(ns) > $maxNeighbors THEN $maxNeighbors ELSE size(ns) END AS m "
            "RETURN docId, [i IN range(0, m-1) | {labels: labels(ns[i]), name: ns[i].name, text: ns[i].text}] AS neighbors"
        )
        rows = self.graph_db.query(
            cypher, params={"docIds": doc_ids, "maxNeighbors": max_neighbors}
        )
        return rows

    def _build_context(self, docs: List[Dict], neighbors: List[Dict]) -> str:
        """
        Top-k 문서 스니펫과 각 문서에서 확장한 이웃 엔티티 요약을 합쳐 컨텍스트 문자열 생성
        """
        # 문서 섹션
        doc_lines = [
            f"[Doc#{i + 1} score={d.get('score', 0):.4f}] {d.get('text', '')[:500]}"
            for i, d in enumerate(docs)
        ]

        # 이웃 섹션: docId 기준으로 매핑
        nbr_map = {row.get("docId"): row.get("neighbors", []) for row in neighbors}
        nbr_lines_all: List[str] = []
        for i, d in enumerate(docs):
            did = d.get("id")
            items = nbr_map.get(did, [])
            # 각 이웃은 {labels, name, text}
            preview = []
            for it in items[:20]:
                labels = ",".join(it.get("labels", []) or [])
                name = it.get("name")
                text = it.get("text")
                if name:
                    preview.append(f"({labels}) name={name}")
                elif text:
                    preview.append(f"({labels}) text={text[:80]}")
                else:
                    preview.append(f"({labels})")
            nbr_lines_all.append(f"[Doc#{i + 1} neighbors] " + "; ".join(preview))

        context = "\n".join(
            ["# Top Documents"] + doc_lines + ["", "# Graph Neighbors"] + nbr_lines_all
        )
        return context

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
        print("node: ", self.node_information)
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

    def generate_answer(
        self,
        msg: str,
        context: dict,
        chat_history: List[HistoryItem],
        callback: Optional[Callable] = None,
    ):
        chat_history = "\n".join([c.format() for c in chat_history])
        filled_prompt = self.qa_prompt.format_messages(
            question=msg, context=str(context), chat_history=chat_history
        )
        print("filled_prompt: ", filled_prompt)
        for chunk in self.llm.stream(filled_prompt, config={"callbacks": [callback]}):
            yield chunk.content

    def answer(
        self,
        msg: str,
        callback: Optional[Callable] = None,
        chat_history: List[HistoryItem] = [],
    ):
        """
        고수준 질의 응답 API.
        1) text2cypher 기반 구조적 경로 시도
        """
        context = self.retrieve_context(msg, callback)
        return self.generate_answer(
            msg, context, chat_history=chat_history, callback=callback
        )
