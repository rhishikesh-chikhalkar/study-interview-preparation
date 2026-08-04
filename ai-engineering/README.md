# 🤖 Phase 9: AI Engineering

This directory contains code implementations, experiments, and projects related to **Phase 9 — AI Engineering (Highest ROI)** of the interview preparation roadmap.

## 📁 Directory Structure

- [agents/](./agents/) — AI Agentic workflows, tool use, and multi-agent systems.
  - [basic_langchain_agent.py](./agents/basic_langchain_agent.py) — Tool-selection LangChain agent (Calculator, Word Counter, Weather, DB Lookup).
  - [langchain_demo.py](./agents/langchain_demo.py) — RAG & SQL database LangChain agent demonstration.
  - [langchain_ollama_demo.py](./agents/langchain_ollama_demo.py) — Local LLM integration using LangChain and Ollama.
  - [langchain_ollama_interactive.py](./agents/langchain_ollama_interactive.py) — Interactive local LLM CLI chatbot using LangChain and Ollama.
  - [langchain_pdf_chatbot.py](./agents/langchain_pdf_chatbot.py) — Conversational PDF chatbot using LangChain, FAISS, and Ollama.
- [rag/](./rag/) — Retrieval-Augmented Generation architectures (Chunking, vector DBs, retrieval optimization).
  - [rag_pipeline.py](./rag/rag_pipeline.py) — Core RAG pipeline utilizing ChromaDB and OpenAI.
  - [rag_api.py](./rag/rag_api.py) — Flask API wrapper offering `/health`, `/index`, and `/ask` endpoints.
- `prompts/` — Advanced prompt engineering techniques.
- `evaluation/` — LLM evaluation frameworks.

## 🚀 Running the Flask API Server

To start the RAG Flask API server:
```bash
uv run python ai-engineering/rag/rag_api.py
```

To test the server using `curl`:
```bash
# Check health
curl http://127.0.0.1:5001/health

# Query RAG Pipeline
curl -X POST http://127.0.0.1:5001/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'
```

## 🎯 High-ROI Topics Covered

1. **LLM Fundamentals & Inference Parameter Tuning** (temperature, top-p, nucleus sampling)
2. **Advanced Prompting** (Few-shot, CoT, ReAct, Structured JSON outputs)
3. **Production RAG** (Hybrid search, Re-ranking, Contextual Retrieval, chunking strategies)
4. **Agentic Workflows** (Planning, Tool Use / Function calling, Memory integration)
5. **LLM Evaluation & Guardrails** (RAGAS, toxicity detection, cost optimization)
