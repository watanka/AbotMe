# import asyncio
# import os

# import neo4j
# import vertexai
# from dotenv import load_dotenv
# from google import genai
# from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
# from neo4j import GraphDatabase
# from neo4j_graphrag.embeddings import Embedder, OllamaEmbeddings
# from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
# from neo4j_graphrag.experimental.pipeline.pipeline import PipelineResult
# from neo4j_graphrag.generation import GraphRAG
# from neo4j_graphrag.indexes import create_fulltext_index, create_vector_index
# from neo4j_graphrag.llm import LLMInterface, LLMResponse, VertexAILLM
# from neo4j_graphrag.retrievers import (
#     HybridCypherRetriever,
#     Text2CypherRetriever,
#     VectorCypherRetriever,
#     VectorRetriever,
# )

# load_dotenv()

# client = genai.Client()


# URI = os.getenv("NEO4J_URI")
# AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
# DATABASE = "neo4j"
# print(URI)
# print(AUTH)


# # INDEX_NAME = "Instance02"
# driver = GraphDatabase.driver(URI, auth=AUTH)

# # embedder = OllamaEmbeddings(model="all-minilm")

# # embedder = GoogleGenerativeAIEmbeddings(
# #     model="gemini-embedding-001", api_key=os.getenv("GOOGLE_API_KEY")
# # )

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API_KEY")
# )


# file_path = "tests/resume/eunsungshin-ml.pdf"

# NODE_TYPES = [
#     "Applicant",
#     "Company",
#     "Project",
#     "School",
#     "SelfIntro",
#     "Activity",
#     "Certificate",
#     "TechStack",
#     "Achievement",
# ]

# RELATIONSHIP_TYPES = [
#     "WORKED_AT",
#     "ATTENDED",
#     "PARTICIPATED",
#     "OBTAINED",
#     "USES",
#     "BELONGS_TO",
#     "ACHIEVED",
# ]

# PATTERNS = [
#     ("Applicant", "WORKED_AT", "Company"),
#     ("Applicant", "ATTENDED", "School"),
#     ("Applicant", "PARTICIPATED", "Project"),
#     ("Applicant", "OBTAINED", "Certificate"),
#     ("Applicant", "USES", "TechStack"),
#     ("Applicant", "ACHIEVED", "Achievement"),
#     ("Project", "BELONGS_TO", "Company"),
#     ("Project", "USES", "TechStack"),
#     ("Project", "ACHIEVED", "Achievement"),
# ]

# # from typing import Any, List, Optional, Union

# # from neo4j_graphrag.message_history import MessageHistory
# # from neo4j_graphrag.types import LLMMessage


# # class GeminiLLM(LLMInterface):
# #     def __init__(self, model_name: str, model_params: Optional[dict[str, Any]] = None):
# #         self.model_name = model_name
# #         self.model_params = model_params or {}
# #         self._model = ChatGoogleGenerativeAI(
# #             model=model_name, api_key=os.getenv("GOOGLE_API_KEY")
# #         )

# #     def invoke(
# #         self,
# #         input: str,
# #         message_history: Optional[Union[List[LLMMessage], MessageHistory]] = None,
# #         system_instruction: Optional[str] = None,
# #     ) -> str:
# #         return self._parse_content_response(self._model.invoke(input).content)

# #     def _parse_content_response(self, response: str) -> LLMResponse:
# #         return LLMResponse(content=response)

# #     async def ainvoke(
# #         self,
# #         input: str,
# #         message_history: Optional[Union[List[LLMMessage], MessageHistory]] = None,
# #         system_instruction: Optional[str] = None,
# #     ) -> str:
# #         response = await self._model.ainvoke(input)
# #         return self._parse_content_response(response.content)


# # llm = GeminiLLM(model_name="gemini-2.0-flash-exp")


