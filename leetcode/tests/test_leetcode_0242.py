import importlib
import pytest

leetcode_0242 = importlib.import_module("leetcode.0242")
Solution = leetcode_0242.Solution


@pytest.fixture
def solution():
    return Solution()


@pytest.mark.parametrize(
    "method_name",
    ["isAnagram", "isAnagram_counter", "isAnagram_sorting"],
)
@pytest.mark.parametrize(
    "s,t,expected",
    [
        ("anagram", "nagaram", True),
        ("rat", "car", False),
        ("a", "a", True),
        ("a", "b", False),
        ("ab", "a", False),
        ("a", "ab", False),
        ("listen", "silent", True),
        ("triangle", "integral", True),
        ("apple", "papel", True),
        ("aabbcc", "abcabc", True),
        ("aabbcc", "abbbcc", False),
        ("a" * 1000 + "b" * 1000, "b" * 1000 + "a" * 1000, True),
    ],
)
def test_is_anagram_methods(solution, method_name, s, t, expected):
    method = getattr(solution, method_name)
    assert method(s, t) == expected
