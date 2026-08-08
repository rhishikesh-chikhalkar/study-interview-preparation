import os
from typing import Dict, List
import requests

from src.core.llm_factory import LLMFactory
from src.services.evaluator import LLMEvaluator


def main() -> None:
    """Main execution workflow for LLM competitor evaluation."""

    # 1. Audit environment keys across all registered providers
    LLMFactory.audit_keys()

    # Read Single Source of Truth (SSOT) from environment / .env
    primary_provider = os.getenv("LLM_PROVIDER", "ollama")
    primary_model = os.getenv("LLM_MODEL", "qwen3:1.7b")

    print(
        f"\nActive SSOT Config: Provider='{primary_provider}', Model='{primary_model}'"
    )

    # 2. Instantiate Evaluator Engine
    evaluator = LLMEvaluator()

    # 3. Generate benchmark question
    print(f"\n--- Generating Benchmark Question via {primary_provider} ---")
    question = evaluator.generate_question(
        provider=primary_provider, model_name=primary_model
    )

    messages: List[Dict[str, str]] = [{"role": "user", "content": question}]

    # 4. Evaluate Competitors
    # Competitor 1: OpenAI (if key available)
    if os.getenv("OPENAI_API_KEY"):
        print("\n--- Evaluating Competitor: OpenAI (gpt-5.4-nano) ---")
        evaluator.evaluate_model(
            provider="openai",
            model_name="gpt-5.4-nano",
            messages=messages,
            reasoning_effort="none",
        )

    # Competitor 2: Ollama Local
    print("\n--- Evaluating Competitor: Ollama Local ---")
    try:
        models_res = requests.get("http://localhost:11434/v1/models").json()
        print("Available Local Models:")
        local_models = [m.get("id") for m in models_res.get("data", [])]
        for m in local_models:
            print(f" - {m}")

        chat_models = [
            m
            for m in local_models
            if not m.startswith("nomic-embed") and not m.endswith("-cloud")
        ]
        eval_model = chat_models[0] if chat_models else primary_model

        evaluator.evaluate_model(
            provider="ollama",
            model_name=eval_model,
            messages=messages,
        )
    except Exception as err:
        print(f"Ollama local service unavailable: {err}")

    # 5. Judge and Rank Competitors
    print(f"\n--- Running Judge & Ranking via {primary_provider} ---")
    evaluator.judge_and_rank(
        question=question,
        judge_provider=primary_provider,
        judge_model_name=primary_model,
    )


if __name__ == "__main__":
    main()
