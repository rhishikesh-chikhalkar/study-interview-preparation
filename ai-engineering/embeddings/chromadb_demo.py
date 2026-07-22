import chromadb


def main():
    print("=== ChromaDB Local Vector Database Demo ===")

    # 1. Initialize an in-memory ChromaDB client
    # EphemeralClient stores data in-memory and is perfect for quick demos.
    print("\nInitializing in-memory ChromaDB client...")
    client = chromadb.EphemeralClient()

    # 2. Create a collection
    # A collection is similar to a table in a relational database or a collection in MongoDB.
    # By default, ChromaDB uses the "all-MiniLM-L6-v2" Sentence Transformers model to generate embeddings.
    print("Creating collection 'sentences_demo'...")
    collection = client.create_collection(name="sentences_demo")

    # 3. Define 5 sentences to store
    sentences = [
        "The quick brown fox jumps over the lazy dog.",
        "Artificial intelligence is changing the software industry.",
        "Deep learning models require high-performance GPUs.",
        "I love eating delicious Italian pasta and pizza.",
        "A warm cup of coffee in the morning is highly relaxing.",
    ]
    ids = [f"id_{i}" for i in range(len(sentences))]

    # 4. Add the sentences to the collection
    # ChromaDB will automatically compute embeddings for these sentences using the default model.
    print(f"Storing {len(sentences)} sentences in the vector database...")
    collection.add(
        documents=sentences,
        ids=ids,
    )
    print("Sentences stored successfully!")

    # 5. Query the database for the most similar sentence
    # We will test two queries to demonstrate semantic search.
    queries = [
        "spaghetti and garlic bread",
        "neural networks and computer hardware",
    ]

    print("\n=== Performing Semantic Queries ===")
    for query in queries:
        print(f"\nQuery: '{query}'")
        print("Retrieving the most similar sentence...")

        results = collection.query(
            query_texts=[query],
            n_results=1,
        )

        # Retrieve result details
        retrieved_doc = results["documents"][0][0]
        retrieved_id = results["ids"][0][0]
        # Distance represents similarity (lower distance = higher similarity)
        distance = results["distances"][0][0]

        print(f"-> Most Similar Sentence: '{retrieved_doc}' (ID: {retrieved_id})")
        print(f"-> Distance (lower is closer/more similar): {distance:.4f}")


if __name__ == "__main__":
    main()
