# LLM 최적화 및 RAG 시스템 설계

이 문서는 AbotMe 프로젝트의 LLM(대형 언어 모델) 활용 최적화, RAG(Retrieval-Augmented Generation) 구성, 사용자 컨텍스트 관리, AI 응답 스트리밍에 대한 설계 및 구현 방안을 정리합니다.

---

## 1. RAG(Retrieval-Augmented Generation) 구성

### 1-1. 벡터 스토어 구성
- 적합한 벡터 데이터베이스(예: Chroma, FAISS, Pinecone 등) 선택 및 구축
    - linkedin(500자 내외), 이력서(4,700자), 포트폴리오(2,000자), 블로그 글 하나당(1,500자) x 20개의 글 => 총 41,700자 정도
    - 임베딩 차원 수 768(google text-embedding-005 모델 기준) x 4bytes = 3,072byte ~= 3KB => 한 글자당 사용 메모리 3KB
    - 41,700 x 3KB = 125,100KB ~= 125MB
    - Railway Volume은 0.5GB까지 무료 지원
    - 따라서 벡터 스토어는 백엔드 서버 로컬에다가 뜨우고, Volume에 저장해서 배포마다 업데이트하도록 구성한다.
- LangChain의 VectorStore 인터페이스 활용

### 1-2. 개인 정보 임베딩 및 벡터화
- 임베딩 대상: 
    - LinkedIn 링크
    - 이력서(PDF)
    - 포트폴리오(PDF)
    - GitHub 링크
    - 블로그 링크
- 각 데이터 소스에서 텍스트 추출 및 임베딩 수행
- 임베딩 모델: Gemini, OpenAI, Sentence Transformers 등 활용 가능
- 임베딩 결과를 벡터 스토어에 저장

---

## 2. 사용자 컨텍스트 관리
- 한 채팅 세션에서 LLM에게 전달할 맥락(대화 이력, 관련 정보 등)의 범위와 정책 설계
- 예시: 최근 N개 메시지, 중요 메시지, 사용자별 프롬프트 템플릿 등
- 컨텍스트 윈도우 최적화 및 토큰 한계 고려

---

## 3. AI 응답 스트리밍(Streaming)
- Gemini 등 LLM API의 스트리밍 기능 지원 여부 확인
- FastAPI에서 SSE(Server-Sent Events) 또는 WebSocket을 활용한 실시간 응답 스트리밍 구현
- 프론트엔드(React)에서 스트리밍 응답 처리 및 표시
- 목적: 사용자 경험(UX) 개선, 응답 지연 최소화

---

## 향후 진행 순서
1. 벡터 스토어 및 임베딩 파이프라인 구축
2. 컨텍스트 관리 정책 및 코드 설계
3. AI 응답 스트리밍 백엔드/프론트엔드 적용

각 단계별 상세 설계 및 구현 내역은 이 문서에 계속 업데이트합니다.
