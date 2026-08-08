"""Basic LangChain Agent Implementation.

This module demonstrates the core concepts of LangChain Agents:
1. Reasoning Engine: Using an LLM (model) to dynamically decide actions.
2. Tools: Pure functions wrapped with @tool containing action descriptions.
3. Execution Loop: AgentExecutor facilitating the ReAct/Tool-Calling loop
   (Input -> Reasoning -> Action -> Observation -> Final Answer).
"""

import ast
import operator
from typing import Any

from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from llm_factory import get_configured_llm


@tool
def calculator(expression: str) -> str:
    """Evaluate basic arithmetic expressions safely.

    Use this tool when the user asks to solve mathematical expressions, perform calculations,
    or evaluate formulas.

    Args:
        expression: A string mathematical expression (e.g. "45 * 12 + 350" or "(100 - 25) / 5").

    Returns:
        The calculated numerical result as a string.
    """

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def _eval(node: ast.AST) -> float | int:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in operators:
                return operators[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type}")
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in operators:
                return operators[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type}")
        raise ValueError(f"Unsupported expression node: {type(node)}")

    try:
        parsed_ast = ast.parse(expression.strip(), mode="eval")
        result = _eval(parsed_ast.body)
        return str(result)
    except Exception as err:
        return f"Error evaluating expression '{expression}': {err}"


@tool
def word_counter(text: str) -> str:
    """Count words and characters in a given text snippet.

    Use this tool when the user explicitly asks to count words, sentences, or characters in text.

    Args:
        text: The input text to analyze.

    Returns:
        A structured string summarizing word count, character count, and line count.
    """

    cleaned = text.strip()
    if not cleaned:
        return "Word count: 0 | Character count: 0 | Line count: 0"

    words = cleaned.split()
    chars = len(cleaned)
    lines = len(cleaned.splitlines())
    return f"Word count: {len(words)} | Character count: {chars} | Line count: {lines}"


@tool
def get_weather(city: str) -> str:
    """Get current weather forecast and temperature for a given city.

    Use this tool when user asks for weather conditions, temperature, or forecasts for a city.

    Args:
        city: Name of the city (e.g. "Tokyo", "London", "New York").

    Returns:
        Weather report string.
    """

    mock_weather_db = {
        "tokyo": "Sunny, 24°C (75°F), Humidity 55%",
        "london": "Light rain, 15°C (59°F), Humidity 82%",
        "new york": "Partly cloudy, 20°C (68°F), Humidity 60%",
        "mumbai": "Humid & warm, 31°C (88°F), Humidity 78%",
        "paris": "Clear sky, 22°C (71°F), Humidity 50%",
    }

    key = city.strip().lower()
    if key in mock_weather_db:
        return f"Weather for {city.title()}: {mock_weather_db[key]}"
    return f"Weather for '{city.title()}': Mild, 21°C (70°F) with light breeze."


@tool
def database_lookup(user_id: int) -> str:
    """Fetch user profile and recent order details from internal database.

    Use this tool when user asks about order status, account details, or purchase history.

    Args:
        user_id: The unique numerical ID of the user.

    Returns:
        User record and status string.
    """

    mock_user_db = {
        101: {
            "name": "Alice Smith",
            "tier": "Gold",
            "recent_order": "#ORD-8821",
            "status": "Shipped",
        },
        102: {
            "name": "Bob Jones",
            "tier": "Silver",
            "recent_order": "#ORD-9934",
            "status": "Processing",
        },
        103: {
            "name": "Charlie Brown",
            "tier": "Platinum",
            "recent_order": "#ORD-1002",
            "status": "Delivered",
        },
    }

    if user_id in mock_user_db:
        record = mock_user_db[user_id]
        return (
            f"User ID {user_id} ({record['name']}): Tier={record['tier']}, "
            f"Recent Order={record['recent_order']}, Status={record['status']}"
        )
    return f"No user record found for User ID {user_id}."


