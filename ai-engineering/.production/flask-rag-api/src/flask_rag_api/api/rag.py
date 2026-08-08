from pathlib import Path
from typing import Any

from flask import Blueprint, current_app, jsonify, request
from werkzeug.utils import secure_filename

from flask_rag_api.utils.errors import make_error_response
from flask_rag_api.utils.logging import get_logger

logger = get_logger(__name__)

rag_bp = Blueprint("rag", __name__)


@rag_bp.route("/index", methods=["POST"])
def index() -> tuple[Any, int]:
    """Index a PDF document into the vector database (supports file upload or JSON path)."""
    uploaded_file = request.files.get("file") or request.files.get("pdf")
    temp_file_created = False
    pdf_path_str = ""

    if uploaded_file and uploaded_file.filename:
        filename = secure_filename(uploaded_file.filename) or "uploaded.pdf"
        temp_dir = Path("./_tmp/uploads")
        temp_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = temp_dir / filename
        uploaded_file.save(pdf_path)
        pdf_path_str = str(pdf_path)
        temp_file_created = True
    else:
        data = request.get_json(silent=True) or {}
        pdf_path_str = data.get("pdf_path", "").strip()

        if not pdf_path_str:
            return make_error_response(
                "Either 'file' upload or 'pdf_path' JSON parameter is required", 400
            )

        pdf_path = Path(pdf_path_str)
        if not pdf_path.exists():
            # Check relative to application root / package root
            pkg_root = Path(current_app.root_path).parent.parent
            possible_paths = [
                pkg_root / pdf_path_str,
                pkg_root / "data" / pdf_path_str,
                pkg_root / "data" / Path(pdf_path_str).name,
            ]
            found_path = None
            for p in possible_paths:
                if p.exists():
                    found_path = p
                    break

            if found_path:
                pdf_path = found_path
            else:
                return make_error_response(f"File not found at: {pdf_path_str}", 400)

    pipeline = current_app.rag_pipeline
    collection = current_app.chroma_collection

    try:
        pages = pipeline.load_pdf(str(pdf_path))
        chunks = pipeline.chunk_documents(pages)
        pipeline.populate_vector_store(chunks, collection)
        logger.info("Indexed PDF '%s' with %d chunks.", pdf_path.name, len(chunks))
        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"Successfully indexed PDF: {pdf_path.name}",
                    "chunks_created": len(chunks),
                }
            ),
            200,
        )
    except Exception as e:
        logger.exception("Failed to index PDF '%s'", pdf_path_str)
        return make_error_response(f"Failed to index PDF: {e!s}", 500)
    finally:
        if temp_file_created and pdf_path.exists():
            try:
                pdf_path.unlink()
            except OSError as err:
                logger.warning("Failed to remove temp file '%s': %s", pdf_path, err)


@rag_bp.route("/ask", methods=["POST"])
def ask() -> tuple[Any, int]:
    """Query the RAG pipeline."""
    data = request.get_json() or {}
    question = data.get("question", "").strip() or data.get("query", "").strip()

    if not question:
        return make_error_response("question or query is required", 400)

    pipeline = current_app.rag_pipeline
    collection = current_app.chroma_collection

    try:
        retrieved_chunks = pipeline.query_vector_store(question, collection, k=3)
        answer = pipeline.generate_answer(question, retrieved_chunks)

        return jsonify(
            {
                "question": question,
                "answer": answer,
                "retrieved_chunks": retrieved_chunks,
                "conversation_history": pipeline.get_history(),
            }
        ), 200
    except Exception as e:
        logger.exception("Failed to generate answer for question")
        return make_error_response(f"Failed to generate answer: {e!s}", 500)


@rag_bp.route("/clear_history", methods=["POST"])
def clear_history() -> tuple[Any, int]:
    """Clear the pipeline's conversation history."""
    pipeline = current_app.rag_pipeline
    pipeline.clear_history()
    return jsonify(
        {"status": "success", "message": "Conversation history cleared"}
    ), 200
