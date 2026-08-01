# RAG Chatbot Project

A full-stack Retrieval-Augmented Generation (RAG) assistant that allows users to index PDF documents and ask questions based strictly on the retrieved context.

## Project Overview

This project implements a RAG workflow from scratch:
1. **Document Loading**: Extracts text from PDF files page-by-page.
2. **Text Chunking**: Splits extracted text into semantic, overlapping chunks using recursive character splitting.
3. **Vector Embeddings**: Generates high-quality vector representations of text chunks using OpenAI (`text-embedding-3-small`) or local Ollama (`nomic-embed-text`).
4. **Vector Storage**: Stores and queries document vectors locally inside ChromaDB.
5. **Contextual Generation**: Automatically retrieves top-K relevant chunks, structures them into a prompt template, and generates responses using OpenAI (`gpt-4o-mini`) or local Ollama (`qwen3:1.7b`).

---

## Tech Stack

### Frontend (React Study Portal)
- **Vite & React**: Single Page Application container.
- **React Router v6**: Manages project-level routing.
- **CSS3 / Glassmorphism**: High-fidelity modern chat UI with loading spinners, dynamic submit button indicators, and dismissible error banners.

### Backend (Python RAG API)
- **Flask**: Exposes REST endpoints to query and index files.
- **ChromaDB**: Lightweight, embedded vector database.
- **LangChain Splitters**: Custom chunking pipelines.
- **OpenAI API & Ollama (httpx)**: Language model and embedding generation interfaces.
- **Astral uv**: Python virtual environment and execution manager.

---

## Getting Started

### 1. Prerequisites
- **Python 3.10+** (managed via `uv`)
- **Node.js** & **npm**

### 2. Configuration (`.env`)
Create a `.env` file in the root folder or under `ai-engineering/` to configure API keys:
```env
# Optional: To use the OpenAI full flow (defaults to Ollama/Mock if not provided)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: To customize local Ollama endpoint
OLLAMA_BASE_URL=http://localhost:11434
```

### 3. Run the Backend API
The backend automatically detects the configured AI provider. If `OPENAI_API_KEY` is present, it uses OpenAI vectors (`pdf_rag_collection_openai`). Otherwise, it defaults to Ollama (`pdf_rag_collection_ollama`).

```bash
# Install dependencies & run Flask server (on port 5001)
uv run ai-engineering/rag/rag_api.py
```

### 4. Run the React Frontend
```bash
# Navigate to the frontend directory
cd react/react-fundamentals

# Install dependencies and start Vite dev server (on port 5173)
npm install
npm run dev
```

---

## Usage Guide

### Indexing a PDF Document
To add a document to your knowledge base, send a `POST` request to the Flask server or run the interactive CLI:

#### Via REST API:
```bash
curl -X POST http://localhost:5001/index \
  -H "Content-Type: application/json" \
  -d '{"pdf_path": "path/to/your/document.pdf"}'
```

#### Via Command Line:
```bash
# Index a PDF and query it directly
uv run ai-engineering/rag/rag_pipeline.py --pdf "path/to/doc.pdf" --query "What is the summary?"
```

### Conversing with the Assistant
Access the UI at `http://localhost:5173/projects/ai-assistant` to submit queries. The UI will show a spinning indicator while processing, list retrieved context chunks alongside responses, and display dismissible alert banners if backend services are offline.

---

## Running Tests
Run automated pytest assertions for both the pipeline integration and API endpoints:
```bash
uv run pytest python/tests/test_rag_pipeline.py python/tests/test_rag_api.py
```
