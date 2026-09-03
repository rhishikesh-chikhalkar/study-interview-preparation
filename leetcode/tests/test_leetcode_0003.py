import importlib
import pytest

leetcode_0003 = importlib.import_module("leetcode.0003")
Solution = leetcode_0003.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    [
        "lengthOfLongestSubstring",
        "lengthOfLongestSubstring_set",
    ],
)
@pytest.mark.parametrize(
    "s,expected",
    [
        ("abcabcbb", 3),
        ("bbbbb", 1),
        ("pwwkew", 3),
        ("", 0),
        (" ", 1),
        ("au", 2),
        ("abba", 2),
        ("tmmzuxt", 5),
        ("abcdefghijklmnopqrstuvwxyz", 26),
        ("a b!a c", 5),
        ("12345!@#$%^&*()_+-=[]{}|;':,.<>?/`~", 35),
    ],
)
def test_length_of_longest_substring(solution, method_name, s, expected):
    method = getattr(solution, method_name)
    assert method(s) == expected


def test_length_of_longest_substring_with_slice(solution):
    max_len, substr = solution.lengthOfLongestSubstring_with_slice("abcabcbb")
    assert max_len == 3
    assert len(substr) == 3
    assert len(set(substr)) == 3
    assert substr in "abcabcbb"

    empty_len, empty_substr = solution.lengthOfLongestSubstring_with_slice("")
    assert empty_len == 0
    assert empty_substr == ""

    abba_len, abba_substr = solution.lengthOfLongestSubstring_with_slice("abba")
    assert abba_len == 2
    assert len(set(abba_substr)) == 2
    assert abba_substr in "abba"
