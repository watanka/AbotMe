import json
import os

import pytest
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_neo4j import Neo4jGraph
from langfuse import get_client

load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

llm_transformer = LLMGraphTransformer(llm=llm)
graph = Neo4jGraph(refresh_schema=False)


@pytest.mark.skip
def test_save_chunks_to_neo4j():
    # extractor = PDFResumeMetadataExtractor()
    # chunker = AgenticMetadataChunker()

    # meta_list = extractor.extract("./tests/resume/eunsungshin-ml.pdf")
    # chunk_groups = chunker.chunk(meta_list)

    with open("./tests/chunk_results/eunsung_안성희 이력서.json", "r") as f:
        chunk_groups = json.load(f)

    document = Document(
        page_content="\n".join(
            [
                "\n".join([chunk["chunk_text"] for chunk in chunk_group])
                for chunk_group in chunk_groups
            ]
        )
    )

    print(document)

    llm_transformer_filtered = LLMGraphTransformer(
        llm=llm,
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
                    "label_id",
                    # Company
                    "name",
                    "label_id",
                    # Project
                    "name",
                    "background",
                    "label_id",
                    # School
                    "name",
                    "date",
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
                    "date",
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
            # WORKED_AT, ATTENDED, PARTICIPATED_IN_PROJECT, PARTICIPATED_IN_ACTIVITY
            "start_date",
            "end_date",
            "role",
            # OBTAINED
            "date",
            # 기타 관계 속성 필요시 추가
        ],
        strict_mode=True,
    )
    graph_documents_filtered = llm_transformer_filtered.convert_to_graph_documents(
        [document]
    )
    print(f"Nodes:{graph_documents_filtered[0].nodes}")
    print(f"Relationships:{graph_documents_filtered[0].relationships}")

    graph.add_graph_documents(graph_documents_filtered, include_source=True)


@pytest.mark.skip("실제 llm 사용")
def test_user_query2_cypher():

    load_dotenv()
    langfuse = get_client()
    text2cypher_prompt = ChatPromptTemplate.from_template(
        langfuse.get_prompt("text2cypher").get_langchain_prompt()
    )

    llm_input = "안성희가 진행한 프로젝트들 다 알려줘."
    runnable = text2cypher_prompt | llm
    llm_output = runnable.invoke({"user_question": llm_input})

    print("cypher query: ", llm_output)
    print(graph.query(llm_output.content))
