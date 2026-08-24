import importlib
import pytest

leetcode_0724 = importlib.import_module("leetcode.0724")
Solution = leetcode_0724.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    ["pivotIndex", "pivotIndex_prefix_array"],
)
@pytest.mark.parametrize(
    "nums,expected",
    [
        ([1, 7, 3, 6, 5, 6], 3),
        ([1, 2, 3], -1),
        ([2, 1, -1], 0),
        ([0, 0, 0, 0], 0),
        ([-1, -1, 0, 1, 1, 0], 5),
        ([5], 0),
        ([-1, -1, -1, -1, -1, 0], 2),
        ([-1, -1, 0, -1, -1, -1], 3),
        ([1, -1, 2], 2),
        ([1, 2, 1], 1),
    ],
)
def test_find_pivot_index_methods(solution, method_name, nums, expected):
    arr = list(nums)
    method = getattr(solution, method_name)
    assert method(arr) == expected
