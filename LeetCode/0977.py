"""
977. Squares of a Sorted Array
Easy

Given an integer array nums sorted in non-decreasing order, return an array of the
squares of each number sorted in non-decreasing order.

Example 1:
Input: nums = [-4,-1,0,3,10]
Output: [0,1,9,16,100]
Explanation: After squaring, the array becomes [16,1,0,9,100].
After sorting, it becomes [0,1,9,16,100].

Example 2:
Input: nums = [-7,-3,2,3,11]
Output: [4,9,9,49,121]

Constraints:
1 <= nums.length <= 10^4
-10^4 <= nums[i] <= 10^4
nums is sorted in non-decreasing order.

Follow up: Squaring each element and sorting the new array is very trivial,
could you find an O(n) solution using a different approach?
"""

from typing import List


class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        """Computes sorted squares using two pointers moving inward from boundaries.

        Time Complexity: O(N) where N is len(nums).
        Space Complexity: O(N) for output array.
        """

        n = len(nums)
        result = [0] * n
        left = 0
        right = n - 1
        write_idx = n - 1

        while left <= right:
            left_sq = nums[left] * nums[left]
            right_sq = nums[right] * nums[right]

            if left_sq > right_sq:
                result[write_idx] = left_sq
                left += 1
            else:
                result[write_idx] = right_sq
                right -= 1
            write_idx -= 1

        return result

    def sortedSquares_trivial(self, nums: List[int]) -> List[int]:
        """Computes sorted squares by squaring each element and sorting.

        Time Complexity: O(N log N) where N is len(nums).
        Space Complexity: O(N) for sorted result.
        """

        return sorted(x * x for x in nums)