# async def define_and_run_pipeline(
#     neo4j_driver: neo4j.Driver,
#     llm,
# ) -> PipelineResult:
#     # Create an instance of the SimpleKGPipeline
#     kg_builder = SimpleKGPipeline(
#         llm=llm,
#         driver=neo4j_driver,
#         embedder=embedder,
#         schema={
#             "node_types": NODE_TYPES,
#             "relationship_types": RELATIONSHIP_TYPES,
#             "patterns": PATTERNS,
#         },
#         neo4j_database=DATABASE,
#     )
#     return await kg_builder.run_async(file_path=str(file_path))


# async def main():
#     with neo4j.GraphDatabase.driver(URI, auth=AUTH) as driver:
#         res = await define_and_run_pipeline(driver, llm)
#     return res


# if __name__ == "__main__":
#     res = asyncio.run(main())
#     print(res)


# ## search

# neo4j_schema = """
# Node properties:
# Applicant {name, birth_date, email, github, label_id}
# Company {name, label_id}
# Project {name, background, label_id}
# School {name, date, label_id}
# SelfIntro {description, label_id}
# Activity {name, description, label_id}
# Certificate {name, date, label_id}
# TechStack {name, category, label_id}
# Achievement {problem, solution, metric, label_id}
# Relationship properties:
# WORKED_AT {date, role}
# ATTENDED {date}
# PARTICIPATED {date, role}
# OBTAINED {date}
# USES
# BELONGS_TO
# ACHIEVED
# The relationships:
# (:Applicant)-[:WORKED_AT]->(:Company)
# (:Applicant)-[:ATTENDED]->(:School)
# (:Applicant)-[:PARTICIPATED]->(:Project)
# (:Applicant)-[:OBTAINED]->(:Certificate)
# (:Applicant)-[:USES]->(:TechStack)
# (:Applicant)-[:ACHIEVED]->(:Achievement)
# (:Project)-[:BELONGS_TO]->(:Company)
# (:Project)-[USES]->(:TechStack)
# (:Project)-[ACHIEVED]->(:Achievement)
# """

# examples = [
#     "USER INPUT: '신은성에 대해 알려줘' QUERY: MATCH (a:Applicant {name: '신은성'}) RETURN a.name as name, a.label_id as label_id",
#     "USER INPUT: '신은성의 성과 알려줘' QUERY: MATCH (a:Applicant {name: '신은성'})-[:ACHIEVED]->(a:Achievement) RETURN a.name as name, a.label_id as label_id",
#     "USER INPUT: '신은성의 자격증 알려줘' QUERY: MATCH (a:Applicant {name: '신은성'})-[:OBTAINED]->(c:Certificate) RETURN c.name as name, c.label_id as label_id",
#     "USER INPUT: 'python으로 진행한 프로젝트들 알려줘' QUERY: MATCH (p:Project)-[:USES]->(t:TechStack {name: 'python'}) RETURN p.name as name, p.label_id as label_id",
# ]


# # retriever = HybridCypherRetriever(
# #     driver,
# #     INDEX_NAME,
# #     FULLTEXT_INDEX_NAME,
# #     retrieval_query="MATCH (a:Applicant {name: '신은성'})-[:PARTICIPATED]->(p:Project) RETURN p",
# # )


# class GeminiEmbedder(Embedder):
#     def embed_query(self, text: str) -> list[float]:
#         return (
#             client.models.embed_content(model="gemini-embedding-001", contents=text)
#             .embeddings[0]
#             .values
#         )


# embedder = GeminiEmbedder()


# def create_embedding_index(tx):
#     result = tx.run(f"MATCH (n:{node_name}) RETURN n.name, ID(n) AS id")
#     for record in result:
#         name = record["n.name"]
#         id = record["id"]
#         print(name, id)
#         emb = (
#             client.models.embed_content(model="gemini-embedding-001", contents=name)
#             .embeddings[0]
#             .values
#         )

#         tx.run(
#             f"MATCH (n: {node_name} WHERE ID(n) = {id}) SET n.vector = {emb}",
#         )


# node_list = [
#     "Company",
#     "Project",
#     "TechStack",
#     "Activity",
#     "Certificate",
# ]

