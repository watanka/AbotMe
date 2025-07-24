from langfuse import get_client
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
langfuse = get_client()
text2cypher_prompt = ChatPromptTemplate.from_template(
    langfuse.get_prompt("text2cypher").get_langchain_prompt()
        )