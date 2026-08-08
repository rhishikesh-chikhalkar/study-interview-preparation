from typing import Any, Tuple
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from flask_rag_api.utils.logging import get_logger

logger = get_logger(__name__)


def make_error_response(message: str, status_code: int = 400) -> Tuple[Any, int]:
    """Generates a standardized JSON error response."""
    return jsonify({"error": message, "status_code": status_code}), status_code


def register_error_handlers(app: Flask) -> None:
    """Registers global error handlers on the Flask app."""

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException) -> Tuple[Any, int]:
        logger.warning("HTTP Exception: %s", e.description)
        return make_error_response(e.description or "HTTP Error", e.code or 400)

    @app.errorhandler(Exception)
    def handle_unexpected_exception(e: Exception) -> Tuple[Any, int]:
        logger.error("Unhandled Exception: %s", str(e), exc_info=True)
        return make_error_response("An internal server error occurred", 500)
