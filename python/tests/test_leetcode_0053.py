import importlib
import pytest

leetcode_0053 = importlib.import_module("leetcode.0053")
Solution = leetcode_0053.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    ["maxSubArray", "maxSubArray_divide_and_conquer", "maxSubArray_dp"],
)
@pytest.mark.parametrize(
    "nums,expected",
    [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([1], 1),
        ([5, 4, -1, 7, 8], 23),
        ([-1], -1),
        ([-2, -1], -1),
        ([-5, -2, -3, -4], -2),
        ([0, 0, 0, 0], 0),
        ([1, 2, 3, 4, 5], 15),
        ([-2, 1], 1),
        ([100], 100),
    ],
)
def test_max_sub_array_methods(solution, method_name, nums, expected):
    method = getattr(solution, method_name)
    assert method(nums) == expected


def test_max_sub_array_with_subarray(solution):
    max_sum, subarray = solution.maxSubArray_with_subarray(
        [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    )
    assert max_sum == 6
    assert subarray == [4, -1, 2, 1]

    max_sum, subarray = solution.maxSubArray_with_subarray([-1])
    assert max_sum == -1
    assert subarray == [-1]
