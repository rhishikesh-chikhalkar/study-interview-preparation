"""
5. Longest Palindromic Substring
Medium

Given a string s, return the longest palindromic substring in s.

Example 1:
Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.

Example 2:
Input: s = "cbbd"
Output: "bb"

Constraints:
1 <= s.length <= 1000
s consist of only digits and English letters.
"""


class Solution:
    def longestPalindrome(self, s: str) -> str:
        """
        Finds the longest palindromic substring using Expand Around Center.

        Approach:
        1. A palindrome mirrors around its center. A string of length N has 2N - 1 possible
           centers (N single-character centers for odd-length palindromes and N - 1
           two-character centers between adjacent characters for even-length palindromes).
        2. For each center index `i`:
           - Expand outward for odd-length palindrome: `expand(i, i)`.
           - Expand outward for even-length palindrome: `expand(i, i + 1)`.
        3. Track the start and maximum length of the longest palindrome discovered.
        4. Return `s[start:start + max_len]`.

        Time Complexity: O(N^2) where N is len(s). Expanding from each center takes O(N).
        Space Complexity: O(1) auxiliary space.
        """

        n = len(s)
        if n <= 1:
            return s

        start = 0
        max_len = 1

        def expand_from_center(left: int, right: int) -> int:
            while left >= 0 and right < n and s[left] == s[right]:
                left -= 1
                right += 1
            return right - left - 1

        for i in range(n):
            len_odd = expand_from_center(i, i)
            len_even = expand_from_center(i, i + 1)
            current_max = max(len_odd, len_even)

            if current_max > max_len:
                max_len = current_max
                start = i - (current_max - 1) // 2

        return s[start : start + max_len]

    def longestPalindrome_dp(self, s: str) -> str:
        """
        Finds longest palindromic substring using 2D Dynamic Programming table.

        Approach:
        1. Define `dp[i][j]` as True if substring `s[i..j]` is a palindrome, False otherwise.
        2. Base cases:
           - Every single character substring is a palindrome: `dp[i][i] = True`.
           - Two-character substring `s[i..i+1]` is a palindrome if `s[i] == s[i + 1]`.
        3. State Transition:
           - For length `L >= 3`: `dp[i][j] = (s[i] == s[j]) and dp[i + 1][j - 1]`.
        4. Maintain the longest substring indices `(start, max_len)`.

        Time Complexity: O(N^2) table filling.
        Space Complexity: O(N^2) auxiliary space for DP table.
        """

        n = len(s)
        if n <= 1:
            return s

        dp = [[False] * n for _ in range(n)]
        start = 0
        max_len = 1

        # All single characters are palindromes
        for i in range(n):
            dp[i][i] = True

        # Check substrings of length 2
        for i in range(n - 1):
            if s[i] == s[i + 1]:
                dp[i][i + 1] = True
                start = i
                max_len = 2

        # Check substrings of length 3 to n
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and dp[i + 1][j - 1]:
                    dp[i][j] = True
                    start = i
                    max_len = length

        return s[start : start + max_len]

    def longestPalindrome_manacher(self, s: str) -> str:
        """
        Finds the longest palindromic substring using Manacher's Algorithm in linear time.

        Approach:
        1. Transform string by inserting delimiters (e.g., `^#a#b#a#$`) to treat odd and even
           palindromes uniformly without edge checks.
        2. Maintain `C` (center of current furthest-reaching palindrome) and `R` (right boundary).
        3. Use symmetry around `C` (`i_mirror = 2 * C - i`) to initialize radius array `P[i]`.
        4. Expand beyond `R` only when necessary, updating `C` and `R`.
        5. Identify the index with the maximum radius in `P` and map back to original `s`.

        Time Complexity: O(N) linear time.
        Space Complexity: O(N) auxiliary space.
        """

        if len(s) <= 1:
            return s

        transformed = "^#" + "#".join(s) + "#$"
        m = len(transformed)
        p = [0] * m
        center = 0
        right = 0

        max_radius = 0
        max_center = 0

        for i in range(1, m - 1):
            i_mirror = 2 * center - i

            if right > i:
                p[i] = min(right - i, p[i_mirror])
            else:
                p[i] = 0

            while transformed[i + 1 + p[i]] == transformed[i - 1 - p[i]]:
                p[i] += 1

            if i + p[i] > right:
                center = i
                right = i + p[i]

            if p[i] > max_radius:
                max_radius = p[i]
                max_center = i

        start_index = (max_center - max_radius) // 2
        return s[start_index : start_index + max_radius]


def run_test(s: str) -> None:
    result = Solution().longestPalindrome(s)
    print(f"s='{s}' --> longest_palindrome='{result}'")


if __name__ == "__main__":
    run_test("babad")
    run_test("cbbd")
    run_test("a")
    run_test("ac")
    run_test("racecar")
