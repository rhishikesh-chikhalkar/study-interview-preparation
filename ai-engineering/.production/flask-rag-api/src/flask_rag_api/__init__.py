from typing import Any

from flask import Flask, request

from flask_rag_api.api import health_bp, rag_bp
from flask_rag_api.config import Config, get_config
from flask_rag_api.core.pipeline import RAGPipeline
from flask_rag_api.utils.errors import register_error_handlers
from flask_rag_api.utils.logging import get_logger, setup_logging

logger = get_logger(__name__)


def create_app(config_class: type[Config] | None = None) -> Flask:
    """Application Factory for Flask RAG API microservice."""
    setup_logging()

    app = Flask(__name__)

    # Load configuration
    cfg = config_class() if config_class else get_config()
    app.config.from_object(cfg)

    logger.info("Initializing Flask RAG API App...")

    # Attach RAG Pipeline instance to App Context
    pipeline = RAGPipeline(
        api_key=app.config.get("OPENAI_API_KEY"),
        persist_directory=app.config.get("CHROMA_DB_DIR"),
    )
    collection_name = app.config.get(
        "CHROMA_COLLECTION",
        "pdf_rag_collection_openai"
        if pipeline.openai_client
        else "pdf_rag_collection_ollama",
    )
    collection = pipeline.create_or_get_collection(collection_name)

    app.rag_pipeline = pipeline  # type: ignore[attr-defined]
    app.chroma_collection = collection  # type: ignore[attr-defined]
    app.chroma_collection_name = collection_name  # type: ignore[attr-defined]

    # CORS Handlers
    @app.before_request
    def handle_options() -> Any | None:
        if request.method == "OPTIONS":
            response = app.make_default_options_response()
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Headers"] = (
                "Content-Type,Authorization"
            )
            response.headers["Access-Control-Allow-Methods"] = (
                "GET,PUT,POST,DELETE,OPTIONS"
            )
            response.headers["Access-Control-Max-Age"] = "86400"
            return response
        return None

    @app.after_request
    def add_cors_headers(response: Any) -> Any:
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,PUT,POST,DELETE,OPTIONS"
        return response

    # Register Blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(rag_bp)

    # Register Error Handlers
    register_error_handlers(app)

    logger.info("Flask RAG API App initialized successfully.")
    return app
