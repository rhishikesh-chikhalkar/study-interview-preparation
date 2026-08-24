"""
1358. Number of Substrings Containing All Three Characters
Medium
Topics
premium lock icon
Companies
Hint
Given a string s consisting only of characters a, b and c.

Return the number of substrings containing at least one occurrence of all these characters a, b and c.

Example 1:

Input: s = "abcabc"
Output: 10
Explanation: The substrings containing at least one occurrence of the characters a, b and c are "abc", "abca", "abcab", "abcabc", "bca", "bcab", "bcabc", "cab", "cabc" and "abc" (again).
Example 2:

Input: s = "aaacb"
Output: 3
Explanation: The substrings containing at least one occurrence of the characters a, b and c are "aaacb", "aacb" and "acb".
Example 3:

Input: s = "abc"
Output: 1

Constraints:

3 <= s.length <= 5 x 10^4
s only consists of a, b or c characters.
"""

from collections import namedtuple
from itertools import repeat
import numpy


class Solution:
    def numberOfSubstrings(self, s: str) -> int:
        # Initialize counts for 'a', 'b', and 'c'
        count = [0, 0, 0]  # indices 0 for 'a', 1 for 'b', 2 for 'c'

        # Initialize pointers and result
        left = 0
        result = 0

        # Iterate through the string with the right pointer
        for right in range(len(s)):
            # Increment the count for the current character
            count[ord(s[right]) - ord("a")] += 1

            # Check if the current window contains all three characters
            # While the condition is met, shrink the window from the left
            while count[0] > 0 and count[1] > 0 and count[2] > 0:
                # If the window [left, right] is valid, then any substring
                # starting at 'left' and ending at 'right' or later is also valid.
                # The number of such substrings is len(s) - right.
                result += len(s) - right

                # Shrink the window from the left
                count[ord(s[left]) - ord("a")] -= 1
                left += 1

        return result


s = Solution()

# Example 1
s1 = "abcabc"
print(f"Input: s = {s1!r}")
print(f"Output: {s.numberOfSubstrings(s1)}")
print("Expected: 10\n")

# Example 2
s2 = "aaacb"
print(f"Input: s = {s2!r}")
print(f"Output: {s.numberOfSubstrings(s2)}")
print("Expected: 3\n")

# Example 3
s3 = "abc"
print(f"Input: s = {s3!r}")
print(f"Output: {s.numberOfSubstrings(s3)}")
print("Expected: 1")

# Submitted by Samy Vilar <samy_vilar> on 06/20/2026

# For the sake of simplicity assume 1-indexing, for
# each distinct symbol keep track of the last the
# occurrence, assuming we initialize all last
# occurrences to 0, it would suffice to take
# the minima among all other symbols last
# witnessed;

# In general O(n * log(|alpha|)) time w/ O(|alpha|)
# additional-space if we where to use a (ideally a priority)
# min heap to keep track of said minimas
# though given our contraints it would suffice
# to "manually" check;

# version 1.1 vectorized

ids = bytearray(256)
ids[98:100] = 1, 2


def numberOfSubstrings(
    s: str, ids=bytes(ids), indices=numpy.arange(1, 50_001, dtype=numpy.uint16)
) -> int:
    s = numpy.frombuffer(s.encode().translate(ids), dtype=numpy.uint8)
    places = numpy.zeros((3, s.size + 1), dtype=numpy.uint16)
    indices = indices[: s.size]
    places[s, indices] = indices
    return numpy.maximum.accumulate(places, axis=1, out=places).min(axis=0).sum().item()

    # total = last_a = last_b = last_c = 0
    # for at, ch in enumerate(s, 1):
    #     if ch == 'a':
    #         total += last_b if last_b <= last_c else last_c
    #         last_a = at
    #     elif ch == 'b':
    #         total += last_a if last_a <= last_c else last_c
    #         last_b = at
    #     else:
    #         total += last_a if last_a <= last_b else last_b
    #         last_c = at
    # return total


Solution = repeat(
    namedtuple("Solution", ("numberOfSubstrings",))(numberOfSubstrings)
).__next__
