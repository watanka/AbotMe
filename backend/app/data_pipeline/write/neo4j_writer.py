from typing import List

from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j import Neo4jGraph


class GraphDBWriter:
    def __init__(self, graph_db: Neo4jGraph, llm):
        self.graph_db = graph_db
        self.llm = llm
        self.transformer = LLMGraphTransformer(
            llm=self.llm,
            additional_instructions="""
        You are graph expert who handles resume information into graph database. Following this instructions, turn these resume information into nodes and relationships.
        - **input format consists of (label_id, text), and label_id is important information to trace original resume. and label_id is splitted by comma, so make sure it is saved as list in db.**
        - nodes: Applicant, Company, Project, School, SelfIntro, Activity, Certificate, TechStack, Achievement
        - relationships: WORKED_AT, ATTENDED, PARTICIPATED, OBTAINED, USES, BELONGS_TO, ACHIEVED
            - WORKED_AT: (start_date, end_date, role)
            - ATTENDED: (date)
            - PARTICIPATED: (start_date, end_date, role)
            - OBTAINED: (date)
        - Applicant Node can have name, birth_date, email, github, text, label_id properties. Applicant - USES -> SelfIntro, Applicant - WORKED_AT -> Company, Applicant - ATTENDED -> School, Applicant - PARTICIPATED -> Project, Applicant - OBTAINED -> Certificate, Applicant - USES -> TechStack, Applicant - ACHIEVED -> Achievement
        - Company Node can have name, text, label_id properties. Applicant - WORKED_AT -> Company, Project - BELONGS_TO -> Company
        - Project Node can have name, text, label_id properties. Applicant - PARTICIPATED -> Project, TechStack - USES -> Project, Achievement - ACHIEVED -> Project
        - School Node can have name, text, label_id properties. Applicant - ATTENDED -> School
        - SelfIntro Node can have text, label_id properties. Applicant - USES -> SelfIntro
        - Activity Node can have name, text, label_id properties. Applicant - PARTICIPATED -> Activity
        - Certificate Node can have name, text, label_id properties. Applicant - OBTAINED -> Certificate
        - TechStack Node can have name, text, label_id properties. Applicant - USES -> TechStack
        - Achievement Node can have problem, solution, metric, text, label_id properties. Applicant - ACHIEVED -> Achievement
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
                "WORKED_AT",  # 지원자 - 회사 (재직했다, 기간 등)
                "ATTENDED",  # 지원자 - 학교 (다녔다)
                "PARTICIPATED",  # 지원자 - 프로젝트 (진행했다, 기간, 역할)
                "OBTAINED",  # 지원자 - 자격증 (취득했다)
                "USES",  # 지원자 - 기술스택 (사용한다)
                "BELONGS_TO",  # 프로젝트 - 회사 (소속)
                "ACHIEVED",  # 프로젝트 - 성과 (성과를 냈다)
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
                        "label_id",
                        # Company
                        "name",
                        "text",
                        "label_id",
                        # Project
                        "name",
                        "text",
                        "label_id",
                        # School
                        "name",
                        "text",
                        "label_id",
                        # SelfIntro
                        "description",
                        "label_id",
                        # Activity
                        "name",
                        "description",
                        "label_id",
                        # Certificate
                        "name",
                        "text",
                        "label_id",
                        # TechStack
                        "name",
                        "category",
                        "label_id",
                        # Achievement
                        "problem",
                        "solution",
                        "metric",
                        "label_id",
                    ]
                )
            ),
            relationship_properties=[
                "start_date",
                "end_date",
                "role",
            ],
            strict_mode=True,
        )

    def convert_text_to_graph(self, text: str):
        doc = Document(page_content=text)
        return self.transformer.convert_to_graph_documents([doc])

    def save(self, docs: List[dict]):
        self.graph_db.add_graph_documents(docs, include_source=True)
