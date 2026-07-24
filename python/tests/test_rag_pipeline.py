import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

# Ensure our imports work correctly by adding the target directory directly
sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent.parent / "ai-engineering" / "rag")
)

from rag_pipeline import RAGPipeline


@pytest.fixture
def mock_openai_client():
    with patch("rag_pipeline.OpenAI") as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance
        yield mock_instance


def test_rag_pipeline_init_without_key():
    with (
        patch.dict("os.environ", {}, clear=True),
        patch("rag_pipeline.api_key", None),
    ):
        pipeline = RAGPipeline()
        assert pipeline.openai_client is None


def test_rag_pipeline_chunk_documents():
    pipeline = RAGPipeline()
    pages_data = [
        {
            "text": "Hello world. This is a simple test document page for RAG pipeline chunking verification.",
            "metadata": {"source": "test.pdf", "page": 1},
        }
    ]

    # Use small chunk size to force splitting
    chunks = pipeline.chunk_documents(pages_data, chunk_size=20, chunk_overlap=5)

    assert len(chunks) > 0
    for chunk in chunks:
        assert "text" in chunk
        assert "metadata" in chunk
        assert chunk["metadata"]["source"] == "test.pdf"
        assert chunk["metadata"]["page"] == 1
        assert "chunk_index" in chunk["metadata"]


def test_get_embedding_fallback():
    # When OpenAI is not configured, get_embedding should return mock float values
    with patch("rag_pipeline.api_key", None):
        pipeline = RAGPipeline()
        embedding = pipeline.get_embedding("test query text")
        assert isinstance(embedding, list)
        assert len(embedding) == 1536
        assert all(isinstance(x, float) for x in embedding)


def test_chroma_and_retrieval_flow():
    # Use EphemeralClient for tests to avoid disk I/O and keep tests fast
    pipeline = RAGPipeline()
    collection = pipeline.create_or_get_collection("test_rag_flow_collection")

    chunks = [
        {
            "text": "OpenAI provides advanced language models.",
            "metadata": {"source": "docs.pdf", "page": 1, "chunk_index": 0},
        },
        {
            "text": "ChromaDB is a database designed for AI embeddings.",
            "metadata": {"source": "docs.pdf", "page": 1, "chunk_index": 1},
        },
    ]

    # Populate vector store
    pipeline.populate_vector_store(chunks, collection)

    # Query vector store
    results = pipeline.query_vector_store("ChromaDB vector store", collection, k=1)

    assert len(results) == 1
    # Check that it retrieved the most semantically relevant one (our mock embedding seeds on hash,
    # so we mock or test standard properties)
    assert "text" in results[0]
    assert "metadata" in results[0]
    assert "distance" in results[0]


def test_generate_answer_mocked(mock_openai_client):
    pipeline = RAGPipeline()
    # Explicitly assign mocked client
    pipeline.openai_client = mock_openai_client

    # Mock completions endpoint
    mock_choice = MagicMock()
    mock_choice.message.content = "OpenAI builds GPT-4."
    mock_openai_client.chat.completions.create.return_value.choices = [mock_choice]

    retrieved_chunks = [
        {
            "text": "OpenAI builds state of the art models.",
            "metadata": {"source": "openai.pdf", "page": 2},
        }
    ]

    answer = pipeline.generate_answer("What does OpenAI build?", retrieved_chunks)
    assert answer == "OpenAI builds GPT-4."
    mock_openai_client.chat.completions.create.assert_called_once()


def test_conversation_history_retention():
    pipeline = RAGPipeline()
    assert pipeline.get_history() == []

    # First exchange
    chunks = [{"text": "Chunk 1", "metadata": {"source": "doc.pdf", "page": 1}}]
    ans1 = pipeline.generate_answer("Q1", chunks)
    assert len(pipeline.get_history()) == 2
    assert pipeline.get_history()[0] == {"role": "user", "content": "Q1"}
    assert pipeline.get_history()[1] == {"role": "assistant", "content": ans1}

    # Generate more exchanges to exceed the limit of 3
    ans2 = pipeline.generate_answer("Q2", chunks)
    ans3 = pipeline.generate_answer("Q3", chunks)
    ans4 = pipeline.generate_answer("Q4", chunks)

    # Should retain the last 3 exchanges (Q2, Q3, Q4)
    history = pipeline.get_history()
    assert len(history) == 6
    assert history[0] == {"role": "user", "content": "Q2"}
    assert history[1] == {"role": "assistant", "content": ans2}
    assert history[2] == {"role": "user", "content": "Q3"}
    assert history[3] == {"role": "assistant", "content": ans3}
    assert history[4] == {"role": "user", "content": "Q4"}
    assert history[5] == {"role": "assistant", "content": ans4}

    # Clear history
    pipeline.clear_history()
    assert pipeline.get_history() == []

