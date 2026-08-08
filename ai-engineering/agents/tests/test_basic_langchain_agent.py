"""Unit tests for the Basic LangChain Tool Selection Agent and its individual tools."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

from langchain_classic.agents import AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.language_models.chat_models import BaseChatModel

# Add parent directory to sys.path to enable direct module import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from basic_langchain_agent import (
    AgentLoadingStatusHandler,
    calculator,
    create_basic_agent,
    database_lookup,
    get_agent_tools,
    get_configured_llm,
    get_weather,
    web_search,
    word_counter,
)


def test_calculator_tool_valid():
    """Test calculator tool with valid mathematical expressions."""

    res1 = calculator.invoke({"expression": "45 * 12 + 350"})
    assert res1 == "890"

    res2 = calculator.invoke({"expression": "(100 - 20) / 4"})
    assert float(res2) == 20.0

    res3 = calculator.invoke({"expression": "2 ** 3"})
    assert res3 == "8"


def test_calculator_tool_invalid():
    """Test calculator tool with malformed expressions."""

    res = calculator.invoke({"expression": "invalid + math"})
    assert "Error evaluating expression" in res


def test_word_counter_tool_valid():
    """Test word_counter tool with standard text."""

    sample_text = "LangChain agents select tools dynamically"
    res = word_counter.invoke({"text": sample_text})
    assert "Word count: 5" in res
    assert "Character count: 41" in res
    assert "Line count: 1" in res


def test_word_counter_tool_empty():
    """Test word_counter tool with empty or whitespace text."""

    res = word_counter.invoke({"text": "   "})
    assert "Word count: 0" in res
    assert "Character count: 0" in res


def test_get_weather_tool_known_city():
    """Test get_weather tool for known cities."""

    res = get_weather.invoke({"city": "Tokyo"})
    assert "Tokyo" in res
    assert "24°C" in res


def test_get_weather_tool_unknown_city():
    """Test get_weather tool for unlisted cities."""

    res = get_weather.invoke({"city": "Atlantis"})
    assert "Atlantis" in res
    assert "21°C" in res


def test_database_lookup_tool_known_user():
    """Test database_lookup tool with existing user ID."""

    res = database_lookup.invoke({"user_id": 101})
    assert "Alice Smith" in res
    assert "Shipped" in res


def test_database_lookup_tool_unknown_user():
    """Test database_lookup tool with non-existent user ID."""

    res = database_lookup.invoke({"user_id": 999})
    assert "No user record found" in res


def test_web_search_tool_metadata():
    """Verify web_search tool name and description metadata."""

    assert web_search.name == "web_search"
    assert "DuckDuckGo" in web_search.description
    assert "not know the answer" in web_search.description


def test_web_search_tool_mocked():
    """Test web_search tool execution with mocked DuckDuckGo search output."""

    with patch.object(
        DuckDuckGoSearchRun, "_run", return_value="Mocked search results"
    ):
        res = web_search.invoke({"query": "Python 3.14 features"})
        assert res == "Mocked search results"


def test_get_agent_tools():
    """Verify tool collection contains all expected tools including web_search."""

    tools = get_agent_tools()
    tool_names = [t.name for t in tools]
    assert len(tools) == 5
    assert "calculator" in tool_names
    assert "word_counter" in tool_names
    assert "get_weather" in tool_names
    assert "database_lookup" in tool_names
    assert "web_search" in tool_names


def test_create_basic_agent_construction():
    """Verify AgentExecutor can be created with a mock model."""

    mock_model = MagicMock(spec=BaseChatModel)
    mock_model._combine_llm_outputs = MagicMock(return_value={})

    agent_executor = create_basic_agent(model=mock_model, verbose=False)
    assert isinstance(agent_executor, AgentExecutor)
    assert len(agent_executor.tools) == 5


def test_agent_execution_mocked():
    """Test running AgentExecutor with a mocked return value."""

    mock_executor = MagicMock(spec=AgentExecutor)
    mock_executor.invoke.return_value = {
        "input": "What is 45 * 12 + 350?",
        "output": "890",
    }

    result = mock_executor.invoke({"input": "What is 45 * 12 + 350?"})
    assert result["output"] == "890"


def test_get_configured_llm_factory():
    """Verify get_configured_llm returns a BaseChatModel instance."""

    model = get_configured_llm(provider="ollama", model_name="qwen3:1.7b")
    assert isinstance(model, BaseChatModel)


def test_web_search_tool_failure_fallback():
    """Test web_search tool gracefully returns a fallback message on exception."""

    with patch.object(
        DuckDuckGoSearchRun,
        "run",
        side_effect=Exception("Rate limit or connection timeout"),
    ):
        res = web_search.invoke({"query": "Latest AI news 2026"})
        assert "[Fallback] Web search is currently unavailable" in res
        assert "Rate limit or connection timeout" in res
        assert "Latest AI news 2026" in res


def test_agent_loading_status_handler():
    """Verify AgentLoadingStatusHandler tracks state transitions correctly."""

    handler = AgentLoadingStatusHandler()
    assert handler.current_state == "IDLE"

    handler.on_chain_start({}, {})
    assert handler.current_state == "THINKING"

    handler.on_tool_start({"name": "web_search"}, "AI news")
    assert handler.current_state == "LOADING"
    assert "Executing tool 'web_search'" in handler.logs[-1]

    handler.on_tool_end("Search results string")
    assert handler.current_state == "COMPLETED"

    handler.on_tool_error(RuntimeError("Tool failed"))
    assert handler.current_state == "ERROR"

    handler.on_chain_end({})
    assert handler.current_state == "FINISHED"


def test_create_basic_agent_with_callbacks():
    """Verify create_basic_agent configures callbacks and handles parsing errors."""

    mock_model = MagicMock(spec=BaseChatModel)
    mock_model._combine_llm_outputs = MagicMock(return_value={})
    handler = AgentLoadingStatusHandler()

    agent_executor = create_basic_agent(
        model=mock_model, callbacks=[handler], verbose=False
    )
    assert isinstance(agent_executor, AgentExecutor)
    assert agent_executor.handle_parsing_errors is True
    assert handler in agent_executor.callbacks
