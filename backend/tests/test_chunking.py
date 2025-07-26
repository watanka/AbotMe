import json
import os
import pytest
from app.data_pipeline.chunk.agentic_chunker import AgenticMetadataChunker
from app.data_pipeline.extract import PDFResumeMetadataExtractor
from app.data_pipeline.prompts import resume_prompt
from langchain_google_genai import ChatGoogleGenerativeAI


@pytest.mark.skip(reason="실제 llm 사용")
def test_chunking(sample_pdf_paths):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API_KEY")
    )
    extractor = PDFResumeMetadataExtractor()
    chunker = AgenticMetadataChunker(prompt_template=resume_prompt, llm=llm)
    for sample_pdf_path in sample_pdf_paths:

        meta_list = extractor.extract(sample_pdf_path)
        chunks = chunker.chunk(meta_list)
        result_chunks = [
            [
                {
                    "tags": t["tags"],
                    "name": t["name"],
                    "chunk_text": meta_list[t["label"]]["text"],
                }
                for t in text_info
            ]
            for text_info in chunks
        ]

        file_name = os.path.splitext(os.path.basename(sample_pdf_path))[0]
        with open(f"./tests/chunk_results/{file_name}.json", "w") as f:
            json.dump(result_chunks, f, indent=4, ensure_ascii=False)
