import importlib
import pytest

leetcode_0238 = importlib.import_module("leetcode.0238")
Solution = leetcode_0238.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    ["productExceptSelf", "productExceptSelf_prefix_suffix_arrays"],
)
@pytest.mark.parametrize(
    "nums,expected",
    [
        ([1, 2, 3, 4], [24, 12, 8, 6]),
        ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),
        ([0, 0], [0, 0]),
        ([0, 4, 0], [0, 0, 0]),
        ([1, -1], [-1, 1]),
        ([2, 3, 4, 5], [60, 40, 30, 24]),
        ([5, 2], [2, 5]),
        ([-1, -2, -3, -4], [-24, -12, -8, -6]),
        ([1, 1, 1, 1], [1, 1, 1, 1]),
        ([10, 0], [0, 10]),
    ],
)
def test_product_except_self_methods(solution, method_name, nums, expected):
    arr = list(nums)
    method = getattr(solution, method_name)
    assert method(arr) == expected
