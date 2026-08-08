from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class ProviderMeta:
    """Metadata specification for an LLM Provider."""

    base_url: Optional[str]
    env_key: str
    prefix_len: int = 4
    optional: bool = True


GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

PROVIDER_REGISTRY: Dict[str, ProviderMeta] = {
    "openai": ProviderMeta(
        base_url=None,
        env_key="OPENAI_API_KEY",
        prefix_len=8,
        optional=False,
    ),
    "anthropic": ProviderMeta(
        base_url="https://api.anthropic.com/v1/",
        env_key="ANTHROPIC_API_KEY",
        prefix_len=7,
    ),
    "google": ProviderMeta(
        base_url=GEMINI_BASE_URL,
        env_key="GOOGLE_API_KEY",
        prefix_len=2,
    ),
    "deepseek": ProviderMeta(
        base_url="https://api.deepseek.com/v1",
        env_key="DEEPSEEK_API_KEY",
        prefix_len=3,
    ),
    "groq": ProviderMeta(
        base_url="https://api.groq.com/openai/v1",
        env_key="GROQ_API_KEY",
        prefix_len=4,
    ),
    "grok": ProviderMeta(
        base_url="https://api.x.ai/v1",
        env_key="GROK_API_KEY",
        prefix_len=4,
    ),
    "openrouter": ProviderMeta(
        base_url="https://openrouter.ai/api/v1",
        env_key="OPENROUTER_API_KEY",
        prefix_len=6,
    ),
    "ollama": ProviderMeta(
        base_url="http://localhost:11434/v1",
        env_key="OLLAMA_API_KEY",
        prefix_len=0,
    ),
}
