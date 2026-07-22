import chromadb


def test_chromadb_basic_flow():
    # 1. Initialize client
    client = chromadb.EphemeralClient()

    # 2. Create collection
    collection = client.create_collection(name="test_collection")

    # 3. Add sentences
    documents = [
        "Python is a programming language.",
        "The sky is blue today.",
    ]
    ids = ["id_1", "id_2"]
    collection.add(documents=documents, ids=ids)

    # 4. Query
    results = collection.query(
        query_texts=["software engineering and coding"],
        n_results=1,
    )

    # Assertions
    assert len(results["documents"][0]) == 1
    assert results["documents"][0][0] == "Python is a programming language."
    assert results["ids"][0][0] == "id_1"
