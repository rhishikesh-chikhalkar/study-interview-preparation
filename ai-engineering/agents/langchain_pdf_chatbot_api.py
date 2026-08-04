import uuid
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template_string, request
from langchain_classic.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llm_factory import get_configured_llm

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Global registry of active sessions
# session_id -> {
#     "chain": RunnableWithMessageHistory,
#     "history": InMemoryChatMessageHistory,
#     "pdf_path": str
# }
sessions: Dict[str, Dict[str, Any]] = {}


@app.route("/health", methods=["GET"])
def health() -> Any:
    return jsonify({"status": "healthy", "message": "PDF Chatbot API is running"})


@app.route("/initialize", methods=["POST"])
def initialize() -> Any:
    data = request.get_json() or {}
    pdf_path_str = data.get("pdf_path", "").strip()

    if not pdf_path_str:
        return jsonify({"error": "pdf_path is required"}), 400

    pdf_path = Path(pdf_path_str)
    if not pdf_path.exists():
        return jsonify({"error": f"File does not exist at '{pdf_path_str}'"}), 400

    if pdf_path.suffix.lower() != ".pdf":
        return jsonify({"error": f"'{pdf_path_str}' is not a PDF file"}), 400

    try:
        # Load PDF document
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()

        # Split document into text chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(pages)

        # Generate embeddings and build vector store index (FAISS)
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = FAISS.from_documents(chunks, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

        # Initialize the LLM using the centralized factory
        llm = get_configured_llm()

        # 1. Create a retriever prompt to contextualize questions
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )

        # 2. Create the QA prompt and combine chain
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know.\n\n"
            "{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        rag_chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )

        # 3. Create session history and wrap in RunnableWithMessageHistory
        chat_history = InMemoryChatMessageHistory()

        def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
            return chat_history

        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        # Generate a unique session ID
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "chain": conversational_rag_chain,
            "history": chat_history,
            "pdf_path": pdf_path_str,
        }

        return jsonify(
            {
                "status": "success",
                "message": "Successfully indexed PDF and initialized chatbot session",
                "session_id": session_id,
                "pdf_pages": len(pages),
                "chunks_created": len(chunks),
            }
        )

    except Exception as e:
        return jsonify({"error": f"Failed to initialize chatbot: {str(e)}"}), 500


@app.route("/chat", methods=["POST"])
def chat() -> Any:
    data = request.get_json() or {}
    session_id = data.get("session_id", "").strip()
    message = data.get("message", "").strip()

    if not session_id:
        return jsonify({"error": "session_id is required"}), 400
    if not message:
        return jsonify({"error": "message is required"}), 400

    if session_id not in sessions:
        return jsonify(
            {"error": f"Session '{session_id}' not found. Please initialize first."}
        ), 404

    try:
        session_data = sessions[session_id]
        chain = session_data["chain"]

        config = {"configurable": {"session_id": session_id}}
        response = chain.invoke({"input": message}, config=config)

        return jsonify({"answer": response.get("answer", ""), "session_id": session_id})

    except Exception as e:
        return jsonify({"error": f"Failed to generate response: {str(e)}"}), 500


@app.route("/swagger.json", methods=["GET"])
def swagger_json() -> Any:
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "PDF Chatbot API",
            "version": "1.0.0",
            "description": "API for PDF Chatbot utilizing LangChain, FAISS, and Ollama",
        },
        "paths": {
            "/health": {
                "get": {
                    "summary": "Check API health",
                    "responses": {
                        "200": {
                            "description": "API is healthy",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string"},
                                            "message": {"type": "string"},
                                        },
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/initialize": {
                "post": {
                    "summary": "Initialize PDF vector store",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["pdf_path"],
                                    "properties": {
                                        "pdf_path": {
                                            "type": "string",
                                            "example": "./roadmaps/18-month-full-stack-roadmap.pdf",
                                        }
                                    },
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "PDF indexed successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string"},
                                            "message": {"type": "string"},
                                            "session_id": {"type": "string"},
                                            "pdf_pages": {"type": "integer"},
                                            "chunks_created": {"type": "integer"},
                                        },
                                    }
                                }
                            },
                        },
                        "400": {"description": "Invalid input or file not found"},
                        "500": {"description": "Internal server error"},
                    },
                }
            },
            "/chat": {
                "post": {
                    "summary": "Chat with the PDF chatbot",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["session_id", "message"],
                                    "properties": {
                                        "session_id": {
                                            "type": "string",
                                            "example": "41fb439d-d6d6-47f2-9259-05d6df930ef6",
                                        },
                                        "message": {
                                            "type": "string",
                                            "example": "What is this roadmap about?",
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Successful chat response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "answer": {"type": "string"},
                                            "session_id": {"type": "string"},
                                        },
                                    }
                                }
                            },
                        },
                        "400": {"description": "Missing session_id or message"},
                        "404": {"description": "Session not found"},
                        "500": {"description": "Internal server error"},
                    },
                }
            },
        },
    }
    return jsonify(spec)


@app.route("/docs", methods=["GET"])
def swagger_ui() -> str:
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8" />
        <title>PDF Chatbot API Docs</title>
        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            window.onload = () => {
                window.ui = SwaggerUIBundle({
                    url: '/swagger.json',
                    dom_id: '#swagger-ui',
                });
            };
        </script>
    </body>
    </html>
    """
    return render_template_string(template)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
