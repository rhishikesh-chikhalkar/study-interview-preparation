"""
125. Valid Palindrome
Easy

A phrase is a palindrome if, after converting all uppercase letters into
lowercase letters and removing all non-alphanumeric characters, it reads the
same forward and backward. Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.

Example 1:

Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Example 2:

Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.

Example 3:

Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.

Constraints:

1 <= s.length <= 2 * 10^5
s consists only of printable ASCII characters.
"""


class Solution:
    def is_palindrome(self, s: str) -> bool:
        """Two-pointer approach with in-place skip of non-alphanumeric chars.

        Pointers:
          - left: starts at index 0, advances right.
          - right: starts at index len(s)-1, advances left.
          - Both skip non-alphanumeric characters and compare lowercase.

        Time Complexity: O(N) where N is the length of s.
        Space Complexity: O(1) auxiliary space (no filtered copy).
        """

        left = 0
        right = len(s) - 1

        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1

            if s[left].lower() != s[right].lower():
                return False

            left += 1
            right -= 1

        return True

    def is_palindrome_filtered(self, s: str) -> bool:
        """Filter-then-compare approach using a cleaned string.

        Builds a lowercase alphanumeric-only string, then checks
        palindrome via reverse comparison.

        Time Complexity: O(N) where N is the length of s.
        Space Complexity: O(N) for the filtered string.
        """

        filtered = "".join(ch.lower() for ch in s if ch.isalnum())
        return filtered == filtered[::-1]


if __name__ == "__main__":
    solution = Solution()

    tests: list[tuple[str, bool]] = [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        (" ", True),
        ("", True),
        ("a", True),
        ("ab", False),
        ("aba", True),
        ("0P", False),
        (".,", True),
    ]

    for i, (s, expected) in enumerate(tests, 1):
        print(f"--- Test Case {i} ---")
        print(f"Input: s = {s!r}")
        print(f"Expected: {expected}")

        r1 = solution.is_palindrome(s)
        print(f"Method 1 (Two-Pointer In-Place): {r1}")
        assert r1 == expected, f"Failed method 1 for {s!r}"

        r2 = solution.is_palindrome_filtered(s)
        print(f"Method 2 (Filter + Reverse):     {r2}")
        assert r2 == expected, f"Failed method 2 for {s!r}"
        print("All checks passed!\n")
