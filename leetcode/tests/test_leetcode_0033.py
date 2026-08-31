import importlib
import pytest

leetcode_0033 = importlib.import_module("leetcode.0033")
Solution = leetcode_0033.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize("method_name", ["search", "search_two_pass"])
@pytest.mark.parametrize(
    "nums,target,expected",
    [
        # Standard rotated array examples
        ([4, 5, 6, 7, 0, 1, 2], 0, 4),
        ([4, 5, 6, 7, 0, 1, 2], 3, -1),
        ([4, 5, 6, 7, 0, 1, 2], 4, 0),
        ([4, 5, 6, 7, 0, 1, 2], 2, 6),
        ([4, 5, 6, 7, 0, 1, 2], 7, 3),
        # Single element arrays
        ([1], 0, -1),
        ([1], 1, 0),
        # Two element arrays
        ([1, 3], 0, -1),
        ([1, 3], 1, 0),
        ([1, 3], 3, 1),
        ([3, 1], 1, 1),
        ([3, 1], 3, 0),
        ([3, 1], 0, -1),
        ([3, 1], 4, -1),
        # Three element arrays with different rotations
        ([1, 2, 3], 2, 1),
        ([3, 1, 2], 1, 1),
        ([2, 3, 1], 3, 1),
        ([3, 1, 2], 4, -1),
        # Unrotated sorted arrays
        ([1, 2, 3, 4, 5, 6], 1, 0),
        ([1, 2, 3, 4, 5, 6], 4, 3),
        ([1, 2, 3, 4, 5, 6], 6, 5),
        ([1, 2, 3, 4, 5, 6], 10, -1),
        # Rotated by 1 position (pivot at index 1)
        ([6, 1, 2, 3, 4, 5], 6, 0),
        ([6, 1, 2, 3, 4, 5], 1, 1),
        ([6, 1, 2, 3, 4, 5], 5, 5),
        # Pivot at the very end
        ([2, 3, 4, 5, 6, 1], 1, 5),
        ([2, 3, 4, 5, 6, 1], 2, 0),
        ([2, 3, 4, 5, 6, 1], 6, 4),
        # Negative numbers in rotated array
        ([-5, -3, -1, -10, -8, -6], -10, 3),
        ([-5, -3, -1, -10, -8, -6], -1, 2),
        ([-5, -3, -1, -10, -8, -6], 0, -1),
        # Array containing negative and positive numbers
        ([5, 6, -3, -2, -1, 0, 1, 2, 3, 4], -3, 2),
        ([5, 6, -3, -2, -1, 0, 1, 2, 3, 4], 5, 0),
        ([5, 6, -3, -2, -1, 0, 1, 2, 3, 4], 4, 9),
        ([5, 6, -3, -2, -1, 0, 1, 2, 3, 4], 99, -1),
    ],
)
def test_search_rotated_sorted_array(solution, method_name, nums, target, expected):
    method = getattr(solution, method_name)
    assert method(nums, target) == expected
