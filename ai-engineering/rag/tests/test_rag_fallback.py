import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from chroma_fallback_agent import (
    ChromaFallbackRAG,
    validate_retrieval,
)


@pytest.fixture
def rag_agent() -> ChromaFallbackRAG:
    agent = ChromaFallbackRAG(
        collection_name="kb_test_fallback_fixture",
        distance_threshold=0.45,
    )
    agent.collection.add(
        documents=[
            "Python decorators extend function behavior.",
            "FastAPI uses Pydantic for data validation.",
        ],
        ids=["doc1", "doc2"],
    )
    return agent


def test_internal_chromadb_hit(rag_agent: ChromaFallbackRAG) -> None:
    state = rag_agent.run("decorators")
    assert state["fallback_needed"] is False
    assert state["source_used"] == "chromadb"
    assert len(state["documents"]) > 0
    assert "decorators" in state["final_answer"].lower()


def test_web_search_fallback_trigger(rag_agent: ChromaFallbackRAG) -> None:
    state = rag_agent.run("quantum computing algorithms")
    assert state["fallback_needed"] is True
    assert state["source_used"] == "web_search"
    assert len(state["documents"]) == 1
    assert state["documents"][0].metadata["source"] == "web_search"


def test_validate_retrieval_empty_and_threshold() -> None:
    has_valid, docs = validate_retrieval({})
    assert has_valid is False
    assert docs == []

    mock_results = {
        "documents": [["doc_a", "doc_b"]],
        "distances": [[0.30, 0.80]],
    }
    has_valid, docs = validate_retrieval(mock_results, max_distance=0.40)
    assert has_valid is True
    assert docs == ["doc_a"]
