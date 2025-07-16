import csv
import os
from pathlib import Path
import pytest
from app.data_pipeline.chunk.agentic_chunker import AgenticMetadataChunker
from app.data_pipeline.extract import PDFResumeMetadataExtractor
from app.data_pipeline.prompts import resume_prompt
from langchain_openai import ChatOpenAI

@pytest.mark.skip
def test_resume_extractor_and_agentic_metadata_chunker_to_csv(sample_pdf_paths):
    extractor = PDFResumeMetadataExtractor()
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

    prompt_template = resume_prompt
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
