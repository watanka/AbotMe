from typing import Optional, Callable
from langchain_core.prompts import ChatPromptTemplate
from langfuse import get_client
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph


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
    ):
        self.graph_db = graph_db
        self.text2cypher_prompt = text2cypher_prompt
        self.qa_prompt = qa_prompt
        self.llm = llm

    def retrieve_context(self, msg: str):
        print("text2cypher_prompt: ", self.text2cypher_prompt)
        print("llm: ", self.llm)
        _text2cypher_runnable = self.text2cypher_prompt | self.llm
        query_cypher = _text2cypher_runnable.invoke({"user_question": msg})
        if "NO_CYPHER" in query_cypher.content:
            return "NO_CYPHER"
        return str(self.graph_db.query(query_cypher.content))

    def generate_answer(self, msg: str, callback: Optional[Callable] = None):
        context = self.retrieve_context(msg)
        filled_prompt = self.qa_prompt.format_messages(msg=msg, context=context)
        for chunk in self.llm.stream(filled_prompt):
            yield chunk.content
