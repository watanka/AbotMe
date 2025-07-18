from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langfuse import get_client

load_dotenv()
langfuse = get_client()
qna_prompt = ChatPromptTemplate.from_template(
    langfuse.get_prompt("resume-question").get_langchain_prompt()
)
