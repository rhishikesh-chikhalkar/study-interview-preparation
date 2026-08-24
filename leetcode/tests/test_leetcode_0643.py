import importlib
import pytest

leetcode_0643 = importlib.import_module("leetcode.0643")
Solution = leetcode_0643.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    ["findMaxAverage", "findMaxAverage_brute_force"],
)
@pytest.mark.parametrize(
    "nums,k,expected",
    [
        ([1, 12, -5, -6, 50, 3], 4, 12.75),
        ([5], 1, 5.0),
        ([-1], 1, -1.0),
        ([-5, -12, -6, -2], 2, -4.0),
        ([0, 4, 0, 3, 2], 1, 4.0),
        ([7, 4, 5, 8, 8, 3, 9, 8, 7, 6], 3, 8.0),
    ],
)
def test_find_max_average(solution, method_name, nums, k, expected):
    arr = list(nums)
    method = getattr(solution, method_name)
    assert pytest.approx(method(arr, k), rel=1e-5) == expected
