# 이력서 챗봇 AbotMe


## 기능 설명
- 이력서 정보 기반 챗봇
- 추가적인 문맥을 제공할 수 있는 QnA 세션
- 챗봇 관련 답변에 가독성을 위한 하이라이트 표기

이력서를 업로드 -> 이력서 파싱 -> 위치, 태그 메타정보 저장  
            -> 챗봇 -> 이력서 기반 질문에 답변
            -> 질문 생성 -> 질문별 답변 제출 -> 벡터 스토어 저장 -> 더 상세한 답변 가능
            

답변이 길어지면, 답변 형식 Pydantic Model Validation 에러가 발생함. 누락되는 tag가 발생하는 문제 
-> API요청을 나눌 수 있도록 처리. 


## 개발 과정
- 바이브 코딩을 적극적으로 활용했습니다.
바이브 코딩을 몇 번 실패해본 이후, 필요한 정보들과 컨텍스트를 제공해주는 것이 중요하다는 걸 알게 되어 LLM에게 요구하는 내용들은 정보를 얻은 후 문서로 정리하고자 했습니다.   

coding_principles.md, design.md, requirements.md, usage.md, git_conventions.md 등으로 크게 문서 종류를 나누고 시작했습니다. coding_principles는 AI가 코드를 작성할 때 준수해야할 코딩 원칙(SOLID, 변경사항은 최소한으로, 중복 코드는 X 등)을 담았고, requirements에는 구현하려는 기능에 대한 명세와 그에 따른 최소 요구사항을 담았습니다. design은 전체 프로세스 동작방식, 코드 구조, UI 명세 등 전체적으로 어떻게 코드가 동작하는지 담았습니다. 마지막으로 usage에는 사용자에게 어떻게 사용하는지에 대한 명세를 담았습니다. 그리고, git_conventions에는 브랜치와 커밋 작업 단위를 설명해서, 많은 코드를 한 번에 작성하는 것이 아닌 제가 관리할 수 있는 범위 내에서 커밋 체크포인트를 나눠서 작업하도록 했습니다.(AI가 한 번에 작성한 코드를 계속해서 무지성으로 accept하다보면, 어느 순간에는 더 이상 감당할 수 없이 코드가 커져버려 관리하기 힘들게 되더라구요.) 이렇게 구성해놓으면, 개발을 하면서 추가되는 사항이 있어도 어느 정도 정리된 상태로 문서를 관리할 수 있다고 생각했습니다.  


(windsurf를 사용 중)AI에 코드 작성을 요청할 때마다 필요한 문서들을 태그(@)하여 추가해주니 문맥을 잘 이해해서 작성해주었습니다.
하지만, 분명한 건 더 빠르고 효율적으로 AI를 활용할 수 있을 거라는 생각이 들었습니다.


먼저 이렇게 크게만 나눠놓고 시작하니, 변경사항이 생길 때마다 관리하기 조금 어렵다는 느낌이 들었습니다. 나눠 놓은 카테고리에 새로운 문서를 끼워맞추려다보니 조금씩 핀트가 나가는 느낌을 받았습니다. 문서의 depth를 맞추는 게 어렵달까요..? 위에 나눈 문서들 외에도 개발을 하다보니, 추가적으로 필요한 문서들이 있었습니다. Frontend, LLM, 백엔드 등이 어떻게 동작하는지를 design 문서에다가 전부 담기에는 문서 양이 너무 커진다는 생각이 들었습니다. 그래서 개발을 하면서 frontend, llm_details, 백엔드 기능들(llm_details, pdf-highlight, qna) 관련 문서를 추가했습니다. 이 문서들을 다시 `details` 폴더를 두어 정리를 할 수는 있겠지만, 뭔가 더 나은 방법도 있을 거라는 생각이 들었습니다.

AI와 인터랙트하면서 중요한 점은 필요한 정보 제공과 AI가 처리할 수 있는 정보량 사이의 미세한 trade-off를 잘 조절하는 것이라고 생각이 들었습니다. 필요한 정보가 부족하면, AI가 사용자의 의도에 알맞은 답변을 내놓을 확률이 떨어지게 되고, 반대로 정보가 너무 많아도 AI가 처리할 수 있는 범위를 벗어나게 되어 수행능력이 떨어질 수 있습니다(context rot). 필요한 컨텍스트만 최소한으로 제공하는 것이 중요하죠.



다른 사람들의 문서 작성 방법을 적극적으로 참조하기로 했습니다.
TaskMasterAI가 어떤 식으로 문서를 작성하는지 확인했습니다.
PRD(Product Requirements Document)를 작성하고, 태스크들을 여러 태스크들로 분류합니다. 



### 
metadata 저장
이력서 -> chunk -> labeling -> db에 metadata와 함께 저장 
question -> labeling -> metadata 기준 먼저 parsing

metadata로만 사용자 질문과 답변 컨텍스트를 매칭하기에는 한계가 있음
다양한 질문들이 들어올 수 있기 때문








