from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document


class GraphDBWriter:
    def __init__(self, graph_db: Neo4jGraph, llm):
        self.graph_db = graph_db
        self.llm = llm
        self.transformer = LLMGraphTransformer(
            llm=self.llm,
            additional_instructions="""
        You are graph expert who handles resume information into graph database. Following this instructions, turn these resume information into nodes and relationships.
        - **input format consists of (label_id, text), and label_id is important information to trace original resume.**
        - nodes: Applicant, Company, Project, School, SelfIntro, Activity, Certificate, TechStack, Achievement
        - relationships: WORKED_AT, ATTENDED, PARTICIPATED, OBTAINED, USES, BELONGS_TO, ACHIEVED
        - Applicant Node can only have name, birth_date, email, github, label_id properties.
        - Company Node can only have name, label_id properties.
        - Project Node can only have name, background, label_id properties.
        - School Node can only have name, date, label_id properties.
        - SelfIntro Node can only have description, label_id properties.
        - Activity Node can only have name, description, label_id properties.
        - Certificate Node can only have name, date, label_id properties.
        - TechStack Node can only have name, category, label_id properties.
        - Achievement Node can only have problem, solution, metric, label_id properties.
        - Make sure you keep id same as name.
        """,
        allowed_nodes=[
            "Applicant", "Company", "Project", "School", "SelfIntro",
            "Activity", "Certificate", "TechStack", "Achievement"
        ],
        allowed_relationships=[
            "WORKED_AT",             # 지원자 - 회사 (재직했다, 기간 등)
            "ATTENDED",              # 지원자 - 학교 (다녔다)
            "PARTICIPATED",   # 지원자 - 프로젝트 (진행했다, 기간, 역할)
            "OBTAINED",              # 지원자 - 자격증 (취득했다)
            "USES",                  # 지원자 - 기술스택 (사용한다)
            "BELONGS_TO",    # 프로젝트 - 회사 (소속)
            "ACHIEVED",      # 프로젝트 - 성과 (성과를 냈다)
        ],
        node_properties=list(set([
        # Applicant
        "name", "birth_date", "email", "github", "label_id",
        # Company
        "name", "label_id",
        # Project
        "name", "background", "label_id", 
        # School
        "name", "date", "label_id",
        # SelfIntro
        "description", "label_id",
        # Activity
        "name", "description", "label_id",
        # Certificate
        "name", "date", "label_id",
        # TechStack
        "name", "category", "label_id",
        # Achievement
        "problem", "solution", "metric", "label_id",
        ])),
        relationship_properties=[
            # WORKED_AT, ATTENDED, PARTICIPATED_IN_PROJECT, PARTICIPATED_IN_ACTIVITY
            "start_date", "end_date", "role",
            # OBTAINED
            "date",
            # 기타 관계 속성 필요시 추가
        ],
        strict_mode=True,
        )

    
    def convert_text_to_graph(self, text: str):
        doc = Document(page_content=text)
        return self.transformer.convert_to_graph_documents([doc])

    def save(self, docs: List[dict]):
        self.graph_db.add_graph_documents(docs, include_source=True)
