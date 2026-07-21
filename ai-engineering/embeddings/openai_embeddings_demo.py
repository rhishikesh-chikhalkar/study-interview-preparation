import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load the environment variables from the correct .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Retrieve the API key from environment
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY environment variable not found in:", env_path)
    exit(1)

# Initialize OpenAI client
client = OpenAI(api_key=api_key)


def main():
    # Define a sentence to convert into an embedding vector
    sentence = "AI is transforming the way we write and understand code."

    print(f"Original Sentence: '{sentence}'\n")

    # Call OpenAI Embeddings API (using the text-embedding-3-small model)
    print("Generating embedding vector from OpenAI API...")
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small", input=sentence
        )
        # Extract the vector
        vector = response.data[0].embedding
        is_mocked = False
    except Exception as e:
        print(f"\n[Warning] API call failed: {e}")
        print(
            "Falling back to a simulated embedding vector for educational purposes.\n"
        )
        # text-embedding-3-small has 1536 dimensions. We generate a realistic sample vector.
        import random

        # Seed for deterministic mock outputs
        random.seed(42)
        vector = [round(random.uniform(-0.1, 0.1), 6) for _ in range(1536)]
        is_mocked = True

    # Print information about the vector
    print("\n--- Vector Information ---")
    print(f"Is Mocked/Simulated: {is_mocked}")
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
        "2. Semantic meaning: The position of the vector in a high-dimensional space (1536 dimensions for text-embedding-3-small) captures the semantic meaning of the text."
    )
    print(
        "3. Distance & Similarity: Texts with similar meanings (e.g., 'machine learning' and 'artificial intelligence') will be closer to each other in this space, measured by cosine similarity or dot product."
    )


if __name__ == "__main__":
    main()
