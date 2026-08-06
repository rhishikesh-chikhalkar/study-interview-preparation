import importlib
import pytest

leetcode_1480 = importlib.import_module("leetcode.1480")
Solution = leetcode_1480.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    ["runningSum", "runningSum_inplace", "runningSum_accumulate"],
)
@pytest.mark.parametrize(
    "nums,expected",
    [
        ([1, 2, 3, 4], [1, 3, 6, 10]),
        ([1, 1, 1, 1, 1], [1, 2, 3, 4, 5]),
        ([3, 1, 2, 10, 1], [3, 4, 6, 16, 17]),
        ([5], [5]),
        ([-1, -2, -3, -4], [-1, -3, -6, -10]),
        ([3, -1, 0, -2, 4], [3, 2, 2, 0, 4]),
    ],
)
def test_running_sum(solution, method_name, nums, expected):
    arr = list(nums)
    method = getattr(solution, method_name)
    assert method(arr) == expected
