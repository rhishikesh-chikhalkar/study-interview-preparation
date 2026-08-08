"""Flask proxy routes for communicating with downstream Go microservice.

Establishes inter-service HTTP pipeline: React SPA -> Flask Backend -> Go Microservice.
"""

import os
from typing import Any

import httpx
from flask import Blueprint, jsonify, request

from flask_rag_api.utils.errors import make_error_response
from flask_rag_api.utils.logging import get_logger

logger = get_logger(__name__)

go_proxy_bp = Blueprint("go_proxy", __name__)

DEFAULT_GO_URL = "https://render-go-service-txtm.onrender.com"


def get_go_service_url() -> str:
    """Retrieve configured Go microservice base URL."""
    url = os.getenv("GO_SERVICE_URL", DEFAULT_GO_URL).strip()
    return url.rstrip("/")


def get_headers() -> dict[str, str]:
    """Build authorization and content headers for Go microservice calls."""
    headers = {"Content-Type": "application/json"}
    api_key = os.getenv("GO_API_KEY", "").strip()
    if api_key:
        headers["X-API-Key"] = api_key
    return headers


@go_proxy_bp.route("/go-health", methods=["GET"])
def go_health() -> tuple[Any, int]:
    """Check health status of downstream Go microservice."""
    base_url = get_go_service_url()
    target_url = f"{base_url}/healthz"
    try:
        with httpx.Client(timeout=3.0) as client:
            resp = client.get(target_url, headers=get_headers())

        if resp.status_code == 200:
            return (
                jsonify(
                    {
                        "status": "healthy",
                        "go_service_url": base_url,
                        "go_response": resp.json(),
                    }
                ),
                200,
            )
        return make_error_response(
            f"Go microservice returned status {resp.status_code}",
            resp.status_code,
        )
    except Exception as err:  # noqa: BLE001
        logger.warning("Failed to reach Go microservice: %s", err)
        return (
            jsonify(
                {
                    "status": "degraded",
                    "go_service_url": base_url,
                    "error": f"Connection error: {err!s}",
                }
            ),
            503,
        )


@go_proxy_bp.route("/go-analyze", methods=["POST"])
def go_analyze() -> tuple[Any, int]:
    """Forward text analysis payload to downstream Go microservice."""
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")

    base_url = get_go_service_url()
    target_url = f"{base_url}/api/v1/analyze"
    try:
        with httpx.Client(timeout=5.0) as client:
            resp = client.post(target_url, json={"text": text}, headers=get_headers())

        if resp.status_code == 200:
            result = resp.json()
            result["gateway"] = "Flask RAG Backend API"
            return jsonify(result), 200

        return make_error_response(
            f"Go microservice error ({resp.status_code}): {resp.text}",
            resp.status_code,
        )
    except Exception as err:
        logger.exception("Go microservice proxy failed for /go-analyze")
        return make_error_response(
            f"Failed to connect to Go microservice: {err!s}", 502
        )


@go_proxy_bp.route("/go-tasks", methods=["GET", "POST"])
def go_tasks() -> tuple[Any, int]:
    """Proxy task management requests to downstream Go microservice."""
    base_url = get_go_service_url()
    target_url = f"{base_url}/api/v1/tasks"
    try:
        with httpx.Client(timeout=5.0) as client:
            if request.method == "GET":
                resp = client.get(target_url, headers=get_headers())
            else:
                payload = request.get_json(silent=True) or {}
                resp = client.post(target_url, json=payload, headers=get_headers())

        if resp.status_code in (200, 201):
            return jsonify(resp.json()), resp.status_code

        return make_error_response(
            f"Go task endpoint returned error ({resp.status_code})",
            resp.status_code,
        )
    except Exception as err:
        logger.exception("Go microservice proxy failed for /go-tasks")
        return make_error_response(
            f"Failed to communicate with Go tasks service: {err!s}", 502
        )
