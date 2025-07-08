from langfuse import get_client
from dotenv import load_dotenv

load_dotenv()
langfuse = get_client()

resume_prompt = langfuse.get_prompt("resume-chunker")
