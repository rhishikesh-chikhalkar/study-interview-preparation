"""
3. Longest Substring Without Repeating Characters
Medium
Topics
premium lock icon
Companies
Hint
Given a string s, find the length of the longest substring without duplicate characters.

Example 1:

Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3. Note that "bca" and "cab" are also correct answers.
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

0 <= s.length <= 5 * 104
s consists of English letters, digits, symbols and spaces.
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> tuple[int, str]:
        char_index = {}
        left = 0
        max_len = 0
        best_left = 0

        for right, char in enumerate(s):
            if char in char_index and char_index[char] >= left:
                left = char_index[char] + 1
            char_index[char] = right

            # If we find a new maximum length, record the starting position
            if right - left + 1 > max_len:
                max_len = right - left + 1
                best_left = left

        # Return both the length and the sliced substring
        return max_len, s[best_left : best_left + max_len]


if __name__ == "__main__":
    solution = Solution()

    # Example 1
    s1 = "abcabcbb"
    length1, sub1 = solution.lengthOfLongestSubstring(s1)
    print(f"Input: s = {s1!r}")
    print(f"Output Length: {length1}, Substring: {sub1!r}")
    print("Expected: 3\n")

    # Example 2
    s2 = "bbbbb"
    length2, sub2 = solution.lengthOfLongestSubstring(s2)
    print(f"Input: s = {s2!r}")
    print(f"Output Length: {length2}, Substring: {sub2!r}")
    print("Expected: 1\n")

    # Example 3
    s3 = "pwwkew"
    length3, sub3 = solution.lengthOfLongestSubstring(s3)
    print(f"Input: s = {s3!r}")
    print(f"Output Length: {length3}, Substring: {sub3!r}")
    print("Expected: 3")
