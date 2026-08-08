"""Integration tests for Flask proxy routes calling downstream Go microservice.

Verifies end-to-end telemetry and proxy forwarding in Flask backend.
"""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def client():
    """Construct test client for Flask application."""
    from flask_rag_api import create_app
    from flask_rag_api.config import TestingConfig

    app = create_app(TestingConfig)
    with app.test_client() as test_client:
        yield test_client


def test_go_health_success(client):
    """Verify /go-health proxy route when Go service responds 200."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"status": "ok", "service": "go-microservice"}

    with patch("httpx.Client.get", return_value=mock_resp):
        response = client.get("/go-health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"
        assert data["go_response"]["service"] == "go-microservice"


def test_go_health_connection_error(client):
    """Verify /go-health proxy route fallback when Go service is unreachable."""
    with patch("httpx.Client.get", side_effect=Exception("Connection refused")):
        response = client.get("/go-health")
        assert response.status_code == 503
        data = response.get_json()
        assert data["status"] == "degraded"
        assert "Connection refused" in data["error"]


def test_go_analyze_success(client):
    """Verify /go-analyze proxy route forwards text and returns enriched result."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "status": "success",
        "word_count": 5,
        "character_count": 25,
        "service": "Go High-Performance Microservice",
    }

    with patch("httpx.Client.post", return_value=mock_resp):
        response = client.post(
            "/go-analyze", json={"text": "Hello world from React SPA"}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "success"
        assert data["word_count"] == 5
        assert data["gateway"] == "Flask RAG Backend API"


def test_go_tasks_get_success(client):
    """Verify /go-tasks proxy route retrieves tasks list from Go microservice."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = [
        {"id": "task-1", "title": "Analyze telemetry", "status": "completed"}
    ]

    with patch("httpx.Client.get", return_value=mock_resp):
        response = client.get("/go-tasks")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]["id"] == "task-1"
