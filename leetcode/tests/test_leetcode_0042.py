import importlib
from typing import List
import pytest

leetcode_0042 = importlib.import_module("leetcode.0042")
Solution = leetcode_0042.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize("method_name", ["trap", "trap_monotonic_stack", "trap_dp"])
@pytest.mark.parametrize(
    "height,expected",
    [
        # Standard LeetCode examples
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([4, 2, 0, 3, 2, 5], 9),
        # Empty and edge cases under 3 elements (cannot trap water)
        ([], 0),
        ([1], 0),
        ([1, 2], 0),
        ([3, 1], 0),
        # Flat and uniform heights
        ([0, 0, 0, 0], 0),
        ([3, 3, 3, 3], 0),
        # Monotonically increasing or decreasing (no trapped water)
        ([1, 2, 3, 4, 5], 0),
        ([5, 4, 3, 2, 1], 0),
        # Mountain / Pyramid (no basin)
        ([1, 2, 3, 2, 1], 0),
        ([1, 3, 5, 4, 2], 0),
        # Single basin / Simple V-shape and U-shape
        ([3, 0, 3], 3),
        ([2, 0, 2], 2),
        ([5, 1, 1, 5], 8),
        ([3, 0, 0, 0, 3], 9),
        # Multiple basins with varying wall heights
        ([3, 0, 2, 0, 4], 7),
        ([5, 2, 1, 2, 1, 5], 14),
        ([2, 1, 0, 2], 3),
        ([4, 2, 3], 1),
    ],
)
def test_trapping_rain_water(
    solution: Solution, method_name: str, height: List[int], expected: int
):
    method = getattr(solution, method_name)
    assert method(list(height)) == expected
