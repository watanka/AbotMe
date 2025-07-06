.PHONY: help backend-install backend-lint backend-test backend-format backend-clean backend frontend dev


# 기본 타겟
help:
	@echo "사용 가능한 명령어:"
	@echo "  make backend-install  - Python 의존성 설치"
	@echo "  make backend-lint     - flake8으로 코드 검사"
	@echo "  make backend-test     - pytest로 테스트 실행"
	@echo "  make backend-check    - lint + test 모두 실행"
	@echo "  make backend-clean    - 캐시 파일 정리"
	@echo "  make backend-format   - black으로 코드 포맷팅"
	@echo "  make backend  - 백엔드 로컬 실행"
	@echo "  make frontend - 프론트엔드 로컬 실행"
	@echo "  make dev      - 백엔드&프론트엔드 로컬 실행"

# Python 의존성 설치
backend-install:

	@echo "📦 Python 의존성 설치 중..."
	cd backend && . .venv/bin/activate && uv pip install -r requirements.txt

# 코드 린팅 (flake8)
backend-lint:
	@echo "🔍 코드 린팅 중..."
	cd backend && . .venv/bin/activate && flake8 .

# 테스트 실행 (pytest)
backend-test:
	@echo "🧪 테스트 실행 중..."
	cd backend && . .venv/bin/activate && pytest

# 코드 포맷팅 (black)
backend-format:
	@echo "🎨 코드 포맷팅 중..."
	cd backend && . .venv/bin/activate && black .

# 캐시 파일 정리
backend-clean:
	@echo "🧹 캐시 파일 정리 중..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true

backend-build:
	@echo "📦 도커 이미지 빌드 중..."
	cd backend && uv pip freeze > requirements.txt && docker build -t eshin94/abotme:latest .

backend-image-push:
	@echo "🚀 도커 이미지 푸시 중..."
	cd backend && docker push eshin94/abotme:latest

backend-image-pull:
	@echo "🚀 도커 이미지 풀링 중..."
	docker pull eshin94/abotme:latest

backend-image-run:
	@echo "🚀 도커 이미지 실행 중..."
	docker run --rm --name abotme-backend -p 8000:8000 eshin94/abotme:latest


backend:
	cd backend && set -a && [ -f .env ] && set +a && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

frontend:
	cd frontend && set -a && [ -f .env ] && set +a && npm run start

dev:
	$(MAKE) -j2 backend frontend