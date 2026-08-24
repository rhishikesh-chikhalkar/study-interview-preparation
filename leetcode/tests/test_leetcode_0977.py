import importlib
import pytest

leetcode_0977 = importlib.import_module("leetcode.0977")
Solution = leetcode_0977.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    ["sortedSquares", "sortedSquares_trivial"],
)
@pytest.mark.parametrize(
    "nums,expected",
    [
        ([-4, -1, 0, 3, 10], [0, 1, 9, 16, 100]),
        ([-7, -3, 2, 3, 11], [4, 9, 9, 49, 121]),
        ([-5, -4, -3, -2, -1], [1, 4, 9, 16, 25]),
        ([0, 1, 2, 3, 4], [0, 1, 4, 9, 16]),
        ([-3], [9]),
        ([0], [0]),
        ([-2, -2, 0, 2, 2], [0, 4, 4, 4, 4]),
    ],
)
def test_sorted_squares(solution, method_name, nums, expected):
    arr = list(nums)
    method = getattr(solution, method_name)
    assert method(arr) == expected
