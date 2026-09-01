import importlib
from typing import List
import pytest

leetcode_0001 = importlib.import_module("leetcode.0001")
Solution = leetcode_0001.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    [
        "twoSum",
        "two_sum",
        "twoSum_two_pass",
        "twoSum_two_pointers",
        "twoSum_brute_force",
    ],
)
@pytest.mark.parametrize(
    "nums,target,expected_pair",
    [
        ([2, 7, 11, 15], 9, (0, 1)),
        ([3, 2, 4], 6, (1, 2)),
        ([3, 3], 6, (0, 1)),
        ([-1, -2, -3, -4, -5], -8, (2, 4)),
        ([0, 4, 3, 0], 0, (0, 3)),
        ([-3, 4, 3, 90], 0, (0, 2)),
        ([10**9, -(10**9)], 0, (0, 1)),
        ([1, 5, 3, 7, 9, 2], 12, (2, 4)),  # 3 + 9 = 12 or 5 + 7 = 12
    ],
)
def test_two_sum_methods(
    solution: Solution,
    method_name: str,
    nums: List[int],
    target: int,
    expected_pair: tuple[int, int],
) -> None:
    method = getattr(solution, method_name)
    result = method(nums, target)

    assert len(result) == 2, f"{method_name} should return exactly 2 indices"
    i, j = result[0], result[1]
    assert i != j, f"{method_name} must return distinct indices"
    assert nums[i] + nums[j] == target, (
        f"{method_name} indices {i}, {j} (values {nums[i]}, {nums[j]}) do not sum to {target}"
    )


def test_two_sum_no_solution(solution: Solution) -> None:
    nums = [1, 2, 3]
    target = 10
    assert solution.twoSum(nums, target) == []
    assert solution.twoSum_two_pass(nums, target) == []
    assert solution.twoSum_two_pointers(nums, target) == []
    assert solution.twoSum_brute_force(nums, target) == []