# # for node_name in node_list:
# #     with driver.session() as session:
# #         session.write_transaction(create_embedding_index)

# context = ""
# with driver.session() as session:
#     for node_name in node_list:
#         result = session.run(f"MATCH (n:{node_name}) RETURN n.name as name")
#         context += (
#             "\n" + node_name + ": " + ",".join([record["name"] for record in result])
#         )

# print(context)


# custom_prompt = (
#     """
#     Task: Generate a Cypher statement for querying a Neo4j graph database from user input.
# Schema:
# {schema}
# Context:
# Edit node label in cypher query according to the node information below, if needed. Because if entity name does not match exactly, it cannot find right node.
# For example, it should be 'python', not '파이썬' or 'Python'.
# """
#     + context
#     + """
# Examples:
# {examples}

# Question:
# {query_text}

# ALWAYS include name, label_id properties, and EXCLUDE vector.
# Answer:
# """
# )
# print(custom_prompt)

# retriever = Text2CypherRetriever(
#     custom_prompt=custom_prompt,
#     driver=driver,
#     llm=llm,
#     neo4j_schema=neo4j_schema,
#     examples=examples,
# )


# # for node_name in node_list:
# #     create_vector_index(
# #         driver,
# #         f"{node_name}_emb_index",
# #         label=node_name,
# #         embedding_property="vector",
# #         dimensions=3072,
# #         similarity_fn="cosine",
# #         fail_if_exists=False,
# #     )


# # rag = GraphRAG(retriever=retriever, llm=llm)

# # query_text = "신은성이 참여했던 프로젝트들 알려줘"

# # response = rag.search(query_text=query_text, return_context=True)
# # print(response.retriever_result.metadata)
# # print(response.answer)


# # retrieval_query = """
# # RETURN node.name as name,
# #         collect { MATCH (p:Project)-[:BELONGS_TO]->(node) RETURN p.name} AS projects
# # """

# # # retriever = VectorCypherRetriever(
# # #     driver, index_name=INDEX_NAME, embedder=embedder, retrieval_query=retrieval_query
# # # )

# # INDEX_NAME = "Company_emb_index"
# # retriever = VectorRetriever(
# #     driver,
# #     index_name=INDEX_NAME,
# #     embedder=embedder,
# # )

# retriever_result = retriever.search(query_text="python으로 진행한 프로젝트들 알려줘")
# print("retriever_result", retriever_result)

# # 🔹 Step 5: 저장 (옵션)
# faiss.write_index(index, "company.index")
# with open("company_names.pkl", "wb") as f:
#     pickle.dump(company_names, f)

# index = faiss.read_index("company.index")
# with open("company_names.pkl", "rb") as f:
#     company_names = pickle.load(f)

import json
import uuid
from typing import Callable, Optional

from app.data_pipeline.prompts import chat_prompt, text2cypher_prompt
from app.database.models.resume import Resume
from app.dependencies import get_graph_db, get_llm, get_uow, get_vector_store
from app.llm.base_engine import BaseEngine
from app.llm.graph_rag_engine import GraphRAGEngine
from app.llm.rag_engine import RAGEngine
from app.services.data_service import run_graph_resume_pipeline, run_resume_pipeline
from ragas import EvaluationDataset, evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import FactualCorrectness, Faithfulness, LLMContextRecall

llm = get_llm()
uow = get_uow()
graph_db = get_graph_db()

# graph rag 호출
graph_rag = GraphRAGEngine(
    graph_db=graph_db,
    text2cypher_prompt=text2cypher_prompt,
    qa_prompt=chat_prompt,
    llm=llm,
    uow=uow,
)

# vector db 호출
vector_db = get_vector_store()
rag = RAGEngine(vector_db, chat_prompt, llm)


# 같은 질문에 답변 테스트
def answer_question(
    question: str, engine: BaseEngine, callback: Optional[Callable] = None
):
    context = engine.retrieve_context(question)
    answer = engine.generate_answer(question, context, callback)
    return answer
