import importlib
from typing import List
import pytest

leetcode_0005 = importlib.import_module("leetcode.0005")
Solution = leetcode_0005.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    ["longestPalindrome", "longestPalindrome_dp", "longestPalindrome_manacher"],
)
@pytest.mark.parametrize(
    "s,expected_valid",
    [
        # Standard examples (multiple valid palindromes of same max length)
        ("babad", ["bab", "aba"]),
        ("cbbd", ["bb"]),
        # Single character and two identical characters
        ("a", ["a"]),
        ("bb", ["bb"]),
        ("aa", ["aa"]),
        ("aaa", ["aaa"]),
        ("aaaa", ["aaaa"]),
        # Two distinct characters
        ("ac", ["a", "c"]),
        ("ab", ["a", "b"]),
        # Full string palindromes
        ("racecar", ["racecar"]),
        ("noon", ["noon"]),
        ("deified", ["deified"]),
        # Substring palindrome surrounded by non-palindromic prefixes/suffixes
        ("forgeeksskeegfor", ["geeksskeeg"]),
        ("abacdfgdcaba", ["aba"]),
        ("aacabdkacaa", ["aca"]),
        ("bananas", ["anana"]),
        ("abacaba", ["abacaba"]),
    ],
)
def test_longest_palindromic_substring(
    solution: Solution, method_name: str, s: str, expected_valid: List[str]
):
    method = getattr(solution, method_name)
    result = method(s)

    # Verify that the returned result is one of the valid longest palindromes
    assert result in expected_valid
    # Verify the palindrome property directly
    assert result == result[::-1]
    # Verify maximum length
    assert len(result) == len(expected_valid[0])
