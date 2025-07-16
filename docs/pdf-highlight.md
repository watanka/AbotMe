## PDF highlight에 필요한 백엔드 정보

### extract
- PDF Extraction 단계에서 텍스트와 함께 필요한 메타정보를 추출해야함
- Extractor 인터페이스를 구현. `extract` 함수 구현.
- 메타정보: page_id, bbox, text, label_id(1-2, 첫째줄 2번째 단어)
- extract 단계 후에는 RAG에 참고할 벡터 스토어 저장을 위한 청킹 단계를 거치게 됨. 청킹 단계 후에도 각 청크마다 필요한 메타정보가 포함될 수 있도록 구성해야함. 예를 들어, 같은 줄에 'oo고등학교', 'oo대학교'가 있고, 서로 다른 청크로 쪼개졌을 때, 'oo고등학교'의 bbox좌표와 'oo대학교'의 bbox좌표가 알맞게 설정될 수 있어야함. 이를 위해서 띄어쓰기 단위로 메타정보가 구성될 수 있도록 설정해야함.

### chunk
- LLM 기반 청크 진행
- 전체 이력서 정보를 넘겨서 맥락을 파악하게 함.
- 청크를 구분하는 방법
  - 계층적 청킹 
    - 개인정보, 학력, 이력, 수상정보, 프로젝트, 기술스택, 기타 등으로 우선 구분함. 그 안에 세부 항목들로 구분함
    
- 결과로 extract 단계에서 나온 메타 정보가 유지되어야함.


### tag
- 미리 정의해둔 이력서 태그 항목에 따라 청크를 태깅
  - #personal
  - #education
  - #experience
  - #project
  - #tech_stack
  - #achievement
  - #certificate
  - #award
  - #timeline
  - #summary



### 저장 스키마

#### 1. PDFResumeMetadataExtractor의 출력 (meta_list)
- **타입:** Dict[str, Dict]
- **예시:**
  ```python
  {
    "1-1": {
      "page_id": 1,
      "label_id": "1-1",
      "text": "홍길동",
      "bbox": [x0, top, x1, bottom]
    },
    ...
  }
  ```
  - 각 label_id는 "페이지번호-단어순번" 형식
  - bbox는 (좌상단x, 상단y, 우하단x, 하단y) 좌표 (추후 0~1 정규화 필요)

#### 2. AgenticTextChunker의 출력
- **타입:** List[str]
- **예시:**
  ```python
  [
    "홍길동은 서울대학교를 졸업하고 ...",
    "삼성전자에서 3년간 소프트웨어 엔지니어로 근무 ...",
    ...
  ]
  ```

#### 3. AgenticMetadataChunker의 출력 (chunks)
- **타입:** List[Dict]
- **예시:**
  ```python
  [
    {
      "label_id": ["1-1", "1-2"],
      "tags": ["#personal"],
      "name": "이메일",
      "chunk_text": "홍길동 이메일"
    },
    ...
  ]
  ```
  - label_id: 해당 chunk에 포함된 label_id(들)
  - tags: LLM이 부여한 태그 리스트
  - name: 대표 엔티티명
  - chunk_text: chunk에 포함된 전체 텍스트

#### 4. VectorStoreSaver 및 구현체(예: ChromaVectorStoreSaver)에 저장되는 형식
- **AgenticTextChunker 사용 시:**  각 chunk(str) 단위로 저장
- **AgenticMetadataChunker 사용 시:**
  - 각 chunk(dict) 단위로 저장하며, 반드시 메타정보(예: label_id, tags, name, chunk_text 등) 전체를 벡터스토어의 메타데이터로 함께 저장해야 함
  - 예시 (Chroma 기준):
    ```python
    collection.upsert(
      documents=[chunk["chunk_text"]],
      metadatas=[{
        "label_id": chunk["label_id"],
        "tags": chunk["tags"],
        "name": chunk["name"],
        ...
      }],
      ids=[f"resume-{i}"]
    )
    ```

---

### 프론트엔드 하이라이트 구현 (2025-07-16)

#### 데이터 흐름 및 구조
- ChatBot이 백엔드로부터 받은 metadata(하이라이트 정보)를 HomePage의 상태(highlights)로 올려서 ResumeViewer에 전달
- highlights는 각 항목이 `{ x0, x1, top, bottom, page_id, ... }` 형태로, bbox 없이 좌표 필드가 최상위에 위치
- ResumeViewer는 현재 pageNumber에 해당하는 highlight만 필터링하여 PdfDocument에 전달
- PdfDocument는 react-pdf의 <Page> 위에 HighlightOverlay를 absolute div로 렌더링
- 좌표 변환: PDF 원본 width/height와 렌더링 width/height를 비율로 환산하여 하이라이트 위치/크기 변환

#### UI/UX 개선
- TailwindCSS로 하이라이트 스타일 개선:
    - 배경색: 밝은 형광 노랑(`backgroundColor: rgba(255,255,80,0.45)`)
    - 테두리(border) 제거, 그림자(`shadow`), 둥글기(`rounded-xl`), 트랜지션(`transition-all duration-200`) 적용
    - 면적은 width/height 15% 확장하여 더 넓게, left/top도 보정
    - pointer-events-none으로 PDF 조작에 영향 없음
- 하이라이트가 실시간으로 챗봇 응답에 반영되어 UX가 자연스러움

#### 코드 예시 (핵심)
```jsx
<div
  className="absolute pointer-events-none rounded-xl shadow transition-all duration-200"
  style={{
    left, top, width, height, // 변환 및 확장 적용
    backgroundColor: "rgba(255,255,80,0.45)",
    zIndex: 10,
  }}
/>
```

#### 데이터 전달 구조
- HomePage: `[highlights, setHighlights]` 상태로 관리, `<ChatBot onMetadata={setHighlights} />`
- ChatBot: metadata를 받으면 onMetadata(metadata)로 전달
- ResumeViewer: `highlights` prop으로 전달받아 하이라이트 렌더링

---

### LLM/백엔드 데이터 흐름 및 오류 대응

#### LLM Output Parsing 오류 사례
- LLM이 생성한 JSON 중 일부 항목이 Pydantic 모델(ResumeChunkList) 스키마와 맞지 않아 파싱 실패
- 예: `{ 'label_id': '2-29', 'tags': ['#timeline], '] }` → "name" 필드 누락, "tags" 문법 오류
- 해결책:
    - 프롬프트에 각 항목에 반드시 "name" 필드 포함, "tags"는 올바른 JSON 배열로 생성하도록 명시
    - 파싱 전 데이터 검증/보정 코드 추가(누락 필드 빈 문자열 대체, tags JSON 파싱 오류 복구 등)
    - OutputParser에 strict 옵션이 있다면 완화 적용(일부 데이터 손실 위험)

#### 참고
- LangChain Output Parsing Failure 공식 문서: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE
- Pydantic ValidationError 공식 문서: https://errors.pydantic.dev/2.11/v/missing

---

### 테스트 케이스
PDF에서 추출 가능한 좌표 정보 확인용 유닛 테스트 작성
- pdfplumber를 사용하여 PDF에서 좌표 정보가 어떤 식으로 나오는지 확인
- 여러 개의 PDF 유형들을 테스트하고, 좌표 정보가 정상적으로 추출되는지 확인
- pdf 추출 정보의 데이터 구조를 어떻게 구성할 건지 테스트

