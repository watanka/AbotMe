from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langfuse import get_client
from langchain.output_parsers import PydanticOutputParser
from app.data_pipeline.chunk.agentic_chunker import ResumeChunkList

load_dotenv()
langfuse = get_client()

# resume_prompt = ChatPromptTemplate.from_template(
#     langfuse.get_prompt("resume-chunker").get_langchain_prompt()
# )


resume_prompt = PromptTemplate(
    input_variables=["input"],
    partial_variables={
        "format_instructions": PydanticOutputParser(
            pydantic_object=ResumeChunkList
        ).get_format_instructions()
    },
    template="""
    System Prompt
You are an expert in segmenting resume text into chunks optimized for vector database storage.
Each chunk should be a semantically complete unit that can be effectively utilized in search and RAG systems.

**Chunking Principles:**
1. Semantic Completeness: Each chunk must be independently understandable
2. Context Preservation: Include necessary background information in each chunk
3. Search Optimization: Structure content so keywords and meanings are clearly evident
4. Appropriate Size: Prioritize semantic boundaries within 200-800 token range

Main Prompt
Please analyze the following resume text and segment it into chunks suitable for vector DB storage.

**Input Text:**
{input}

**Output Format:**
Please output each chunk in the following JSON format:

```json
{{
  "chunks": [
    {{
      "content": "Chunk content (refined original text)",
      "chunk_type": "personal_info|education|experience|skills|certification",
      "metadata": {{
        "period": "Time period (if applicable)",
        "achievement": <achievement summary>,
        "keyword": <keyword summary>,
      }},
      "search_summary": "Summary of key searchable content in this chunk"
    }}
  ]
}}
Chunking Guidelines:

Personal Information Chunk: Name, contact info, self-introduction as one chunk

Serves as overview providing context for the entire resume


Education Chunks: Separate by institution

Include school name, major, period, GPA, etc.


Experience Chunks: Separate by company or major project

Include company info, role, main responsibilities, achievements
Specify tech stack and quantified results


Skills/Certification Chunks: Group related technologies

Categorize by languages, frameworks, databases, infrastructure, etc.



Text Refinement Rules:

Clean up special characters or corrupted text
Use consistent date format (YYYY.MM - YYYY.MM)
Standardize technical terms to official names
Express achievements with clear numerical values

Keyword Extraction Rules:

Technical stack (Python, Django, AWS, etc.)
Domain keywords (OCR, deep learning, backend, etc.)
Achievement keywords (improvement, optimization, development, etc.)
Industry keywords (insurance, healthcare, AI, etc.)

Structure each chunk to clearly show "who, when, where, what, how, and what results" were achieved.

Output Format:
{format_instructions}
""",
).partial(
    format_instructions=PydanticOutputParser(
        pydantic_object=ResumeChunkList
    ).get_format_instructions()
)
