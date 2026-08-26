import importlib
import pytest

leetcode_0056 = importlib.import_module("leetcode.0056")
Solution = leetcode_0056.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize("method_name", ["merge", "merge_in_place"])
@pytest.mark.parametrize(
    "intervals,expected",
    [
        # Standard examples
        ([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
        ([[1, 4], [4, 5]], [[1, 5]]),
        # Single element & empty list
        ([], []),
        ([[1, 5]], [[1, 5]]),
        # Completely nested / contained intervals
        ([[1, 4], [2, 3]], [[1, 4]]),
        ([[1, 10], [2, 3], [4, 5], [6, 7]], [[1, 10]]),
        # Reverse sorted input
        ([[15, 18], [8, 10], [2, 6], [1, 3]], [[1, 6], [8, 10], [15, 18]]),
        # Point intervals (start == end)
        ([[1, 1], [1, 2], [2, 2], [3, 4]], [[1, 2], [3, 4]]),
        # All overlapping into one single continuous interval
        ([[1, 4], [0, 4], [2, 3], [3, 5]], [[0, 5]]),
        # Non-overlapping already disjoint intervals
        ([[1, 2], [4, 5], [7, 8]], [[1, 2], [4, 5], [7, 8]]),
        # Duplicate intervals
        ([[1, 3], [1, 3], [1, 3]], [[1, 3]]),
        # Large coordinates
        ([[0, 10000], [1000, 2000], [9999, 10000]], [[0, 10000]]),
    ],
)
def test_merge_intervals(solution, method_name, intervals, expected):
    method = getattr(solution, method_name)
    # Pass deep copy to avoid modifying test input across fixtures
    input_data = [list(interval) for interval in intervals]
    result = method(input_data)
    assert result == expected
