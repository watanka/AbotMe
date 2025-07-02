.PHONY: help lint test check clean install

# 기본 타겟
help:
	@echo "사용 가능한 명령어:"
	@echo "  make install  - Python 의존성 설치"
	@echo "  make lint     - flake8으로 코드 검사"
	@echo "  make test     - pytest로 테스트 실행"
	@echo "  make check    - lint + test 모두 실행"
	@echo "  make clean    - 캐시 파일 정리"
	@echo "  make format   - black으로 코드 포맷팅"

# Python 의존성 설치
install:
	@echo "📦 Python 의존성 설치 중..."
	cd backend && . .venv/bin/activate && uv pip install -r requirements.txt

# 코드 린팅 (flake8)
lint:
	@echo "🔍 코드 린팅 중..."
	cd backend && . .venv/bin/activate && flake8 .

# 테스트 실행 (pytest)
test:
	@echo "🧪 테스트 실행 중..."
	cd backend && . .venv/bin/activate && pytest

# 전체 검사 (lint + test)
check: lint test
	@echo "✅ 모든 검사 통과!"

# 코드 포맷팅 (black)
format:
	@echo "🎨 코드 포맷팅 중..."
	cd backend && . .venv/bin/activate && black .

# 캐시 파일 정리
clean:
	@echo "🧹 캐시 파일 정리 중..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true 