class AgentLoadingStatusHandler(BaseCallbackHandler):
    """Callback handler to track and report agent execution and tool loading states."""

    def __init__(self) -> None:
        self.current_state: str = "IDLE"
        self.logs: list[str] = []

    def _update_state(self, state: str, message: str = "") -> None:
        self.current_state = state
        entry = f"[{state}] {message}".strip() if message else f"[{state}]"
        self.logs.append(entry)

    def on_chain_start(
        self, serialized: dict[str, Any], inputs: dict[str, Any], **kwargs: Any
    ) -> None:
        self._update_state("THINKING", "Initializing agent reasoning process")

    def on_tool_start(
        self, serialized: dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        tool_name = serialized.get("name", "unknown_tool")
        self._update_state(
            "LOADING", f"Executing tool '{tool_name}' with input: {input_str}"
        )

    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        self._update_state("COMPLETED", "Tool execution finished successfully")

    def on_tool_error(self, error: BaseException, **kwargs: Any) -> None:
        self._update_state("ERROR", f"Tool encountered an error: {error}")

    def on_chain_end(self, outputs: dict[str, Any], **kwargs: Any) -> None:
        self._update_state("FINISHED", "Agent execution finished")


@tool
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo.

    Use this tool when you do not know the answer or need current real-world information,
    news, or external facts.

    Args:
        query: The search query string or keywords.

    Returns:
        Search result snippets, or a fallback error message if search fails.
    """

    try:
        ddg = DuckDuckGoSearchRun()
        return ddg.run(query)
    except Exception as err:
        return (
            f"[Fallback] Web search is currently unavailable for query '{query}'. "
            f"Reason: {err}. Please proceed using internal knowledge."
        )


def get_agent_tools() -> list[Any]:
    """Return all available tools for the basic agent."""

    return [calculator, word_counter, get_weather, database_lookup, web_search]


def create_basic_agent(
    model: BaseChatModel | None = None,
    tools: list[Any] | None = None,
    callbacks: list[BaseCallbackHandler] | None = None,
    verbose: bool = True,
) -> AgentExecutor:
    """Create and return a tool-calling LangChain AgentExecutor.

    Args:
        model: Language model instance (defaults to get_configured_llm()).
        tools: List of tools available to the agent (defaults to get_agent_tools()).
        callbacks: Optional list of callback handlers for loading states/monitoring.
        verbose: Whether to log intermediate reasoning steps and tool execution.

    Returns:
        Configured AgentExecutor ready to handle inputs.
    """

    if model is None:
        model = get_configured_llm()

    if tools is None:
        tools = get_agent_tools()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an intelligent assistant equipped with specialized tools. "
                "Carefully inspect user requests and choose the appropriate tool when "
                "calculation, word counting, weather lookup, user database queries, or web "
                "search is requested. Search the web when you do not know the answer or need "
                "current information. If web search tool returns a fallback message, answer "
                "gracefully based on your base knowledge. If no tool is needed, respond directly.",
            ),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(model, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose,
        callbacks=callbacks,
        handle_parsing_errors=True,
    )
    return agent_executor


def run_demo_queries(agent_executor: AgentExecutor) -> None:
    """Run sample queries demonstrating dynamic tool selection."""

    sample_queries = [
        "What is 45 * 12 + 350?",
        (
            "How many words are in the text 'LangChain agents dynamically pick "
            "tools based on user input'?"
        ),
        "What is the weather in Tokyo right now?",
        "Can you check the order status for user ID 102?",
        "What is the capital of France?",
    ]

    print("\n" + "=" * 60)
    print("LANGCHAIN TOOL SELECTION AGENT DEMO")
    print("=" * 60 + "\n")

    for idx, query in enumerate(sample_queries, start=1):
        print(f"[{idx}] User Query: '{query}'")
        try:
            handler = AgentLoadingStatusHandler()
            response = agent_executor.invoke(
                {"input": query}, config={"callbacks": [handler]}
            )
            print(f"    Agent Output: {response['output']}")
            print(f"    Loading State Trace: {handler.logs}\n")
        except Exception as err:
            print(f"    Execution Note: {err}\n")


if __name__ == "__main__":
    try:
        agent_executor = create_basic_agent(verbose=True)
        run_demo_queries(agent_executor)
    except Exception as error:
        print(f"Agent Initialization Info: {error}")
