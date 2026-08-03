import importlib
import pytest

leetcode_0217 = importlib.import_module("leetcode.0217")
Solution = leetcode_0217.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    ["containsDuplicate", "containsDuplicate_sorting", "containsDuplicate_length"],
)
@pytest.mark.parametrize(
    "nums,expected",
    [
        ([1, 2, 3, 1], True),
        ([1, 2, 3, 4], False),
        ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True),
        ([1], False),
        ([1, 1], True),
        ([1, 2], False),
        ([-(10**9), 10**9, -(10**9)], True),
        (list(range(1000)), False),
    ],
)
def test_contains_duplicate(solution, method_name, nums, expected):
    method = getattr(solution, method_name)
    assert method(nums) == expected
