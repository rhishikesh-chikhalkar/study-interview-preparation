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


def get_agent_tools() -> list[Any]:
    """Return all available tools for the basic agent."""

    return [calculator, word_counter, get_weather, database_lookup]


def create_basic_agent(
    model: BaseChatModel | None = None,
    tools: list[Any] | None = None,
    verbose: bool = True,
) -> AgentExecutor:
    """Create and return a tool-calling LangChain AgentExecutor.

    Args:
        model: Language model instance (defaults to get_configured_llm()).
        tools: List of tools available to the agent (defaults to get_agent_tools()).
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
                "Carefully inspect user requests and choose the appropriate tool when calculation, "
                "word counting, weather lookup, or user database queries are requested. "
                "If no tool is needed, respond directly.",
            ),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=verbose)
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
            response = agent_executor.invoke({"input": query})
            print(f"    Agent Output: {response['output']}\n")
        except Exception as err:
            print(f"    Execution Note: {err}\n")


if __name__ == "__main__":
    try:
        agent_executor = create_basic_agent(verbose=True)
        run_demo_queries(agent_executor)
    except Exception as error:
        print(f"Agent Initialization Info: {error}")
