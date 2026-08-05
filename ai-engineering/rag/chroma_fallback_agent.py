from typing import Any, Dict, List, Optional, TypedDict

import chromadb
from pydantic import BaseModel, Field


class Document(BaseModel):
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    score: Optional[float] = None


class AgentState(TypedDict):
    query: str
    documents: List[Document]
    fallback_needed: bool
    source_used: str
    final_answer: str


def validate_retrieval(results: dict, max_distance: float = 0.40) -> tuple[bool, list]:
    if not results or not results.get("documents") or not results["documents"][0]:
        return False, []

    valid_docs = []
    distances = results.get("distances", [[]])[0]
    documents = results["documents"][0]

    for doc, dist in zip(documents, distances):
        if dist <= max_distance:
            valid_docs.append(doc)

    has_valid_context = len(valid_docs) > 0
    return has_valid_context, valid_docs


class ChromaFallbackRAG:
    """Agentic RAG pipeline querying ChromaDB with web search fallback."""

    def __init__(
        self,
        collection_name: str = "kb_fallback",
        distance_threshold: float = 0.45,
        chroma_client: Optional[chromadb.ClientAPI] = None,
    ) -> None:
        self.client = chroma_client or chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        self.distance_threshold = distance_threshold

    def retrieve_internal(self, query: str, top_k: int = 3) -> List[Document]:
        """Query internal ChromaDB collection and apply distance threshold."""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
        )

        docs: List[Document] = []
        if not results["documents"] or not results["documents"][0]:
            return docs

        distances = results["distances"][0] if results["distances"] else []
        contents = results["documents"][0]
        metadatas = (
            results["metadatas"][0] if results["metadatas"] else [{}] * len(contents)
        )

        for content, dist, meta in zip(contents, distances, metadatas):
            if dist <= self.distance_threshold:
                meta_dict = meta if meta is not None else {}
                docs.append(Document(content=content, metadata=meta_dict, score=dist))

        return docs

    def execute_web_search(self, query: str) -> List[Document]:
        """Execute web search fallback when internal retrieval is insufficient."""
        web_content = f"Web search results for query: {query}"
        return [
            Document(
                content=web_content,
                metadata={"source": "web_search", "url": "https://search.api/results"},
            )
        ]

    def grade_relevance(self, query: str, docs: List[Document]) -> bool:
        """Evaluate context relevance to the query."""
        if not docs:
            return False
        return any(word in docs[0].content.lower() for word in query.lower().split())

    def run(self, query: str) -> AgentState:
        """Run the complete agentic RAG workflow with fallback."""
        state: AgentState = {
            "query": query,
            "documents": [],
            "fallback_needed": False,
            "source_used": "none",
            "final_answer": "",
        }

        internal_docs = self.retrieve_internal(query)

        if internal_docs and self.grade_relevance(query, internal_docs):
            state["documents"] = internal_docs
            state["source_used"] = "chromadb"
        else:
            state["fallback_needed"] = True

        if state["fallback_needed"]:
            web_docs = self.execute_web_search(query)
            state["documents"] = web_docs
            state["source_used"] = "web_search"

        context = "\n".join([d.content for d in state["documents"]])
        state["final_answer"] = (
            f"Answer based on [{state['source_used']}]: "
            f"Context summary -> {context[:100]}"
        )

        return state
