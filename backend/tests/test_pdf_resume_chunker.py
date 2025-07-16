import csv
import os
from pathlib import Path

from app.data_pipeline.chunk.agentic_chunker import AgenticMetadataChunker
from app.data_pipeline.extract import PDFResumeMetadataExtractor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def test_resume_extractor_and_agentic_metadata_chunker_to_csv(
    sample_pdf_paths, tmp_path
):
    extractor = PDFResumeMetadataExtractor()
    # 실제 환경에 맞는 prompt_template, llm 인스턴스를 아래에 주입하세요
    tag_list = [
        "#personal",
        "#education",
        "#experience",
        "#project",
        "#tech_stack",
        "#achievement",
        "#certificate",
        "#award",
        "#timeline",
        "#summary",
    ]
    tag_guide = ", ".join(tag_list)

    prompt_template = ChatPromptTemplate.from_template(
        """
너는 지금부터 이력서 문서를 분석해서 의미 단위로 청킹(chunking)하고, 각 청크가 어떤 종류의 정보를 담고 있는지 태그(tag)도 함께 붙이는 역할을 맡았어.

💡 아래 기준을 반드시 지켜줘:

1. 이력서는 여러 개의 정보(경력, 학력, 프로젝트, 자격증 등)를 포함하고 있어.
2. 먼저 이 정보들을 큰 주제별로 나눠줘. 경력, 학력, 프로젝트, 자격증, 수상내역 등으로 나눠. 이걸 tag로 설정해주면 돼. **하나 이상의 태그(tags)** 를 붙여줘. 태그는 리스트 형태로 제공해. 태그 목록은 {tag_guide}이야.
3. 각 큰 주제에는 여러 개의 항목들이 들어있을 수 있어. 여러 회사, 학력, 프로젝트, 자격증, 수상내역 등이 있을 수 있어. 이걸 name으로 설정해주면 돼.
4. 이 여러 개의 항목들은 여러 개의 청크로 나뉠 수 있어. 예를 들어, A회사 경력은 'A회사'와 재직 기간 '2025.02 - 2025.05'까지가 될 수 있겠지. 이 나뉜 청크들은 전부 같은 tag와 name을 갖고 있어야해. 나중에 그룹핑하기 쉽도록.
5. 각 청크는 가능한 한 **하나의 주제나 사실**만을 담아야 해.
6. 이력서 정보는 (label_id와) (text) 형식으로 주어지며, label_id는 page_id-line_id로 구성되어있어. label_id와 text는 한 쌍으로 구성되어 있고, 나중에 데이터를 정렬할 때 필요한 정보야.
7. **최종 출력은 반드시 아래처럼 리스트로 출력**해.  
   - 코드블록(\`\`\`)이나 텍스트 설명 없이,  
   - 개행문자, 특수문자, 제어문자 없이  
   - 아래 예시처럼 한 줄로 출력해.

형식:
[
    (label_id, tags, name),
    ...
]
예시:
[
    (["1-1"], ["#personal"], "연락처"),
    (["1-2"], ["#personal"], "이메일"),
    (["2-4", "2-5"], ["#experience", "#project"], "엠지알", "소다")
]


이제 다음 이력서 정보를 보고 청크를 생성해줘:
{{input}}
""".format(
            tag_guide=tag_guide
        )
    )
    # llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE_URL"),
        model_name="deepseek/deepseek-chat:free",
    )

    chunker = AgenticMetadataChunker(prompt_template=prompt_template, llm=llm)

    csv_dir = Path("./tests/chunk_results")
    csv_dir.mkdir(exist_ok=True)
    for pdf_path in sample_pdf_paths:
        meta_list = extractor.extract(pdf_path)
        chunks = chunker.chunk(meta_list)
        pdf_name = Path(pdf_path).stem
        csv_path = csv_dir / f"{pdf_name}_agentic_chunks.csv"
        with open(csv_path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["chunk_index", "chunk_text", "tags", "name", "label_ids"])
            for i, chunk in enumerate(chunks, 1):
                writer.writerow(
                    [
                        i,
                        chunk["chunk_text"],
                        ",".join(chunk["tags"]),
                        chunk["name"],
                        ",".join(chunk["label_id"]),
                    ]
                )
        print(f"[INFO] CSV 저장 완료: {csv_path}")
        assert csv_path.exists() and csv_path.stat().st_size > 0
