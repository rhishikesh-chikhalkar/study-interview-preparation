import importlib
import pytest

leetcode_0020 = importlib.import_module("leetcode.0020")
Solution = leetcode_0020.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    ["is_valid", "is_valid_complement_push"],
)
@pytest.mark.parametrize(
    "s,expected",
    [
        # Odd length -- early termination
        ("(", False),
        # Single valid pair
        ("()", True),
        # Nested valid (full nesting depth)
        ("([{}])", True),
        # Interleaved invalid (type mismatch)
        ("([)]", False),
        # Only openers (excess openers)
        ("(((", False),
        # Only closers (excess closers)
        (")))", False),
        # Sequential valid pairs
        ("(){}[]", True),
        # Deep nesting
        ("{[()]}", True),
        # Empty-equivalent single closer
        (")", False),
        # Mixed valid nesting
        ("{[]}", True),
        # Closer then opener
        (")(", False),
        # Long repeated valid
        ("()()()()", True),
        # Long nested valid
        ("(((())))", True),
        # Wrong closer at end
        ("(){", False),
    ],
)
def test_is_valid(solution, method_name, s, expected):
    method = getattr(solution, method_name)
    assert method(s) == expected
