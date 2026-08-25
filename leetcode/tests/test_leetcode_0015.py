import importlib
from typing import List
import pytest

leetcode_0015 = importlib.import_module("leetcode.0015")
Solution = leetcode_0015.Solution


@pytest.fixture
def solution():
    return Solution()


def normalize_triplets(triplets: List[List[int]]) -> set[tuple[int, ...]]:
    return {tuple(sorted(t)) for t in triplets}


@pytest.mark.parametrize(
    "method_name",
    ["threeSum", "threeSum_hashset", "threeSum_no_sort"],
)
@pytest.mark.parametrize(
    "nums,expected",
    [
        ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
        ([0, 1, 1], []),
        ([0, 0, 0], [[0, 0, 0]]),
        ([0, 0, 0, 0], [[0, 0, 0]]),
        ([-2, 0, 1, 1, 2], [[-2, 0, 2], [-2, 1, 1]]),
        ([-1, -1, -1, 2, 2], [[-1, -1, 2]]),
        ([1, 2, -2, -1], []),
        ([], []),
        ([0], []),
        ([1, -1], []),
        (
            [-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6],
            [
                [-4, -2, 6],
                [-4, 0, 4],
                [-4, 1, 3],
                [-4, 2, 2],
                [-2, -2, 4],
                [-2, 0, 2],
            ],
        ),
    ],
)
def test_three_sum_methods(solution, method_name, nums, expected):
    method = getattr(solution, method_name)
    # Pass a copy since some methods sort in place
    result = method(nums.copy())
    assert normalize_triplets(result) == normalize_triplets(expected)
