import hashlib
from typing import List

from app.data_pipeline.chunk.agentic_chunker import ResumeChunk
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j import Neo4jGraph


class GraphDBWriter:
    def __init__(self, graph_db: Neo4jGraph, llm, embedding):
        self.graph_db = graph_db
        self.llm = llm
        self.embedding = embedding
        self.transformer = LLMGraphTransformer(
            llm=self.llm,
            additional_instructions="""
        You are graph expert who handles resume information into graph database. Following this instructions, turn these resume information into nodes and relationships.
        - nodes: Applicant, Company, Project, School, SelfIntro, Activity, Certificate, TechStack, Achievement
        - relationships: WORKED_AT, ATTENDED, PARTICIPATED, OBTAINED, USES, BELONGS_TO, ACHIEVED
            - WORKED_AT: (start_date, end_date, role)
            - ATTENDED: (date)
            - PARTICIPATED: (start_date, end_date, role)
            - OBTAINED: (date)
        - Applicant Node can have name, birth_date, email, github, text properties. Applicant - USES -> SelfIntro, Applicant - WORKED_AT -> Company, Applicant - ATTENDED -> School, Applicant - PARTICIPATED -> Project, Applicant - OBTAINED -> Certificate, Applicant - USES -> TechStack, Applicant - ACHIEVED -> Achievement
        - Company Node can have name, text, properties. Applicant - WORKED_AT -> Company, Project - BELONGS_TO -> Company
        - Project Node can have name, text, properties. Applicant - PARTICIPATED -> Project, TechStack - USES -> Project, Achievement - ACHIEVED -> Project
        - School Node can have name, text, properties. Applicant - ATTENDED -> School
        - SelfIntro Node can have text, properties. Applicant - USES -> SelfIntro
        - Activity Node can have name, text, properties. Applicant - PARTICIPATED -> Activity
        - Certificate Node can have name, text, properties. Applicant - OBTAINED -> Certificate
        - TechStack Node can have name, text, properties. Applicant - USES -> TechStack
        - Achievement Node can have problem, solution, metric, text properties. Applicant - ACHIEVED -> Achievement
        - ALWAYS keep label's first letter as uppercase.
        """,
            allowed_nodes=[
                "Applicant",
                "Company",
                "Project",
                "School",
                "SelfIntro",
                "Activity",
                "Certificate",
                "TechStack",
                "Achievement",
            ],
            allowed_relationships=[
                "WORKED_AT",
                "ATTENDED",
                "PARTICIPATED",
                "OBTAINED",
                "USES",
                "BELONGS_TO",
                "ACHIEVED",
            ],
            node_properties=list(
                set(
                    [
                        # Applicant
                        "name",
                        "birth_date",
                        "email",
                        "github",
                        "text",
                        # Company
                        "name",
                        "text",
                        # Project
                        "name",
                        "text",
                        # School
                        "name",
                        "text",
                        # SelfIntro
                        "description",
                        # Activity
                        "name",
                        "description",
                        # Certificate
                        "name",
                        "text",
                        # TechStack
                        "name",
                        "category",
                        # Achievement
                        "problem",
                        "solution",
                        "metric",
                    ]
                )
            ),
            relationship_properties=[
                "start_date",
                "end_date",
                "role",
                "date",
            ],
            strict_mode=True,
        )

    def save(self, chunks: List[ResumeChunk]):
        if not chunks:
            return

        # chunk -> llm -> graph_component(node, relationship including embeddings)
        # graph_component -> graph_db

        # 1) 내용과 임베딩 계산
        chunk_str_list = [chunk.content for chunk in chunks]
        embeddings = [self.embedding.embed_query(text) for text in chunk_str_list]

        doc_list = [
            Document(page_content=text, metadata={"embedding": embedding})
            for text, embedding in zip(chunk_str_list, embeddings)
        ]

        # 3) 그래프 저장(소스 Document 노드 포함)
        graph_documents = self.transformer.convert_to_graph_documents(doc_list)
        self.graph_db.add_graph_documents(graph_documents, include_source=False)

        # Vector Index 생성
        self.graph_db.query(
            """CREATE VECTOR INDEX document_embedding IF NOT EXISTS
FOR (d:Document)
ON d.embedding
OPTIONS { indexConfig: {
 `vector.dimensions`: 768,
 `vector.similarity_function`: 'cosine'
}}"""
        )
