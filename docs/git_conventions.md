# Git 컨벤션

## 1. 브랜치 명명 규칙
- `feature/`: 새로운 기능 개발
  - 예: `feature/chat-interface`
- `bugfix/`: 버그 수정
  - 예: `bugfix/chat-response`
- `docs/`: 문서 관련 작업
  - 예: `docs/initial-setup`
- `refactor/`: 코드 리팩토링
  - 예: `refactor/api-structure`
- `hotfix/`: 긴급 수정
  - 예: `hotfix/security`

## 2. 커밋 메시지 규칙
### 형식
```
<타입>: <제목>

<상세 설명 (선택사항)>
```

### 타입
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 스타일 변경 (공백, 포맷팅)
- `refactor`: 코드 리팩토링
- `perf`: 성능 개선
- `test`: 테스트 추가/수정
- `chore`: 빌드 프로세스나 도구 수정

### 예시
```bash
# 올바른 예시
docs: 초기 프로젝트 설정 문서화

feat: 채팅 인터페이스 구현

fix: API 응답 타입 수정

# 피해야 할 예시
# - 타입 없음
# - 설명이 모호함
# - 영어/한글 혼용
```

## 3. PR 제목 규칙
- 명확하고 간결한 제목
- 영어 사용 권장
- 타입 포함 권장

### 예시
```
feat: 채팅 인터페이스 구현

fix: API 응답 타입 수정

docs: 초기 프로젝트 설정 문서화
```

## 4. PR 설명 규칙
### 필수 섹션
1. **목적**
   - PR의 목적을 간단히 설명

2. **변경사항**
   - 주요 변경사항 나열
   - 영향을 받는 파일/모듈

3. **테스트 방법**
   - 테스트 방법 및 검증 절차

### 선택적 섹션
1. **관련 이슈**
   - 연관된 이슈 링크

2. **Todo**
   - 후속 작업 사항

## 5. 이슈 관리
### 레이블 규칙
- `bug`: 버그
- `enhancement`: 기능 개선
- `feature`: 새로운 기능
- `documentation`: 문서 관련
- `good first issue`: 초보자에게 적합한 이슈
- `help wanted`: 도움이 필요한 이슈

### 상태 관리
- `open`: 진행 중
- `closed`: 완료
- `draft`: 초안

### 이슈 템플릿
```markdown
# 이슈 제목

## 문제 설명

## 영향 범위

## 해결 방안

## 관련 이슈
```
