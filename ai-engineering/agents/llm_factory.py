"""Production LLM Model Factory.

Provides a unified factory function to instantiate BaseChatModel instances
dynamically using LangChain's init_chat_model.
"""

import os

from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel


def get_configured_llm(
    provider: str | None = None,
    model_name: str | None = None,
    temperature: float = 0,
) -> BaseChatModel:
    """Return a production-configured BaseChatModel instance using init_chat_model.

    Reads environment variables LLM_PROVIDER and LLM_MODEL if not explicitly provided.
    Supported providers include: 'ollama', 'openai', 'anthropic', etc.

    Args:
        provider: Provider identifier string (e.g. 'ollama', 'openai', 'anthropic').
        model_name: Name of the model to instantiate.
        temperature: Sampling temperature for generation.

    Returns:
        Configured BaseChatModel ready for agent or chain execution.
    """

    resolved_provider = (provider or os.getenv("LLM_PROVIDER", "ollama")).lower()
    default_models = {
        "ollama": "qwen3:1.7b",
        "openai": "gpt-4o-mini",
        "anthropic": "claude-3-5-sonnet-20241022",
    }
    resolved_model = (
        model_name
        or os.getenv("LLM_MODEL")
        or default_models.get(resolved_provider, "qwen3:1.7b")
    )

    return init_chat_model(
        model=resolved_model,
        model_provider=resolved_provider,
        temperature=temperature,
    )
