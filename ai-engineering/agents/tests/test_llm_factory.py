"""Unit tests for the production LLM Model Factory."""

import sys
from pathlib import Path

from langchain_core.language_models.chat_models import BaseChatModel

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from llm_factory import get_configured_llm


def test_get_configured_llm_default_ollama():
    """Test get_configured_llm defaults to Ollama BaseChatModel."""
    model = get_configured_llm(provider="ollama", model_name="qwen3:1.7b")
    assert isinstance(model, BaseChatModel)


def test_get_configured_llm_env_override(monkeypatch):
    """Test get_configured_llm respects LLM_PROVIDER and LLM_MODEL environment variables."""
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setenv("LLM_MODEL", "qwen3:1.7b")
    model = get_configured_llm()
    assert isinstance(model, BaseChatModel)
