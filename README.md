# AbotMe
AI 챗봇 웹 애플리케이션입니다. 챗봇을 기반으로 사용자의 질문에 내 정보(개발자 신은성)를 제공합니다.  

## 데모 영상
[![데모 영상](https://img.youtube.com/vi/93ThYTHi6wY/0.jpg)](https://www.youtube.com/watch?v=93ThYTHi6wY)



~~[🚀 신은성 이력서 챗봇 사용해보기](https://watanka.github.io/AbotMe/)~~ (※Neo4j 무료 버젼을 사용하다보니, DB가 계속 죽는 문제가 있어서 링크는 지웁니다.)


# Features
- 업로드한 PDF 정보 기반 RAG 구성. 챗봇이 이력서 관련 내용을 답변 가능
- 챗봇 답변에 활용된 컨텍스트를 추적해 이력서 페이지에서 하이라이트로 확인 가능
- 업로드한 PDF 정보 기반 질문 생성하여 컨텍스트를 더 풍부하게 구성


## 프로젝트 목적
- 최대한 무료로 만들자
- 이력서는 자신이 했던 일들을 최대한 간략하고 보기 쉽게 만들어야한다. 그래서 이력서에 담기지 못한 내용들도 있다. 이 내용들을 챗봇이 컨텍스트를 이해하고 답변하도록 하자.
- 이력서에는 없지만, 이력서를 보는 사람들이 궁금해할만한 내용들이 뭐가 있을까?
    - 프로젝트/업무를 하면서 어려움을 겪었던 내용과 이를 어떻게 극복했는지.
    - 
    - 내가 전하고 싶은 Extra 정보



## 프로젝트 구성도
- **백엔드**: Python, FastAPI, Langchain, uv
- **프론트엔드**: React, pdf.js
- **데이터베이스**: Supabase, Neo4j Aura
- **서버**: Google Cloud Run
- **API**: Google Gemini API
- **CI/CD**: GitHub Actions

## 실행 방법

### 로컬 개발
```bash
# 백+프론트 실행
make dev
# 백엔드 실행
make backend
# 프론트 실행
make frontend
```

## 문서
- [요구사항](docs/requirements.md)
- [시스템 설계](docs/design.md)
- [코딩 원칙](docs/coding_principles.md)
- [Git 컨벤션](docs/git_conventions.md)
- [문서 작성 원칙](docs/documentation_principles.md)
- [테스트](docs/testing.md)
