# AbotMe

AI 챗봇 웹 애플리케이션입니다. 챗봇을 기반으로 사용자의 질문에 내 정보(개발자 신은성)를 제공합니다.

## 프로젝트 목적
- 다양한 데이터(PDF, GitHub, 블로그, LinkedIn 등) 기반으로 나를 소개하는 LLM 챗봇 제공
- React 기반 채팅 위젯으로 사용자 친화적 인터페이스
- FastAPI, Langchain, ChromaDB 등 최신 기술 활용
- GitHub Pages를 통한 무료 배포

## 폴더 구조

- backend: FastAPI, Langchain, ChromaDB 등 백엔드
- frontend: React + react-chat-widget 프론트엔드
- docs: 문서
- .github: GitHub Actions 등 워크플로우

## 기술 스택
- **프론트엔드**: React, react-chat-widget, TypeScript
- **백엔드**: Python, FastAPI, Langchain, ChromaDB, uv
- **배포**: GitHub Pages (프론트엔드), Docker (백엔드)
- **CI/CD**: GitHub Actions

## 실행 방법

### 로컬 개발
```bash
# 1. 백엔드 의존성 설치
make install

# 2. 코드 검사
make check

# 3. 백엔드 실행
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload

# 4. 프론트엔드 실행 (새 터미널)
cd frontend && npm install && npm start
```

### 도커로 전체 서비스 실행
```bash
docker-compose up --build
```

## 개발 프로세스

### 코드 품질 관리
```bash
make lint      # flake8으로 코드 검사
make test      # pytest로 테스트 실행
make check     # lint + test 모두 실행
make format    # black으로 코드 포맷팅
```

### 커밋 전 체크리스트
- [ ] `make check` 실행하여 모든 검사 통과
- [ ] 코드 포맷팅 적용 (`make format`)
- [ ] 테스트 코드 작성 및 실행

## 구조 다이어그램 (Mermaid)
```mermaid
graph TD
    A[React 채팅 위젯] --> B[FastAPI 서버]
    B --> C[LLM 엔진(Langchain)]
    B --> D[Vector DB(ChromaDB)]
    D --> E[내 정보 저장소]
    
    F[GitHub Pages] --> A
    G[도커/클라우드] --> B
```

## CI/CD
- GitHub Actions로 테스트/빌드/배포 자동화
- develop 브랜치에 push 시 워크플로우 실행
- flake8, pytest, Docker 빌드 자동 검사
- 프론트엔드 자동 배포 (GitHub Pages)

## 기여 가이드
- 브랜치/커밋/PR 컨벤션: docs/git_conventions.md 참고
- 테스트 코드 필수 (TDD 권장)
- 문서화 및 Mermaid 다이어그램 적극 활용
- 커밋 전 `make check` 실행 필수

## 문서
- [요구사항](docs/requirements.md)
- [시스템 설계](docs/design.md)
- [코딩 원칙](docs/coding_principles.md)
- [Git 컨벤션](docs/git_conventions.md)
- [문서 작성 원칙](docs/documentation_principles.md)

---
문의 및 피드백: [Issues](https://github.com/your-repo/AbotMe/issues)
