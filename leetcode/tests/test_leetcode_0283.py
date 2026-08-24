import importlib
import pytest

leetcode_0283 = importlib.import_module("leetcode.0283")
Solution = leetcode_0283.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    ["moveZeroes", "moveZeroes_optimal_swaps"],
)
@pytest.mark.parametrize(
    "nums,expected",
    [
        ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
        ([0], [0]),
        ([1, 2, 3, 4], [1, 2, 3, 4]),
        ([0, 0, 0], [0, 0, 0]),
        ([1, 0, 0, 0, 2], [1, 2, 0, 0, 0]),
        ([0, 0, 1], [1, 0, 0]),
        ([-1, 0, -3, 0, 5], [-1, -3, 5, 0, 0]),
        ([0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0]),
    ],
)
def test_move_zeroes(solution, method_name, nums, expected):
    arr = list(nums)
    method = getattr(solution, method_name)
    method(arr)
    assert arr == expected
