# AbotMe
AI 챗봇 웹 애플리케이션입니다. 챗봇을 기반으로 사용자의 질문에 내 정보(개발자 신은성)를 제공합니다.  

## 데모 영상
<iframe width="560" height="315" src="https://www.youtube.com/embed/93ThYTHi6wY" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


<a href="https://watanka.github.io/AbotMe/" target="_blank" style="
  display: inline-block;
  padding: 0.45em 1em;
  font-size: 0.98em;
  font-weight: bold;
  color: #fff;
  background: linear-gradient(90deg, #4f8cff 0%, #6dd5ed 100%);
  border-radius: 999px;
  box-shadow: 0 1px 4px rgba(79,140,255,0.13);
  text-decoration: none;
  margin: 8px 0;
  transition: background 0.2s;
">
🚀 신은성 이력서 챗봇 사용해보기
</a>


# Features
- 업로드한 PDF 정보 기반 RAG 구성. 챗봇이 이력서 관련 내용을 답변 가능
- 챗봇 답변에 활용된 컨텍스트를 추적해 이력서 페이지에서 하이라이트로 확인 가능
- 업로드한 PDF 정보 기반 질문 생성하여 컨텍스트를 더 풍부하게 구성


## 프로젝트 목적
- 최대한 무료로 만들자



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
