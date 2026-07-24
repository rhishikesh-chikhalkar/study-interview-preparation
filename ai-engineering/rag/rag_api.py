import os
import sys
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request

# Ensure we can import from the current directory
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rag_pipeline import RAGPipeline

app = Flask(__name__)

# Configure persistent database directory and collection
DB_DIR = os.getenv("CHROMA_DB_DIR", "./_tmp/chroma_db")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "pdf_rag_collection")

# Instantiate pipeline and collection
pipeline = RAGPipeline(persist_directory=DB_DIR)
collection = pipeline.create_or_get_collection(COLLECTION_NAME)


@app.route("/health", methods=["GET"])
def health() -> Any:
    """Check the health status of the API."""
    openai_configured = pipeline.openai_client is not None
    return jsonify(
        {
            "status": "healthy",
            "openai_api_configured": openai_configured,
            "collection_name": COLLECTION_NAME,
            "database_dir": DB_DIR,
        }
    )


@app.route("/index", methods=["POST"])
def index() -> Any:
    """Index a PDF document into the vector database.

    Expects a JSON payload:
    {
        "pdf_path": "path/to/document.pdf"
    }
    """
    data = request.get_json() or {}
    pdf_path_str = data.get("pdf_path", "").strip()

    if not pdf_path_str:
        return jsonify({"error": "pdf_path is required"}), 400

    pdf_path = Path(pdf_path_str)
    if not pdf_path.exists():
        return jsonify({"error": f"File not found at: {pdf_path_str}"}), 400

    try:
        pages = pipeline.load_pdf(str(pdf_path))
        chunks = pipeline.chunk_documents(pages)
        pipeline.populate_vector_store(chunks, collection)
        return jsonify(
            {
                "status": "success",
                "message": f"Successfully indexed PDF: {pdf_path.name}",
                "chunks_created": len(chunks),
            }
        )
    except Exception as e:
        return jsonify({"error": f"Failed to index PDF: {str(e)}"}), 500


@app.route("/ask", methods=["POST"])
def ask() -> Any:
    """Query the RAG pipeline.

    Expects a JSON payload:
    {
        "question": "your question here"
    }
    """
    data = request.get_json() or {}
    question = data.get("question", "").strip() or data.get("query", "").strip()

    if not question:
        return jsonify({"error": "question or query is required"}), 400

    try:
        # Retrieve context chunks from vector store
        retrieved_chunks = pipeline.query_vector_store(question, collection, k=3)

        # Generate answer using OpenAI model or mock
        answer = pipeline.generate_answer(question, retrieved_chunks)

        return jsonify(
            {
                "question": question,
                "answer": answer,
                "retrieved_chunks": retrieved_chunks,
                "conversation_history": pipeline.get_history(),
            }
        )
    except Exception as e:
        return jsonify({"error": f"Failed to generate answer: {str(e)}"}), 500


@app.route("/clear_history", methods=["POST"])
def clear_history() -> Any:
    """Clear the pipeline's conversation history."""
    pipeline.clear_history()
    return jsonify({"status": "success", "message": "Conversation history cleared"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
