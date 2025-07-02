from app.models.schemas import FAQ


def get_faqs() -> list[FAQ]:
    # 실제 데이터베이스 연동 전까지는 하드코딩된 예시 반환
    return [
        FAQ(
            question="AbotMe는 무엇인가요?",
            answer="AbotMe는 나를 소개하는 AI 챗봇입니다.",
        ),
        FAQ(
            question="어떤 기술을 사용하나요?",
            answer="FastAPI, React, Langchain, ChromaDB 등 최신 기술을 사용합니다.",
        ),
        FAQ(question="백엔드는 어디에 배포되나요?", answer="Railway에 배포됩니다."),
    ]
