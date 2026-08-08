import os
from typing import Dict

from dotenv import load_dotenv
from openai import OpenAI

from src.config.providers import PROVIDER_REGISTRY, ProviderMeta

load_dotenv(override=True)


class LLMFactory:
    """Production-grade Factory for instantiating LLM clients."""

    _registry: Dict[str, ProviderMeta] = PROVIDER_REGISTRY

    @classmethod
    def get_client(cls, provider: str) -> OpenAI:
        """Instantiates an OpenAI-compatible client for a given provider."""

        provider_name = provider.lower()
        meta = cls._registry.get(provider_name)
        if not meta:
            raise ValueError(f"Unsupported provider: '{provider}'")

        api_key = os.getenv(meta.env_key) or (
            "ollama" if provider_name == "ollama" else None
        )

        if not api_key:
            raise ValueError(
                f"API Key for '{meta.env_key}' is missing. "
                "Set it in .env or use 'ollama' locally."
            )

        return OpenAI(api_key=api_key, base_url=meta.base_url)

    @classmethod
    def audit_keys(cls) -> None:
        """Audits configured provider keys without exposing secrets."""

        print("=== LLM Provider Key Audit ===")
        for name, meta in cls._registry.items():
            key = os.getenv(meta.env_key)
            display_name = name.capitalize() if name != "openai" else "OpenAI"
            if key:
                prefix = key[: meta.prefix_len] if meta.prefix_len > 0 else "[LOCAL]"
                print(f"✓ {display_name:<12}: Set (Prefix: {prefix})")
            else:
                opt_str = " (optional)" if meta.optional else " (REQUIRED)"
                print(f"✗ {display_name:<12}: Not set{opt_str}")
