import sys
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv
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
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load environment variables (contains OPENAI_API_KEY)
load_dotenv()


def main() -> None:

    print("==================================================")
    print("      PDF Chatbot with LangChain & FAISS          ")
    print("==================================================")

    # Prompt user for PDF file path
    while True:
        pdf_path_str = input("Enter the path to your PDF file: ").strip()
        if not pdf_path_str:
            print("Path cannot be empty. Please try again.")
            continue

        pdf_path = Path(pdf_path_str)
        if not pdf_path.exists():
            print(
                f"Error: File does not exist at '{pdf_path_str}'. Please enter a valid path."
            )
            continue

        if pdf_path.suffix.lower() != ".pdf":
            print(
                f"Error: '{pdf_path_str}' is not a PDF file. Please select a .pdf file."
            )
            continue

        break

    print(f"\nLoading PDF document: {pdf_path.name}...")
    try:
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        print(f"Successfully loaded {len(pages)} pages.")
    except Exception as e:
        print(f"Failed to load PDF: {e}")
        sys.exit(1)

    print("Splitting document into text chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(pages)
    print(f"Created {len(chunks)} chunks from the document.")

    print("Generating embeddings and building vector store index (FAISS)...")
    try:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = FAISS.from_documents(chunks, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        print("Vector store built successfully!")
    except Exception as e:
        print(f"Failed to build vector store: {e}")
        sys.exit(1)

    # Initialize the LLM using production variable naming
    print("Initializing ChatOllama model (qwen3:1.7b)...")
    llm = ChatOllama(model="qwen3:1.7b", temperature=0)

    # 1. Create a retriever prompt to contextualize questions (reformulate with history)
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
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    # 3. Memory store to keep chat history per session_id
    store: Dict[str, InMemoryChatMessageHistory] = {}

    def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]

    # Wrap the chain with RunnableWithMessageHistory
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    # Configure the session ID
    config = {"configurable": {"session_id": "pdf_chat_session"}}

    print("\n==================================================")
    print("Interactive PDF Chatbot Ready!")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("==================================================\n")

    while True:
        try:
            # Capture user input
            user_input = input("You: ")

            # Check for exit commands
            if user_input.strip().lower() in ["exit", "quit"]:
                print("Bot: Goodbye!")
                break

            # Skip empty inputs
            if not user_input.strip():
                continue

            # Invoke the conversational RAG chain
            response = conversational_rag_chain.invoke(
                {"input": user_input}, config=config
            )

            # Print response
            print(f"Bot: {response.get('answer', '')}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nBot: Goodbye!")
            break


if __name__ == "__main__":
    main()
