# 시스템 설계 문서

## 1. 시스템 아키텍처
```mermaid
graph TD
    A[웹 클라이언트] --> B[FastAPI 서버]
    B --> C[LLM 엔진]
    B --> D[Vector DB]
    D --> E[내 정보 저장소]
    
    subgraph 외부 서비스
        F[Github]
        G[LinkedIn]
        H[블로그]
    end
    
    F --> E
    G --> E
    H --> E
```

## 2. 기술 스택
### 프론트엔드
- React + TypeScript
- Tailwind CSS
- Shadcn/ui
- react-hook-form

### 백엔드
- FastAPI
- Python 3.11+
- uv (Python 라이브러리 관리)

### LLM
- Langchain

### 데이터베이스
- ChromaDB (Vector DB)
- SQLite (메타데이터 저장)

### 인프라
- Docker
- GitHub Pages
- GitHub Actions

## 3. 컴포넌트 구조
```mermaid
graph TD
    A[프론트엔드]
    B[백엔드]
    C[LLM 엔진]
    D[Vector DB]
    E[인프라]
    
    A --> A1[컴포넌트]
    A --> A2[상태 관리]
    A --> A3[API 클라이언트]
    
    B --> B1[API 라우터]
    B --> B2[비즈니스 로직]
    B --> B3[데이터 액세스]
    
    C --> C1[프롬프트 엔진]
    C --> C2[안전성 검사]
    
    D --> D1[데이터 인덱싱]
    D --> D2[유사도 검색]
    
    E --> E1[CI/CD]
    E --> E2[배포 자동화]
```

## 4. 데이터 흐름
```mermaid
sequenceDiagram
    participant 클라이언트
    participant API서버
    participant VectorDB
    participant LLM
    
    클라이언트->>API서버: 질문 전송
    API서버->>VectorDB: 유사도 검색
    VectorDB-->>API서버: 관련 문서 반환
    API서버->>LLM: 프롬프트 생성 및 전송
    LLM-->>API서버: 답변 생성
    API서버-->>클라이언트: 답변 전송
```

## 5. 배포 전략
### CI/CD 파이프라인
```mermaid
graph TD
    A[Push Event]
    B[Linting]
    C[Test]
    D[Build]
    E[Deploy]
    
    A --> B
    B --> C
    C --> D
    D --> E
```

### 배포 환경
- 개발: 로컬 Docker
- 테스트: GitHub Actions
- 프로덕션: GitHub Pages

## 6. 보안 고려사항
1. 입력 검증
   - XSS 공격 방지
   - SQL Injection 방지
   - LLM 안전성 검사

2. API 보안
   - Rate limiting
   - API 키 관리

3. 데이터 보안
   - 민감 정보 암호화
   - 로그 관리
   - 접근 제어

## 7. 모니터링 및 로깅
### 사용자 행동 모니터링
   - Langfuse를 활용하여 사용자 질문을 모니터링한다.
   - 질문 패턴 분석
   - 자주 사용되는 기능
   - 오류 발생 패턴
