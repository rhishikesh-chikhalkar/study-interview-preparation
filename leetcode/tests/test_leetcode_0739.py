import importlib
import pytest

leetcode_0739 = importlib.import_module("leetcode.0739")
Solution = leetcode_0739.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize("method_name", ["dailyTemperatures", "dailyTemperatures_dp"])
@pytest.mark.parametrize(
    "temperatures,expected",
    [
        # Standard examples
        ([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]),
        ([30, 40, 50, 60], [1, 1, 1, 0]),
        ([30, 60, 90], [1, 1, 0]),
        # Single element
        ([50], [0]),
        # Strictly decreasing
        ([90, 80, 70, 60, 50], [0, 0, 0, 0, 0]),
        # Strictly increasing
        ([30, 35, 40, 45, 50], [1, 1, 1, 1, 0]),
        # All identical elements
        ([70, 70, 70, 70], [0, 0, 0, 0]),
        # Duplicate values with warmer later
        ([70, 70, 70, 75], [3, 2, 1, 0]),
        # Oscillating / V-shaped values
        ([80, 70, 60, 70, 80, 90], [5, 3, 1, 1, 1, 0]),
        ([50, 40, 60, 30, 70], [2, 1, 2, 1, 0]),
        # Large temperature jumps
        ([30, 100, 30, 100], [1, 0, 1, 0]),
        # Inverted V-shape
        ([30, 50, 80, 50, 30], [1, 1, 0, 0, 0]),
    ],
)
def test_daily_temperatures(solution, method_name, temperatures, expected):
    method = getattr(solution, method_name)
    input_data = list(temperatures)
    result = method(input_data)
    assert result == expected
