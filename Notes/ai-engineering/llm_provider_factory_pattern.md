# Production LLM Architecture: Provider Factory & Package Layout

## Overview

When building multi-model or multi-provider AI applications, hardcoding API client
instantiations and scattering procedural logic across a single file creates technical
debt, tight coupling, and security vulnerabilities.

Adopting a **production-grade package directory layout** (`src/config/`, `src/core/`,
`src/services/`) along with the **Factory Pattern**, **Registry Pattern**, and
**Object-Oriented Design (OOP)** decouples configuration parsing, model creation,
and evaluation logic into modular, testable components.

---

## 1. Production Package Layout

An enterprise-grade LLM application organizes components into namespaced packages:

```
courses/AI Engineer Agentic Track- The Complete Agent MCP Course/
├── src/
│   ├── __init__.py           # Package root
│   ├── config/               # Single Source of Truth (SSOT)
│   │   ├── __init__.py
│   │   └── providers.py      # ProviderRegistry & ProviderMeta dataclass
│   ├── core/                 # Neutral core domain & factories
│   │   ├── __init__.py
│   │   └── llm_factory.py    # Centralized LLMFactory class
│   └── services/             # Application services & business logic
│       ├── __init__.py
│       └── evaluator.py      # LLMEvaluator class (benchmarking engine)
└── lab_01.py                 # High-level entrypoint & workflow driver
```

---

## 2. Core Package Modules & Design Patterns

### A. Registry Package (`src/config/providers.py`)
Stores provider metadata (base URLs, environment key names, key prefix lengths) in a centralized,
immutable registry data structure.

```python
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class ProviderMeta:
    base_url: Optional[str]
    env_key: str
    prefix_len: int = 4
    optional: bool = True


PROVIDER_REGISTRY: Dict[str, ProviderMeta] = {
    "openai": ProviderMeta(
        base_url=None, env_key="OPENAI_API_KEY", prefix_len=8, optional=False
    ),
    "anthropic": ProviderMeta(
        base_url="https://api.anthropic.com/v1/", env_key="ANTHROPIC_API_KEY"
    ),
    "ollama": ProviderMeta(
        base_url="http://localhost:11434/v1",
        env_key="OLLAMA_API_KEY",
        prefix_len=0,
    ),
}
```

### B. Core Factory Package (`src/core/llm_factory.py`)
Encapsulates client instantiation logic into a unified interface (`LLMFactory.get_client()`).

```python
import os
from openai import OpenAI
from src.config.providers import PROVIDER_REGISTRY


class LLMFactory:
    """Centralized Model and Client Factory."""

    @classmethod
    def get_client(cls, provider: str) -> OpenAI:
        meta = PROVIDER_REGISTRY.get(provider.lower())
        if not meta:
            raise ValueError(f"Unsupported provider: {provider}")

        api_key = os.getenv(meta.env_key) or (
            "ollama" if provider == "ollama" else None
        )
        return OpenAI(api_key=api_key, base_url=meta.base_url)
```

### C. Services Package (`src/services/evaluator.py`)
Encapsulates benchmark question generation, model evaluation tracking, and judge ranking.

```python
from typing import List, Dict, Optional
from src.core.llm_factory import LLMFactory


class LLMEvaluator:
    """Encapsulates multi-model benchmark generation, execution, and judging."""

    def __init__(self) -> None:
        self.competitors: List[str] = []
        self.answers: List[str] = []

    def record_answer(self, model_name: str, answer: str) -> None:
        self.competitors.append(model_name)
        self.answers.append(answer)

    def evaluate_model(
        self,
        provider: str,
        model_name: str,
        messages: List[Dict[str, str]],
    ) -> Optional[str]:
        client = LLMFactory.get_client(provider)
        response = client.chat.completions.create(
            model=model_name, messages=messages
        )
        answer = response.choices[0].message.content or ""
        self.record_answer(model_name, answer)
        return answer
```

---

## 3. Interview Questions & Answers (5 YOE Level)

### Q1: Conceptual / Package Design
**Question**: Why is organizing code into dedicated package folders (`src/config/`, `src/core/`,
`src/services/`) considered production-grade over flat module files?

**Answer**:
- **Namespacing & Modularity**: Avoids global namespace pollution and circular import cycles.
- **Clear Architectural Boundaries**: `core/` modules never import from `services/` or higher
  script layers.
- **Packaging & Deployment**: Enables clean distribution as a Python package (`pip install -e .`).

---

### Q2: Architecture / System Design
**Question**: How would you extend `LLMEvaluator` to support concurrent asynchronous
model evaluations across multiple providers (e.g., parallel model benchmarking)?

**Answer**:
1. Swap `OpenAI` synchronous client for `AsyncOpenAI` in `LLMFactory`.
2. Use Python's `asyncio.gather()` inside `LLMEvaluator.evaluate_all_async()`:

```python
import asyncio


async def evaluate_all(evaluator: LLMEvaluator, tasks: List[dict]):
    coros = [
        evaluator.evaluate_model_async(
            t["provider"], t["model"], t["messages"]
        )
        for t in tasks
    ]
    return await asyncio.gather(*coros)
```

---

## References

- [GoF Design Patterns: Factory](https://refactoring.guru/design-patterns/factory-method)
- [12-Factor App: Config Principles](https://12factor.net/config)
