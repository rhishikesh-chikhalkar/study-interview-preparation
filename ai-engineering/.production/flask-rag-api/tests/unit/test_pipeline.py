from flask_rag_api.core.pipeline import RAGPipeline


def test_pipeline_initialization():
    pipeline = RAGPipeline()
    assert pipeline.conversation_history == []
    assert pipeline.openai_client is None or hasattr(pipeline, "openai_client")


def test_history_management():
    pipeline = RAGPipeline()
    pipeline._update_history("Q1", "A1")
    history = pipeline.get_history()
    assert len(history) == 2
    assert history[0] == {"role": "user", "content": "Q1"}
    assert history[1] == {"role": "assistant", "content": "A1"}

    pipeline.clear_history()
    assert pipeline.get_history() == []
