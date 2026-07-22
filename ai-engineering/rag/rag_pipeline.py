import argparse
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import pypdf
import chromadb
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI

# 1. Load environment variables. First check workspace root, then ai-engineering/.env.
workspace_root = Path(__file__).resolve().parent.parent.parent
env_paths = [
    workspace_root / "ai-engineering" / ".env",
    workspace_root / ".env",
]
for path in env_paths:
    if path.exists():
        load_dotenv(dotenv_path=path)

api_key = os.getenv("OPENAI_API_KEY")


class RAGPipeline:
    """A Retrieval-Augmented Generation (RAG) pipeline from scratch using ChromaDB and OpenAI."""

    def __init__(self, persist_directory: Optional[str] = None):
        # Initialize OpenAI client if key is available
        if api_key:
            self.openai_client = OpenAI(api_key=api_key)
        else:
            self.openai_client = None

        # Initialize ChromaDB client (persistent or ephemeral)
        if persist_directory:
            self.chroma_client = chromadb.PersistentClient(path=persist_directory)
        else:
            self.chroma_client = chromadb.EphemeralClient()

    def load_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Loads a PDF file and extracts text page-by-page.

        Returns a list of dictionaries with text and page metadata.
        """
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

        pages_data = []
        reader = pypdf.PdfReader(str(path))
        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            pages_data.append(
                {"text": text, "metadata": {"source": path.name, "page": idx + 1}}
            )
        return pages_data

    def chunk_documents(
        self,
        pages_data: List[Dict[str, Any]],
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> List[Dict[str, Any]]:
        """Splits page text into smaller chunks while preserving metadata."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        chunks = []
        for page in pages_data:
            text = page["text"]
            if not text.strip():
                continue
            split_texts = splitter.split_text(text)
            for chunk_idx, split_text in enumerate(split_texts):
                chunks.append(
                    {
                        "text": split_text,
                        "metadata": {
                            **page["metadata"],
                            "chunk_index": chunk_idx,
                        },
                    }
                )
        return chunks

    def get_embedding(self, text: str) -> List[float]:
        """Generates embedding vector for a given text using OpenAI text-embedding-3-small.

        Falls back to a deterministic pseudo-random vector if API key is not configured or fails.
        """
        if self.openai_client:
            try:
                response = self.openai_client.embeddings.create(
                    model="text-embedding-3-small", input=text
                )
                return response.data[0].embedding
            except Exception as e:
                print(
                    f"[Warning] OpenAI embedding generation failed: {e}. Using mock embedding."
                )

        # Fallback/Mock Embedding for offline/testing mode (1536-dimensional vector)
        import random

        # Seed by hash of text to ensure deterministic output for identical text inputs
        random.seed(hash(text))
        return [random.uniform(-0.1, 0.1) for _ in range(1536)]

    def create_or_get_collection(self, collection_name: str) -> chromadb.Collection:
        """Creates or gets an existing ChromaDB collection."""
        return self.chroma_client.get_or_create_collection(name=collection_name)

    def populate_vector_store(
        self, chunks: List[Dict[str, Any]], collection: chromadb.Collection
    ) -> None:
        """Embeds text chunks and stores them in ChromaDB."""
        if not chunks:
            return

        texts = [chunk["text"] for chunk in chunks]
        embeddings: List[List[float]] = []
        batch_size = 100

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]
            if self.openai_client:
                try:
                    response = self.openai_client.embeddings.create(
                        model="text-embedding-3-small", input=batch_texts
                    )
                    embeddings.extend([data.embedding for data in response.data])
                except Exception as e:
                    print(f"[Warning] OpenAI batch embedding failed: {e}. Using mock embeddings.")
                    import random
                    for text in batch_texts:
                        random.seed(hash(text))
                        embeddings.extend([[random.uniform(-0.1, 0.1) for _ in range(1536)]])
            else:
                import random
                for text in batch_texts:
                    random.seed(hash(text))
                    embeddings.extend([[random.uniform(-0.1, 0.1) for _ in range(1536)]])

        documents = []
        ids = []
        metadatas = []

        for idx, chunk in enumerate(chunks):
            doc_id = f"{chunk['metadata']['source']}_p{chunk['metadata']['page']}_c{chunk['metadata']['chunk_index']}_{idx}"
            documents.append(chunk["text"])
            ids.append(doc_id)
            metadatas.append(chunk["metadata"])

        # Batch insert into ChromaDB
        collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )

    def query_vector_store(
        self, query: str, collection: chromadb.Collection, k: int = 3
    ) -> List[Dict[str, Any]]:
        """Retrieves top k relevant documents/chunks for a given query."""
        query_embedding = self.get_embedding(query)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
        )

        retrieved_chunks = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = (
                results["metadatas"][0] if results["metadatas"] else [{}] * len(docs)
            )
            distances = (
                results["distances"][0] if results["distances"] else [0.0] * len(docs)
            )
            ids = results["ids"][0]

            for doc, meta, dist, doc_id in zip(docs, metas, distances, ids):
                retrieved_chunks.append(
                    {
                        "text": doc,
                        "metadata": meta,
                        "distance": dist,
                        "id": doc_id,
                    }
                )
        return retrieved_chunks

    def generate_answer(
        self, query: str, retrieved_chunks: List[Dict[str, Any]]
    ) -> str:
        """Sends query and retrieved context chunks to OpenAI GPT model to generate answer."""
        context_text = "\n\n---\n\n".join(
            [
                f"[Source: {c['metadata'].get('source')} Page: {c['metadata'].get('page')}]\n{c['text']}"
                for c in retrieved_chunks
            ]
        )

        system_message = (
            "You are a helpful, expert AI assistant. Answer the user's question based strictly on the provided context below.\n"
            "If the answer cannot be found in the context, state that the context does not contain enough information to answer.\n\n"
            "### Context:\n"
            f"{context_text}"
        )

        if not self.openai_client:
            return (
                "[Mock Response - OpenAI API Key not configured]\n"
                f"I would answer your query: '{query}' using the context from {len(retrieved_chunks)} source chunk(s)."
            )

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": query},
                ],
                temperature=0.0,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            print(f"[Warning] OpenAI chat completion failed: {e}. Using mock model response.")
            chunks_summary = "\n".join([f"  * Page {c['metadata'].get('page')}: {c['text'].replace('\n', ' ')[:100]}..." for c in retrieved_chunks])
            return (
                f"[Mock Answer - OpenAI API Error: {e}]\n"
                f"Simulating response for query: '{query}' based on retrieved chunks:\n{chunks_summary}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="ChromaDB & OpenAI RAG Pipeline CLI")
    parser.add_argument("--pdf", type=str, help="Path to the PDF document to index")
    parser.add_argument(
        "--query", type=str, help="Single query to ask the RAG pipeline"
    )
    parser.add_argument(
        "--collection",
        type=str,
        default="pdf_rag_collection",
        help="ChromaDB collection name",
    )
    parser.add_argument(
        "--db-dir",
        type=str,
        default="./_tmp/chroma_db",
        help="Persistent ChromaDB directory",
    )
    args = parser.parse_args()

    # Instantiate pipeline
    pipeline = RAGPipeline(persist_directory=args.db_dir)
    collection = pipeline.create_or_get_collection(args.collection)

    # 1. If PDF is supplied, load, chunk, and index it
    if args.pdf:
        print(f"[*] Loading PDF: {args.pdf}")
        pages = pipeline.load_pdf(args.pdf)
        print(f"[*] Loaded {len(pages)} pages.")

        print("[*] Chunking pages...")
        chunks = pipeline.chunk_documents(pages)
        print(f"[*] Created {len(chunks)} chunks.")

        print("[*] Adding chunks to ChromaDB vector store...")
        pipeline.populate_vector_store(chunks, collection)
        print("[*] Vector database populated successfully!")

    # 2. Run query if provided
    if args.query:
        print(f"\n[*] Query: {args.query}")
        print("[*] Retrieving relevant chunks...")
        relevant_chunks = pipeline.query_vector_store(args.query, collection, k=3)
        print(f"[*] Found {len(relevant_chunks)} relevant chunk(s).")
        for idx, chunk in enumerate(relevant_chunks):
            print(
                f"   -> Chunk {idx + 1} (Dist: {chunk['distance']:.4f}) from Page {chunk['metadata'].get('page')}:"
            )
            snippet = chunk["text"].replace("\n", " ")[:100]
            print(f'      "{snippet}..."')

        print("\n[*] Generating response from OpenAI...")
        answer = pipeline.generate_answer(args.query, relevant_chunks)
        print(f"\nAnswer:\n{answer}\n")
    elif not args.pdf:
        # Default interactive shell if no args passed
        print("==================================================")
        print("          Interactive RAG Pipeline CLI           ")
        print("==================================================")
        pdf_path = input("Enter path to PDF file to index: ").strip()
        if not pdf_path:
            print("No PDF path entered. Exiting.")
            return

        try:
            pages = pipeline.load_pdf(pdf_path)
            chunks = pipeline.chunk_documents(pages)
            pipeline.populate_vector_store(chunks, collection)
            print(
                f"Successfully loaded, chunked ({len(chunks)} chunks), and indexed PDF!"
            )
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return

        while True:
            try:
                query = input("\nAsk a question (or type 'exit' to quit): ").strip()
                if not query or query.lower() in ["exit", "quit"]:
                    break
                relevant_chunks = pipeline.query_vector_store(query, collection, k=3)
                answer = pipeline.generate_answer(query, relevant_chunks)
                print(f"\nAnswer:\n{answer}\n")
            except (KeyboardInterrupt, EOFError):
                break


if __name__ == "__main__":
    main()
