"""
49. Group Anagrams
Medium
Given an array of strings strs, group the anagrams together. You can return the answer in any order.

Example 1:
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Example 2:
Input: strs = [""]
Output: [[""]]

Example 3:
Input: strs = ["a"]
Output: [["a"]]

Constraints:
1 <= strs.length <= 104
0 <= strs[i].length <= 100
strs[i] consists of lowercase English letters.
"""

from collections import defaultdict
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """
        Groups anagrams together using character counts (optimal).

        Time Complexity: O(N * L) where N is the number of strings and L is the max length of a string.
        Space Complexity: O(N * L) to store the grouped anagrams in the hash map.
        """
        anagrams = defaultdict(list)
        for s in strs:
            # Since the string consists of lowercase English letters, we can use a tuple
            # of size 26 representing the character count as the hash map key.
            count = [0] * 26
            for char in s:
                count[ord(char) - 97] += 1  # 97 is ord('a')
            anagrams[tuple(count)].append(s)
        return list(anagrams.values())

    def groupAnagrams_sorting(self, strs: List[str]) -> List[List[str]]:
        """
        Groups anagrams together by sorting each string.

        Time Complexity: O(N * L * log(L)) where N is the number of strings and L is the max length of a string.
        Space Complexity: O(N * L) to store the grouped anagrams in the hash map.
        """
        anagrams = defaultdict(list)
        for s in strs:
            # Sort the characters of the string and use the sorted string as the key.
            sorted_s = "".join(sorted(s))
            anagrams[sorted_s].append(s)
        return list(anagrams.values())

    def groupAnagrams_dict(self, strs: List[str]) -> List[List[str]]:
        """
        Groups anagrams together using standard dict (without defaultdict).

        Time Complexity: O(N * L) where N is the number of strings and L is the max length of a string.
        Space Complexity: O(N * L) to store the grouped anagrams in the hash map.
        """
        anagrams = {}
        for s in strs:
            # Since the string consists of lowercase English letters, we can use a tuple
            # of size 26 representing the character count as the hash map key.
            count = [0] * 26
            for char in s:
                count[ord(char) - 97] += 1  # 97 is ord('a')
            key = tuple(count)
            if key not in anagrams:
                anagrams[key] = []
            anagrams[key].append(s)
        return list(anagrams.values())


if __name__ == "__main__":
    solution = Solution()

    # Test inputs
    tests = [["eat", "tea", "tan", "ate", "nat", "bat"], [""], ["a"]]

    for i, strs in enumerate(tests, 1):
        print(f"--- Example {i} ---")
        print(f"Input: strs = {strs}")
        print(f"Count method output:       {solution.groupAnagrams(strs)}")
        print(f"Sorting method output:     {solution.groupAnagrams_sorting(strs)}")
        print(f"Standard dict output:      {solution.groupAnagrams_dict(strs)}")
        print()
