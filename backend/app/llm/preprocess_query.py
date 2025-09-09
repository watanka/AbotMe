from app.data_pipeline.chunk.agentic_chunker import ChunkType
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser


class QueryType(BaseModel):
    chunk_type: str


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # 가장 가벼운 공개 Gemini API 모델
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

# Enum클래스의 list를 다 리스트업해준다
chunk_types = [member.value for member in ChunkType]


def preprocess_query(query: str) -> str:
    prompt = f"""
Your task is to classify the given sentence into one of the predefined categories. You MUST pick one of the categories.
Possible categories: {chunk_types}

Return the output strictly in JSON format only.  
Example: {{"chunk_type": "education"}}

Examples:
Sentence: "저는 2020년에 서울대학교 컴퓨터공학과를 졸업했습니다." → {{"chunk_type": "education"}}
Sentence: "정보처리기사 자격증을 보유하고 있습니다." → {{"chunk_type": "certification"}}
Sentence: "진행한 프로젝트들 알려줘" → {{"chunk_type": "experience"}}
Sentence: "어떤 코딩 언어 사용해?" → {{"chunk_type": "skills"}}

Now classify this sentence:
"{query}"
"""
    runnable = llm | PydanticOutputParser(pydantic_object=QueryType)
    return runnable.invoke(prompt).dict()
