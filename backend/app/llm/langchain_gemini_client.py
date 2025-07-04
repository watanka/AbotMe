from app.llm.llm_client import LLMClient
import os
from langchain.chat_models import init_chat_model

class LangChainGeminiClient(LLMClient):
    """
    Gemini API를 사용하는 LangChain 기반 LLMClient 구현체.
    환경변수 GEMINI_API_KEY에 키를 저장해야 합니다.
    """
    def __init__(self, model: str = "gemini-2.0-flash-exp"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY 환경변수가 설정되어 있지 않습니다.")
        self.llm = init_chat_model(model, model_provider="google_genai")

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Gemini LLM에 프롬프트를 전달하고, 응답 텍스트를 반환합니다.
        :param prompt: 사용자 입력
        :param kwargs: 추가 파라미터
        :return: LLM 응답 텍스트
        """
        response = self.llm.invoke(prompt)
        # LangChain 응답 객체에서 텍스트 추출
        if hasattr(response, "content"):
            return response.content
        elif hasattr(response, "text"):
            return response.text
        return str(response)

if __name__ == "__main__":
    import sys
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "안녕, 너는 누구야?"
    try:
        client = LangChainGeminiClient()
        result = client.generate(prompt)
        print("Gemini 응답:", result)
    except Exception as e:
        print("에러:", e)
