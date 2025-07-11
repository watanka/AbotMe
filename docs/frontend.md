# AbotMe 프론트엔드 UI/UX 설계

## 1. 전체 프로세스 도식

![AbotMe 프로세스](images/abme_process.svg)

- **이력서 업로드**: PDF drag & drop, 이름/이메일 입력
- **질문 생성/답변**: LLM 기반 자동 질문 생성, 질문별 답변/저장, 미입력 시 워닝
- **이력서 보기 & 챗봇**: PDF 전체 렌더링, 챗봇, 질문 관련 하이라이트

---

## 2. 주요 화면 와이어프레임

- **이력서 업로드**: [frontend_wireframe_upload.svg](images/frontend_wireframe_upload.svg)
- **질문 생성/답변**: [frontend_wireframe_questions.svg](images/frontend_wireframe_questions.svg)
- **이력서+챗봇**: [frontend_wireframe_resume_chat.svg](images/frontend_wireframe_resume_chat.svg)

---

## 3. 기타
- 모든 SVG는 Figma, VSCode, 브라우저 등에서 확인 가능
- Tailwind CSS, shadcn/ui 스타일을 기반으로 실제 컴포넌트 구현 권장
- PDF.js 등과 연동 시 하이라이트는 줄 단위 overlay로 구현

## 4. 개발 단계
- PDF 뷰어 연동
- 챗봇 UI 구현
- 중간점검 
- 이력서 업로드 페이지 구현
- 질문 생성/답변 페이지 구현
- PDF 뷰어와 챗봇 질문에 맞춘 하이라이트 구현