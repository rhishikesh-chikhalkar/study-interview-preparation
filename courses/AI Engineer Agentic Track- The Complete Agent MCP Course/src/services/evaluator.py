import json
import os
from typing import Any, Dict, List, Optional

from src.core.llm_factory import LLMFactory

DEFAULT_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
DEFAULT_MODEL = os.getenv("LLM_MODEL", "qwen3:1.7b")

try:
    from IPython.display import Markdown, display
except ImportError:

    def display(obj: Any) -> None:
        """Fallback display function when outside Jupyter notebooks."""

        print(obj)

    def Markdown(text: str) -> str:
        """Fallback Markdown function when outside Jupyter notebooks."""

        return text


class LLMEvaluator:
    """Encapsulates multi-model benchmark generation, execution, and judging."""

    def __init__(self) -> None:
        """Initializes the evaluator with empty competitor tracking."""

        self.competitors: List[str] = []
        self.answers: List[str] = []

    def record_answer(self, model_name: str, answer: str) -> None:
        """Records a model response and renders markdown output."""

        self.competitors.append(model_name)
        self.answers.append(answer)
        display(Markdown(answer))

    def generate_question(
        self,
        provider: str = DEFAULT_PROVIDER,
        model_name: str = DEFAULT_MODEL,
    ) -> str:
        """Generates a benchmark question using the specified LLM."""

        try:
            client = LLMFactory.get_client(provider)
            prompt = (
                "Please come up with a challenging, nuanced question with "
                "a succinct answer, that I can ask a number of LLMs to evaluate "
                "their intelligence. Not a mathematical puzzle, but a "
                "thought-provoking question that requires intelligent insight. "
                "Include in your question that the answer must be short. "
                "Answer only with the question, no explanation."
            )
            messages: List[Dict[str, str]] = [{"role": "user", "content": prompt}]

            response = client.chat.completions.create(
                model=model_name, messages=messages
            )
            question = response.choices[0].message.content or ""
            display(Markdown(question))
            return question
        except Exception as err:
            print(f"Question generation failed on provider '{provider}': {err}")
            fallback_q = (
                "What is the single most important principle in designing "
                "scalable distributed systems? Answer in 1-2 sentences."
            )
            print(f"Using fallback question: {fallback_q}")
            return fallback_q

    def evaluate_model(
        self,
        provider: str,
        model_name: str,
        messages: List[Dict[str, str]],
        reasoning_effort: Optional[str] = None,
    ) -> Optional[str]:
        """Queries a competitor LLM model and records its response."""

        try:
            client = LLMFactory.get_client(provider)
            kwargs: Dict[str, Any] = {
                "model": model_name,
                "messages": messages,
            }
            if reasoning_effort:
                kwargs["reasoning_effort"] = reasoning_effort

            response = client.chat.completions.create(**kwargs)
            answer = response.choices[0].message.content or ""
            self.record_answer(model_name, answer)
            return answer
        except Exception as err:
            print(f"Evaluation skipped for '{model_name}' ({provider}): {err}")
            return None

    def judge_and_rank(
        self,
        question: str,
        judge_provider: str = DEFAULT_PROVIDER,
        judge_model_name: str = DEFAULT_MODEL,
    ) -> List[str]:
        """Evaluates competitor answers using a judge LLM and returns ranks."""

        if not self.answers:
            print("No competitor answers recorded to judge.")
            return []

        formatted_responses = ""
        for index, answer in enumerate(self.answers):
            formatted_responses += (
                f"# Response from competitor {index + 1}\n\n{answer}\n\n"
            )

        judge_prompt = (
            f"You are judging a competition between {len(self.competitors)} "
            f"competitors.\nEach model was given this question:\n\n{question}\n\n"
            "Evaluate each response for clarity and strength of argument, "
            "and rank them in order of best to worst.\n"
            "Respond with JSON, and only JSON, in this exact format:\n"
            '{"results": ["1", "2", ...]}\n\n'
            f"Competitor responses:\n\n{formatted_responses}\n"
            "Respond with JSON with the ranked order, nothing else."
        )

        try:
            judge_client = LLMFactory.get_client(judge_provider)
            messages: List[Dict[str, str]] = [{"role": "user", "content": judge_prompt}]
            response = judge_client.chat.completions.create(
                model=judge_model_name, messages=messages
            )
            raw_result = response.choices[0].message.content or ""
            print(f"Raw Judge Output: {raw_result}")

            parsed = json.loads(raw_result)
            rankings = parsed.get("results", [])
            ranked_models: List[str] = []

            print("\n=== Final Competition Leaderboard ===")
            for index, rank_str in enumerate(rankings):
                comp_idx = int(rank_str) - 1
                if 0 <= comp_idx < len(self.competitors):
                    competitor = self.competitors[comp_idx]
                    ranked_models.append(competitor)
                    print(f"Rank {index + 1}: {competitor}")

            return ranked_models
        except Exception as err:
            print(f"Judgement failed using provider '{judge_provider}': {err}")
            return []
