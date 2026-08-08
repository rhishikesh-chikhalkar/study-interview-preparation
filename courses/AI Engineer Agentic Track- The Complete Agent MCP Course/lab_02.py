import os

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from src.core.llm_factory import LLMFactory

load_dotenv(override=True)


def read_pdf_text(file_path: str) -> str:
    """Extracts text content from a PDF file safely using list accumulation."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found at path: '{file_path}'")

    text_chunks: list[str] = []
    with open(file_path, "rb") as pdf_file:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_chunks.append(text)

    return "".join(text_chunks)


def read_text_file(file_path: str) -> str:
    """Reads and returns text content from a plain text file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Text file not found at path: '{file_path}'")

    with open(file_path, "r", encoding="utf-8") as text_file:
        return text_file.read()


def main() -> None:
    provider = os.getenv("LLM_PROVIDER", "ollama")
    model_name = os.getenv("LLM_MODEL", "qwen3:1.7b")

    llm: OpenAI = LLMFactory.get_client(provider)
    print(
        f"Initialized '{llm.__class__.__name__}' for provider '{provider}' using model '{model_name}'."
    )

    pdf_file_path = "src/assets/linkedin.pdf"
    pdf_text = read_pdf_text(pdf_file_path)
    print(f"Extracted {len(pdf_text)} characters from PDF.")

    text_file_path = "src/assets/summary.txt"
    summary_text = read_text_file(text_file_path)
    print(f"Extracted {len(summary_text)} characters from text file.")


if __name__ == "__main__":
    main()
