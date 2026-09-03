"""
3. Longest Substring Without Repeating Characters
Medium

Given a string s, find the length of the longest substring without duplicate characters.

Example 1:
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.

Example 2:
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.

Example 3:
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

Constraints:
0 <= s.length <= 5 * 10^4
s consists of English letters, digits, symbols and spaces.
"""

from typing import Dict, Set, Tuple


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Optimal Sliding Window with Hash Map (Direct Pointer Jump).

        Tracks the most recent index of each character. When a duplicate
        character is encountered, moves the left pointer directly past its
        previous index, provided that index is within the current window.

        Time Complexity: O(N) where N is the length of string s.
        Space Complexity: O(min(N, M)) where M is the character set size.
        """

        last_seen: Dict[str, int] = {}
        left = 0
        max_length = 0

        for right, char in enumerate(s):
            if char in last_seen and last_seen[char] >= left:
                left = last_seen[char] + 1
            last_seen[char] = right
            current_window_len = right - left + 1
            if current_window_len > max_length:
                max_length = current_window_len

        return max_length

    def lengthOfLongestSubstring_set(self, s: str) -> int:
        """
        Sliding Window with Hash Set (Incremental Contraction).

        Expands the right pointer and contracts the left pointer one by one
        until the duplicate character is removed from the set.

        Time Complexity: O(2N) = O(N) since each char is added and removed at most once.
        Space Complexity: O(min(N, M)) where M is the character set size.
        """

        char_set: Set[str] = set()
        left = 0
        max_length = 0

        for right in range(len(s)):
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1
            char_set.add(s[right])
            current_window_len = right - left + 1
            if current_window_len > max_length:
                max_length = current_window_len

        return max_length

    def lengthOfLongestSubstring_with_slice(self, s: str) -> Tuple[int, str]:
        """
        Returns both the maximum length and the actual longest substring.

        Time Complexity: O(N) where N is the length of string s.
        Space Complexity: O(min(N, M)) where M is the character set size.
        """

        last_seen: Dict[str, int] = {}
        left = 0
        max_length = 0
        best_start = 0

        for right, char in enumerate(s):
            if char in last_seen and last_seen[char] >= left:
                left = last_seen[char] + 1
            last_seen[char] = right
            current_window_len = right - left + 1
            if current_window_len > max_length:
                max_length = current_window_len
                best_start = left

        return max_length, s[best_start : best_start + max_length]


if __name__ == "__main__":
    solution = Solution()

    test_cases = [
        "abcabcbb",
        "bbbbb",
        "pwwkew",
        "",
        " ",
        "abba",
    ]

    for index, test_str in enumerate(test_cases, 1):
        optimal_len = solution.lengthOfLongestSubstring(test_str)
        set_len = solution.lengthOfLongestSubstring_set(test_str)
        slice_len, substr = solution.lengthOfLongestSubstring_with_slice(test_str)
        print(f"--- Case {index}: s = {test_str!r} ---")
        print(f"Optimal Hash Map Length: {optimal_len}")
        print(f"Hash Set Window Length:  {set_len}")
        print(f"Substr Slice Result:     {slice_len} -> {substr!r}")
        print()
