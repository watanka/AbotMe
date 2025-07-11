# LLM 기반 이력서 어플리케이션 백엔드 API 명세서

## 개요
- 이력서 업로드, 질문 생성, 답변 저장, 이력서/챗봇 조회 등 주요 기능을 담당하는 FastAPI 기반 백엔드 API 설계 문서
- 관리자 전용 URL과 공개 URL의 권한 분리 정책을 반영

---

## 1. 인증 및 권한
- **edit_token**: 관리자 전용 endpoint 접근 시 필요 (쿼리 파라미터 또는 헤더)
- 공개 endpoint는 edit_token 없이 접근 가능

---

## 2. 주요 엔드포인트 (2025-07-10 기준)

### [관리자 전용] 이력서 업로드
- `POST /resume`
  - 설명: 이력서(PDF) 파일 업로드 및 신규 등록 (기존 이력서 덮어쓰기)
  - 요청: `multipart/form-data` (file, name, email)
  - 응답: `{ edit_token, public_url }`
  - 권한: edit_token 필요 없음(최초 등록)

### [공개] 이력서/질문/답변 데이터 조회
- `GET /resume`
  - 설명: 이력서, 질문, 답변, 소유자 정보 등 전체 데이터 조회
  - 요청: 없음
  - 응답: `{ resume_pdf_url, questions, answers, name, email }`
  - 권한: 공개

### [관리자 전용] 질문 자동 생성
- `POST /resume/generate-questions`
  - 설명: 업로드된 이력서 기반 LLM 질문 자동 생성. 기존 업로드된 이력서가 없다면 에러 반환
  - 요청: `edit_token` (form-data)
  - 응답: `{ questions: [ {question_id: question_text}, ... ] }`
  - 권한: edit_token 필요

### [관리자 전용] 단일 질문 조회
- `GET /resume/questions/{question_id}`
  - 설명: 특정 질문 1개 조회
  - 요청: `edit_token` (form-data)
  - 응답: `question_text`
  - 권한: edit_token 필요

### [관리자 전용] 답변 저장 (질문별 1대1)
- `POST /resume/questions/{question_id}/answer`
  - 설명: 특정 질문에 대한 답변 저장
  - 요청: `edit_token`, `answer` (form-data)
  - 응답: `{ success: true }`
  - 권한: edit_token 필요

### [공개] 챗봇 질의
- `POST /resume/chat`
  - 설명: 챗봇에 질문 → 답변, 하이라이트, 꼬리질문 등 반환 (이력서 context 활용)
  - 요청: `{ message }` (body)
  - 응답: `{ answer, highlights, suggestions }`
  - 권한: 공개

---

## 3. 데이터 구조 예시

- **질문**: `[ {question_id: question_text}, ... ]` (ex: `[ {"abcd-uuid": "질문내용"}, ... ]`)
- **답변**: `{ question_id: answer, ... }`

---

## 4. 엔드포인트 요약표
| Method | Endpoint | 권한 | 설명 |
|--------|----------|------|------|
| POST   | /resume | (최초) | 이력서 업로드/등록 |
| GET    | /resume | 전체 | 이력서/질문/답변 데이터 조회 |
| POST   | /resume/generate-questions | 관리자 | 질문 자동 생성 |
| GET    | /resume/questions/{question_id} | 관리자 | 단일 질문 조회 |
| POST   | /resume/questions/{question_id}/answer | 관리자 | 답변 저장(1대1) |
| POST   | /resume/chat | 전체 | 챗봇 질의 |
| GET    | /resume/{resume_id} | 전체 | 이력서/챗봇 데이터 조회 |
| POST   | /resume/{resume_id}/chat | 전체 | 챗봇 질의 |

---

## 4. 보안/운영 주의사항
- edit_token은 안전하게 저장/전송, 공개 URL에는 절대 포함하지 말 것
- 관리자 endpoint는 edit_token 미포함 시 403 반환
- 공개 endpoint는 누구나 접근 가능

---
(2025-07-10 기준 최신 설계 반영)
