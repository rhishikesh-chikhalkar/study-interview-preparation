from unittest.mock import patch


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "openai_api_configured" in data
    assert "collection_name" in data


def test_ask_endpoint_missing_payload(client):
    response = client.post("/ask", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_ask_endpoint_success(app, client):
    with (
        patch.object(app.rag_pipeline, "query_vector_store") as mock_query,
        patch.object(app.rag_pipeline, "generate_answer") as mock_generate,
    ):
        mock_query.return_value = [
            {
                "text": "Flask is a micro web framework.",
                "metadata": {"source": "doc.pdf", "page": 1},
                "distance": 0.1,
                "id": "doc_1",
            }
        ]
        mock_generate.return_value = "Flask is a micro web framework."

        response = client.post("/ask", json={"question": "What is Flask?"})
        assert response.status_code == 200
        data = response.get_json()
        assert data["question"] == "What is Flask?"
        assert data["answer"] == "Flask is a micro web framework."
        assert len(data["retrieved_chunks"]) == 1


def test_clear_history_endpoint(client):
    response = client.post("/clear_history")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
