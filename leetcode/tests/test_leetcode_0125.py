import importlib

import pytest

leetcode_0125 = importlib.import_module("leetcode.0125")
Solution = leetcode_0125.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    ["is_palindrome", "is_palindrome_filtered"],
)
@pytest.mark.parametrize(
    "s,expected",
    [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        (" ", True),
        ("", True),
        ("a", True),
        ("ab", False),
        ("aba", True),
        ("0P", False),
        (".,", True),
        ("Aa", True),
        ("a.", True),
        ("ab_ba", True),
        ("Was it a car or a cat I saw?", True),
    ],
)
def test_is_palindrome(solution, method_name, s, expected):
    method = getattr(solution, method_name)
    assert method(s) == expected
