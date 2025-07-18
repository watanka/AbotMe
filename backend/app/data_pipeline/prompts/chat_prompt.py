from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langfuse import get_client

load_dotenv()
langfuse = get_client()
chat_prompt = ChatPromptTemplate.from_template(
    langfuse.get_prompt("chat-answer").get_langchain_prompt()
)
