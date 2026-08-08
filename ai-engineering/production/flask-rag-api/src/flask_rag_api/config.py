import os


class Config:
    """Base Configuration."""

    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    CHROMA_DB_DIR: str = os.getenv("CHROMA_DB_DIR", "./_tmp/chroma_db")
    CHROMA_COLLECTION: str = os.getenv("CHROMA_COLLECTION", "pdf_rag_collection_openai")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_EMBEDDING_MODEL: str = os.getenv(
        "OLLAMA_EMBEDDING_MODEL", "nomic-embed-text"
    )
    LLM_MODEL: str = os.getenv("LLM_MODEL", "qwen3:1.7b")
    PORT: int = int(os.getenv("PORT", "5001"))
    FLASK_DEBUG: bool = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")


class DevelopmentConfig(Config):
    """Development Configuration."""

    FLASK_DEBUG: bool = True


class TestingConfig(Config):
    """Testing Configuration."""

    TESTING: bool = True
    FLASK_DEBUG: bool = False
    CHROMA_DB_DIR: str = "./_tmp/test_chroma_db"


class ProductionConfig(Config):
    """Production Configuration."""

    FLASK_DEBUG: bool = False


def get_config() -> Config:
    """Return appropriate configuration class based on FLASK_ENV environment variable."""
    env = os.getenv("FLASK_ENV", "production").lower()
    if env == "development":
        return DevelopmentConfig()
    elif env == "testing":
        return TestingConfig()
    return ProductionConfig()
