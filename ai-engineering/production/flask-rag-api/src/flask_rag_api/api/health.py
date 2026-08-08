from typing import Any, Tuple
from flask import Blueprint, current_app, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/", methods=["GET"])
@health_bp.route("/health", methods=["GET"])
def health() -> Tuple[Any, int]:
    """Check the health status of the API service."""
    pipeline = getattr(current_app, "rag_pipeline", None)
    openai_configured = bool(pipeline and pipeline.openai_client) if pipeline else False
    collection_name = getattr(current_app, "chroma_collection_name", "unknown")
    database_dir = current_app.config.get("CHROMA_DB_DIR", "./_tmp/chroma_db")

    return jsonify(
        {
            "status": "healthy",
            "openai_api_configured": openai_configured,
            "collection_name": collection_name,
            "database_dir": database_dir,
        }
    ), 200
