import importlib
import pytest

leetcode_0200 = importlib.import_module("leetcode.0200")
Solution = leetcode_0200.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name", ["numIslands", "numIslands_bfs", "numIslands_union_find"]
)
@pytest.mark.parametrize(
    "grid,expected",
    [
        # Standard Example 1 (Single large connected island)
        (
            [
                ["1", "1", "1", "1", "0"],
                ["1", "1", "0", "1", "0"],
                ["1", "1", "0", "0", "0"],
                ["0", "0", "0", "0", "0"],
            ],
            1,
        ),
        # Standard Example 2 (Three disconnected islands)
        (
            [
                ["1", "1", "0", "0", "0"],
                ["1", "1", "0", "0", "0"],
                ["0", "0", "1", "0", "0"],
                ["0", "0", "0", "1", "1"],
            ],
            3,
        ),
        # Empty grid
        ([], 0),
        ([[]], 0),
        # 1x1 grids
        ([["1"]], 1),
        ([["0"]], 0),
        # All water
        (
            [
                ["0", "0", "0"],
                ["0", "0", "0"],
                ["0", "0", "0"],
            ],
            0,
        ),
        # All land
        (
            [
                ["1", "1", "1"],
                ["1", "1", "1"],
                ["1", "1", "1"],
            ],
            1,
        ),
        # Checkerboard / Diagonal grid (no diagonal connections)
        (
            [
                ["1", "0", "1"],
                ["0", "1", "0"],
                ["1", "0", "1"],
            ],
            5,
        ),
        # Single row grid
        ([["1", "0", "1", "1", "0", "1"]], 3),
        # Single col grid
        (
            [
                ["1"],
                ["0"],
                ["1"],
                ["1"],
                ["0"],
            ],
            2,
        ),
        # Donut / Ring island with a water lake inside
        (
            [
                ["1", "1", "1", "1"],
                ["1", "0", "0", "1"],
                ["1", "0", "0", "1"],
                ["1", "1", "1", "1"],
            ],
            1,
        ),
        # Snake / Spiral island
        (
            [
                ["1", "1", "1", "1", "1"],
                ["0", "0", "0", "0", "1"],
                ["1", "1", "1", "0", "1"],
                ["1", "0", "0", "0", "1"],
                ["1", "1", "1", "1", "1"],
            ],
            1,
        ),
    ],
)
def test_num_islands(solution, method_name, grid, expected):
    method = getattr(solution, method_name)
    # Pass deep copy because algorithms may sink/mutate grid cells
    grid_copy = [list(row) for row in grid]
    result = method(grid_copy)
    assert result == expected
