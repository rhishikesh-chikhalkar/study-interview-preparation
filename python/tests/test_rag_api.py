import sys
from pathlib import Path
from unittest.mock import patch
import pytest

# Ensure our imports work correctly by adding the target directory directly
sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent.parent / "ai-engineering" / "rag")
)

from rag_api import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "openai_api_configured" in data


def test_ask_endpoint_missing_payload(client):
    response = client.post("/ask", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


@patch("rag_api.pipeline")
def test_ask_endpoint_success(mock_pipeline, client):
    # Mock return values for vector store querying and answer generation
    mock_pipeline.query_vector_store.return_value = [
        {
            "text": "Flask is a micro web framework written in Python.",
            "metadata": {"source": "flask_doc.pdf", "page": 1},
            "distance": 0.1,
            "id": "doc_1",
        }
    ]
    mock_pipeline.generate_answer.return_value = (
        "Flask is a micro web framework written in Python."
    )
    mock_pipeline.get_history.return_value = []

    response = client.post("/ask", json={"question": "What is Flask?"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["question"] == "What is Flask?"
    assert data["answer"] == "Flask is a micro web framework written in Python."
    assert len(data["retrieved_chunks"]) == 1
    assert (
        data["retrieved_chunks"][0]["text"]
        == "Flask is a micro web framework written in Python."
    )


def test_clear_history_endpoint(client):
    response = client.post("/clear_history")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "cleared" in data["message"]


@patch("rag_api.pipeline")
def test_ask_endpoint_with_history(mock_pipeline, client):
    # Setup mock pipeline history
    mock_pipeline.query_vector_store.return_value = []
    mock_pipeline.generate_answer.return_value = "Mock Answer"
    mock_pipeline.get_history.return_value = [
        {"role": "user", "content": "Prev Q"},
        {"role": "assistant", "content": "Prev Ans"},
    ]

    response = client.post("/ask", json={"question": "New Q"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["question"] == "New Q"
    assert data["answer"] == "Mock Answer"
    assert "conversation_history" in data
    assert len(data["conversation_history"]) == 2
    assert data["conversation_history"][0] == {"role": "user", "content": "Prev Q"}
    assert data["conversation_history"][1] == {
        "role": "assistant",
        "content": "Prev Ans",
    }
