from langfuse import get_client

langfuse = get_client()

resume_prompt = langfuse.get_prompt("resume-chunker")

