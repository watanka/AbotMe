from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langfuse import get_client

load_dotenv()
langfuse = get_client()

user_query_prompt = ChatPromptTemplate.from_template(
    langfuse.get_prompt("user-query").get_langchain_prompt()
)
