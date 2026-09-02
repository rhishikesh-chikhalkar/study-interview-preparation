import importlib
import pytest

leetcode_0121 = importlib.import_module("leetcode.0121")
Solution = leetcode_0121.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    [
        "maxProfit",
        "maxProfit_two_pointers",
        "maxProfit_kadane",
    ],
)
@pytest.mark.parametrize(
    "prices,expected",
    [
        ([7, 1, 5, 3, 6, 4], 5),
        ([7, 6, 4, 3, 1], 0),
        ([1], 0),
        ([1, 2], 1),
        ([2, 1], 0),
        ([3, 3, 3, 3], 0),
        ([1, 2, 3, 4, 5], 4),
        ([2, 4, 1, 7], 6),
        ([0, 10000], 10000),
        ([10, 2, 2, 2], 0),
        ([3, 2, 6, 5, 0, 3], 4),
    ],
)
def test_max_profit_methods(solution, method_name, prices, expected):
    method = getattr(solution, method_name)
    assert method(prices) == expected
