from langchain_ollama import OllamaEmbeddings


def main():
    # Define a sentence to convert into an embedding vector
    sentence = "AI is transforming the way we write and understand code."

    print(f"Original Sentence: '{sentence}'\n")
    print("Generating embedding vector using local Ollama (nomic-embed-text)...")

    try:
        # Initialize OllamaEmbeddings using nomic-embed-text
        embeddings = OllamaEmbeddings(model="nomic-embed-text")

        # Convert sentence into a vector
        vector = embeddings.embed_query(sentence)

        # Print information about the vector
        print("\n--- Vector Information ---")
        print(f"Vector data type: {type(vector)}")
        print(f"Vector dimension (length): {len(vector)}")
        print(f"Sample values (first 10 components): {vector[:10]}")
        print(f"Sample values (last 5 components): {vector[-5:]}")
        print("--------------------------\n")

        # Explain what it represents
        print("What does this vector represent?")
        print(
            "1. Numerical representation: An embedding is a vector (list of floating-point numbers) that represents a piece of text (word, sentence, or document)."
        )
        print(
            "2. Semantic meaning: The position of the vector in a high-dimensional space (768 dimensions for nomic-embed-text) captures the semantic meaning of the text."
        )
        print(
            "3. Distance & Similarity: Texts with similar meanings will be closer to each other in this space, measured by cosine similarity or dot product."
        )

    except Exception as e:
        print(f"\n[Error] Failed to generate embedding with Ollama: {e}")
        print(
            "Make sure Ollama is running (`ollama serve`) and the model is downloaded (`ollama pull nomic-embed-text`)."
        )


if __name__ == "__main__":
    main()
