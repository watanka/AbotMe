import pytest
from app.data_pipeline.chunk.agentic_chunker import AgenticTextChunker
from app.data_pipeline.prompts import chat_prompt, resume_prompt
from app.data_pipeline.write.chroma_writer import ChromaVectorStoreWriter
from app.dependencies import get_llm, get_text_extractor
from app.llm.preprocess_query import preprocess_query
from app.llm.rag_engine import RAGEngine
from app.llm.vector_store.chroma import ChromaVectorStore
from app.llm.vector_store.embedding.gemini import GeminiEmbeddingModel
from langsmith import Client, evaluate, traceable
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT


def test_벡터DB사용시_필터_유무에_따른_성능_평가():
    chroma = ChromaVectorStore("test_db", GeminiEmbeddingModel())
    llm = get_llm()
    rag_engine = RAGEngine(chroma, chat_prompt, llm)
    EXPERIMENT_NAME = "vector_db_with_out_filter"

    # 1. Create and/or select your dataset
    client = Client()
    dataset_name = "abotme-rag-test-dataset"

    def correctness_evaluator(inputs: dict, outputs: dict, reference_outputs: dict):
        evaluator = create_llm_as_judge(
            prompt=CORRECTNESS_PROMPT,
            model="openai:o3-mini",
            feedback_key="correctness",
        )
        eval_result = evaluator(
            inputs=inputs, outputs=outputs, reference_outputs=reference_outputs
        )
        return eval_result

    @traceable
    def get_answer(inputs: dict):
        query = inputs["question"]
        raw_context = rag_engine.retrieve_context(query)
        context = "\n".join(
            [
                (
                    chunk.metadata.get("search_summary", "")
                    if hasattr(chunk, "metadata")
                    else ""
                )
                for chunk in raw_context
            ]
        )
        answer_no_filter = "".join(
            getattr(c, "content", str(c))
            for c in rag_engine.generate_answer(query, context)
        )
        return answer_no_filter

    @traceable
    def get_answer_with_filter(inputs: dict):
        query = inputs["question"]
        filter_dict = preprocess_query(query)
        raw_context = rag_engine.retrieve_context(query, filter_dict=filter_dict)
        context = "\n".join(
            [
                (
                    chunk.metadata.get("search_summary", "")
                    if hasattr(chunk, "metadata")
                    else ""
                )
                for chunk in raw_context
            ]
        )
        answer_with_filter = "".join(
            getattr(c, "content", str(c))
            for c in rag_engine.generate_answer(query, context)
        )
        return answer_with_filter

    evaluate(
        get_answer_with_filter,
        data=dataset_name,
        evaluators=[correctness_evaluator],
        experiment_prefix="abotme-rag-test-dataset-with-filter",
    )


@pytest.mark.skip
def test_벡터DB에_이력서를_저장한다():
    llm = get_llm()
    vector_store = ChromaVectorStore("test_db", GeminiEmbeddingModel())
    extractor = get_text_extractor()
    chunker = AgenticTextChunker(template=resume_prompt, llm=llm)
    vectorstore_writer = ChromaVectorStoreWriter(vector_store)

    extracted = extractor.extract(
        "/home/silver/workspace/AbotMe/backend/assets/신은성-이력서.pdf"
    )
    chunk_list = chunker.chunk(extracted)
    vectorstore_writer.save(chunk_list)
