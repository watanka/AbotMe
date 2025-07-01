# AbotMe

AI 챗봇 웹 애플리케이션입니다. 챗봇을 기반으로 사용자의 질문에 내 정보(개발자 신은성)를 제공합니다.

## 🚀 기술 스택

### 프론트엔드
- React + TypeScript
- Tailwind CSS
- Shadcn/ui
- react-hook-form

### 백엔드
- FastAPI
- Python 3.11+
- uv (Python 라이브러리 관리)

### 데이터베이스
- ChromaDB (Vector DB)
- SQLite (메타데이터 저장)

### 인프라
- Docker
- GitHub Pages
- GitHub Actions

## 🛠️ 설치 및 실행

### 프론트엔드
```bash
# 프론트엔드 디렉토리로 이동
cd src/frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

### 백엔드
```bash
# 백엔드 디렉토리로 이동
cd src/backend

# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uv run app:app
```

## 📝 문서
- [코딩 원칙](docs/coding_principles.md)
- [문서 작성 원칙](docs/documentation_principles.md)
- [요구사항](docs/requirements.md)
- [시스템 설계](docs/design.md)

## 📝 라이선스
MIT License
