import importlib
from typing import List
import pytest

leetcode_0141 = importlib.import_module("leetcode.0141")
Solution = leetcode_0141.Solution
create_linked_list_with_cycle = leetcode_0141.create_linked_list_with_cycle


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    ["hasCycle", "has_cycle", "hasCycle_hash_set"],
)
@pytest.mark.parametrize(
    "values,pos,expected",
    [
        # Standard LeetCode examples
        ([3, 2, 0, -4], 1, True),
        ([1, 2], 0, True),
        ([1], -1, False),
        # Empty list
        ([], -1, False),
        # Single node cycle (self-loop)
        ([42], 0, True),
        # Two nodes acyclic
        ([10, 20], -1, False),
        # Two nodes cycle to second node (self-loop on tail)
        ([10, 20], 1, True),
        # Multi-node acyclic
        ([1, 2, 3, 4, 5, 6], -1, False),
        # Multi-node cycle connecting to head (index 0)
        ([1, 2, 3, 4, 5, 6], 0, True),
        # Multi-node cycle connecting to middle (index 2)
        ([1, 2, 3, 4, 5, 6], 2, True),
        # Multi-node cycle connecting to tail (self loop at index 5)
        ([1, 2, 3, 4, 5, 6], 5, True),
        # Negative and zero values
        ([-5, 0, 5, -10], 2, True),
        ([-5, 0, 5, -10], -1, False),
        # Moderately large list acyclic
        (list(range(200)), -1, False),
        # Moderately large list with cycle
        (list(range(200)), 100, True),
    ],
)
def test_has_cycle_methods(
    solution: Solution,
    method_name: str,
    values: List[int],
    pos: int,
    expected: bool,
) -> None:
    head = create_linked_list_with_cycle(values, pos)
    method = getattr(solution, method_name)
    assert method(head) is expected
