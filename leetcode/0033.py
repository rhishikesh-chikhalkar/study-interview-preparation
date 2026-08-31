"""
33. Search in Rotated Sorted Array
Medium

There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly rotated at an unknown
pivot index k (1 <= k < nums.length) such that the resulting array is
[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed).
For example, [0,1,2,4,5,6,7] might be rotated at pivot index 3 and become
[4,5,6,7,0,1,2].

Given the array nums after the possible rotation and an integer target, return
the index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4

Example 2:
Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1

Example 3:
Input: nums = [1], target = 0
Output: -1

Constraints:
1 <= nums.length <= 5000
-10^4 <= nums[i] <= 10^4
All values of nums are unique.
nums is an ascending array that is possibly rotated.
-10^4 <= target <= 10^4
"""

from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """
        Performs one-pass modified binary search on a rotated sorted array.

        Approach:
        1. Maintain standard binary search pointers left and right.
        2. At any mid point, at least one half of the array (left..mid or mid..right)
           is guaranteed to be strictly sorted.
        3. Determine which half is sorted by comparing nums[left] and nums[mid]:
           - If nums[left] <= nums[mid], the left half is sorted.
             Check if target lies within [nums[left], nums[mid]]:
             if yes, search left (right = mid - 1); otherwise search right (left = mid + 1).
           - Otherwise, the right half must be sorted (nums[mid] < nums[right]).
             Check if target lies within (nums[mid], nums[right]]:
             if yes, search right (left = mid + 1); otherwise search left (right = mid - 1).
        4. If pointers cross without finding target, return -1.

        Time Complexity: O(log N) where N is len(nums).
        Space Complexity: O(1) auxiliary space.
        """

        left, right = 0, len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid

            # Check if left half is sorted
            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            # Otherwise, right half is sorted
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1

    def search_two_pass(self, nums: List[int], target: int) -> int:
        """
        Performs two-pass binary search: first finds the pivot index (minimum element),
        then executes a standard binary search on the appropriate sorted subarray.

        Approach:
        1. Find pivot (index of minimum element) using binary search in O(log N):
           - If nums[mid] > nums[right], pivot is in right half (left = mid + 1).
           - Otherwise, pivot is in left half or at mid (right = mid).
        2. Compare target against array bounds to decide which sorted subarray to search:
           - If target >= nums[pivot] and target <= nums[len(nums) - 1], search [pivot, n - 1].
           - Otherwise, search [0, pivot - 1].
        3. Execute standard binary search on chosen bounds.

        Time Complexity: O(log N) where N is len(nums).
        Space Complexity: O(1) auxiliary space.
        """

        n = len(nums)
        left, right = 0, n - 1

        # Phase 1: Locate pivot index (smallest element)
        while left < right:
            mid = left + (right - left) // 2
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid

        pivot = left

        # Phase 2: Select the correct sorted half
        if nums[pivot] <= target <= nums[n - 1]:
            left, right = pivot, n - 1
        else:
            left, right = 0, pivot - 1

        # Phase 3: Standard binary search
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1
