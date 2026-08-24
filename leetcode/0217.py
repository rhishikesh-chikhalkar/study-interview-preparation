"""
217. Contains Duplicate

Easy

Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.

Example 1:
Input: nums = [1,2,3,1]
Output: true
Explanation: The element 1 occurs at the indices 0 and 3.

Example 2:
Input: nums = [1,2,3,4]
Output: false
Explanation: All elements are distinct.

Example 3:
Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true

Constraints:
1 <= nums.length <= 10^5
-10^9 <= nums[i] <= 10^9
"""

from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        """
        Determines if any value appears at least twice using a hash set.

        Time Complexity: O(N) where N is the number of elements in nums.
        Space Complexity: O(N) to store elements in the hash set.
        """
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False

    def containsDuplicate_sorting(self, nums: List[int]) -> bool:
        """
        Determines if any value appears at least twice by sorting the array.

        Time Complexity: O(N log N) where N is the number of elements in nums.
        Space Complexity: O(N) or O(1) depending on sorting implementation (Timsort in Python requires O(N) space).
        """
        sorted_nums = sorted(nums)
        for i in range(len(sorted_nums) - 1):
            if sorted_nums[i] == sorted_nums[i + 1]:
                return True
        return False

    def containsDuplicate_length(self, nums: List[int]) -> bool:
        """
        Determines if any value appears at least twice by comparing set and array length.

        Time Complexity: O(N) where N is the number of elements in nums.
        Space Complexity: O(N) to store elements in the hash set.
        """
        return len(nums) != len(set(nums))


if __name__ == "__main__":
    solution = Solution()

    # Test cases
    tests = [
        ([1, 2, 3, 1], True),
        ([1, 2, 3, 4], False),
        ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True),
    ]

    for i, (nums, expected) in enumerate(tests, 1):
        print(f"--- Example {i} ---")
        print(f"Input: nums = {nums}")
        print(f"Expected: {expected}")
        res_set = solution.containsDuplicate(nums)
        res_sort = solution.containsDuplicate_sorting(nums)
        res_len = solution.containsDuplicate_length(nums)
        print(f"Hash set method output:  {res_set}")
        print(f"Sorting method output:   {res_sort}")
        print(f"Length method output:    {res_len}")
        assert res_set == expected, f"Failed set method for {nums}"
        assert res_sort == expected, f"Failed sorting method for {nums}"
        assert res_len == expected, f"Failed length method for {nums}"
        print("All checks passed!")
        print()
