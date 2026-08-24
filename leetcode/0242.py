"""
242. Valid Anagram
Easy

Given two strings s and t, return true if t is an anagram of s, and false otherwise.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase,
typically using all the original letters exactly once.

Example 1:
Input: s = "anagram", t = "nagaram"
Output: true

Example 2:
Input: s = "rat", t = "car"
Output: false

Constraints:
1 <= s.length, t.length <= 5 * 10^4
s and t consist of lowercase English letters.

Follow up: What if the inputs contain Unicode characters? How would you adapt your solution?
"""

from collections import Counter


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        """
        Determines if t is an anagram of s using a fixed-size frequency array (optimal for ASCII).

        Approach:
        1. If lengths of s and t differ, they cannot be anagrams.
        2. Create a frequency array of size 26 (for lowercase English letters 'a'-'z').
        3. Iterate through both strings: increment count for characters in s, decrement for t.
        4. If all counts return to 0, t is an anagram of s.

        Time Complexity: O(N) where N is len(s).
        Space Complexity: O(1) auxiliary space (fixed array of 26 integers).
        """

        if len(s) != len(t):
            return False

        counts = [0] * 26
        for char_s, char_t in zip(s, t):
            counts[ord(char_s) - ord("a")] += 1
            counts[ord(char_t) - ord("a")] -= 1

        return all(count == 0 for count in counts)

    def isAnagram_counter(self, s: str, t: str) -> bool:
        """
        Determines if t is an anagram of s using collections.Counter (handles general Unicode).

        Approach:
        1. If lengths differ, return False.
        2. Count frequency of each character in s and t using hash map.
        3. Compare the two frequency maps for equality.

        Time Complexity: O(N) where N is len(s).
        Space Complexity: O(K) where K is the number of distinct characters (up to O(N)).
        """

        if len(s) != len(t):
            return False

        return Counter(s) == Counter(t)

    def isAnagram_sorting(self, s: str, t: str) -> bool:
        """
        Determines if t is an anagram of s by sorting characters.

        Approach:
        1. If lengths differ, return False.
        2. Sort characters of both strings and compare sorted sequences.

        Time Complexity: O(N log N) where N is len(s).
        Space Complexity: O(N) or O(1) depending on the sorting algorithm implementation.
        """

        if len(s) != len(t):
            return False

        return sorted(s) == sorted(t)
