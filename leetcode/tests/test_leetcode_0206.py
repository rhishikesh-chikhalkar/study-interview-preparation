import importlib
import pytest

leetcode_0206 = importlib.import_module("leetcode.0206")
Solution = leetcode_0206.Solution
create_linked_list = leetcode_0206.create_linked_list
linked_list_to_list = leetcode_0206.linked_list_to_list


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    ["reverse_list", "reverse_list_recursive"],
)
@pytest.mark.parametrize(
    "arr,expected",
    [
        # Standard cases
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
        ([1, 2], [2, 1]),
        # Base/Edge cases
        ([], []),
        ([42], [42]),
        # Duplicates
        ([1, 1, 1], [1, 1, 1]),
        ([1, 2, 2, 1], [1, 2, 2, 1]),
        ([1, 2, 3, 2, 1], [1, 2, 3, 2, 1]),
        # Negatives and zeroes
        ([-10, -5, 0, 5, 10], [10, 5, 0, -5, -10]),
        ([-1], [-1]),
        # Moderately sized list
        (list(range(100)), list(range(99, -1, -1))),
    ],
)
def test_reverse_list(solution, method_name, arr, expected):
    head = create_linked_list(arr)
    method = getattr(solution, method_name)
    reversed_head = method(head)
    assert linked_list_to_list(reversed_head) == expected