그래프 DB 구성
- vector db -> 그래프 db 이유
이력서 저장 단위를 어떻게 설정하는지에 따라 다름.
사용자의 질문에 벡터 유사도만으로 평가하는 것은 벡터 스토어 저장 단위 이상의 컨텍스트를 인식하지 못 한다는 단점이 있음.
예를 들어, '프로젝트A에 대해 알려줘'에 대해서는 잘 답변할 수 있지만, '사용자가 진행한 프로젝트들에 대해 전부 알려줘'라는 질문에 대해서는 답변할 수 없음.
그래프 DB는 node와 relationship을 통해 구조화된 컨텍스트를 제공하여 이러한 문제를 해결할 수 있음.


https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html#user-guide-rag

- 저장
    - 이력서 정보 -> 그래프 구조
    - chunk -> extract -> enrich
    - neo4j에 vector 구성?
    - agentic traversal




- 쿼리
    - 텍스트 쿼리 -> 그래프 쿼리
    - local, global
    - page rank, link prediction, community detection
    - agentic loop with tool calling

- QnA -> 그래프 보강
- 평가

Text2CypherRetriever 사용.
노드의 이름과 완전 일치하지 않을 경우, cypher 쿼리가 동작하지 않는 문제 발생.
사용자 쿼리
"파이썬 사용한 프로젝트들 알려줘"
변환된 Cypher
MATCH (p: Project)-[:USES]->(t: TechStack { name: "파이썬" }) RETURN p
결과 None. TechStack name이 python으로 저장되어있음

회사
프로젝트
기술 스택
활동
자격증

company_emb_index
project_emb_index
techstack_emb_index
activity_emb_index
achievement_emb_index
certificate_emb_index

각 노드들에 대한 임베딩 인덱스를 만들어, 이름이 완전 일치하지 않더라도 노드를 찾을 수 있도록 구성

text2cypher 시에 index를 활용해서 노드를 찾고, 그 후에 cypher 쿼리를 수행한다.

Project BELONGS_TO Company
Project USES TechStack


extract 단계, chunk 단계, write 단계
Graph가 Vector DB보다 더 좋은 이유
- 더 큰 맥락을 불러올 수 있다.
- 벡터 유사도 검색은 청크 단위의 데이터를 질문과 비슷한 정도로 불러옴. 여기서 불러온 데이터들을 rerank하거나 조합해서 처리하는 방식.
-> 아닌가? 더 있나? 벡터 RAG 종류에 대해서 더 살펴보는 것은 어떨까?
- [ ] RAG종류
- [ ] 엘라스틱서치를 활용한 벡터 검색 실무 가이드


각 테스트 구성

# Vector DB Filter Evaluation

이 프로젝트에서는 **Vector DB 검색 과정에서 filter 적용 유무에 따른 효과**를 검증했습니다.  

## 실험 개요
- **데이터셋**: 직접 검수를 거친 104개의 질문–응답 쌍 (`abotme-rag-test-dataset`)  
- **평가 방법**: [LangSmith OpenEval](https://smith.langchain.com/)의 **Correctness** 지표  
- **실험 조건**:  
  1. **Without Filter**: 단순 벡터 검색 결과 기반 응답  
  2. **With Filter**: 질의어를 전처리하여 `chunk_type` 등 메타데이터 기반 filter 적용  

## 평가 목적
- Vector DB 검색 시 **필터링 유무가 LLM 응답의 정확도(correctness)에 미치는 영향** 검증  
- 실제 서비스 환경에서 필터 전략을 적용했을 때의 효과성을 확인  

## 실험 환경
- **LLM**: OpenAI `o3-mini`  
- **Vector DB**: Chroma + Gemini Embedding  
- **RAG Engine**: 검색 결과를 컨텍스트로 활용해 답변 생성  

## 결과 요약
- **With Filter**: 특정 문맥(`experience` 등)에 집중 → 더 정밀한 응답 생성  
- **Without Filter**: 검색 결과가 넓어져 불필요한 문맥 포함 가능성 ↑  
- **Trade-off**:  
  - 필터 적용 시 P50 6.04s, P99 12.17s, 필터 없이 P50 6.06s, P99 14.14. (필터 적용을 할 경우 추가적인 api 호출이 발생하는데도 불구하고 필터 적용 P99가 더 짧은 건 API 호출 자체의 차이인듯 하다.)
  - **Correctness 지표에서 약 2% 개선**이 확인됨  
  - 

## 평가 스크린샷
(📸 LangSmith 평가 대시보드 스크린샷 추가 예정)

맞았는데, 틀리고
틀렸는데, 맞았다고 한 항목들이 있다.

---

### 결론
이번 실험을 통해 **필터 기반 검색이 RAG 시스템의 응답 정확도를 향상**시킬 수 있음을 확인했습니다.  
다만, 성능(속도)과 정확도 간의 트레이드오프가 존재하므로, 서비스 환경에 맞는 최적의 필터 전략을 설계하는 것이 중요합니다.  
향후에는 필터링 전략을 세분화하여 다양한 유형의 쿼리에서도 최적의 검색 성능을 낼 수 있도록 확장할 계획입니다.  
