import importlib
from typing import List
import pytest

leetcode_0011 = importlib.import_module("leetcode.0011")
Solution = leetcode_0011.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize("method_name", ["maxArea", "maxArea_optimized_skip"])
@pytest.mark.parametrize(
    "height,expected",
    [
        # Standard examples
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 1], 1),
        # Minimum size with varying heights
        ([1, 2], 1),
        ([2, 1], 1),
        ([5, 5], 5),
        # Symmetric walls
        ([4, 3, 2, 1, 4], 16),
        ([1, 2, 1], 2),
        # Strictly increasing
        ([1, 2, 3, 4, 5, 6, 7, 8], 16),
        # Strictly decreasing
        ([8, 7, 6, 5, 4, 3, 2, 1], 16),
        # Flat heights
        ([3, 3, 3, 3, 3], 12),
        # Tall walls inside, short walls outside
        ([1, 100, 100, 1], 100),
        # Mountain / Pyramid
        ([1, 3, 5, 7, 9, 8, 6, 4, 2], 20),
        # Valley / U-shape
        ([9, 2, 2, 2, 9], 36),
        # Heights with 0
        ([0, 2], 0),
        ([0, 0], 0),
        ([0, 14, 0, 14, 0], 28),
    ],
)
def test_max_area(
    solution: Solution, method_name: str, height: List[int], expected: int
):
    method = getattr(solution, method_name)
    assert method(list(height)) == expected
