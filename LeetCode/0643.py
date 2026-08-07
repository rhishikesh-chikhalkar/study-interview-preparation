"""
643. Maximum Average Subarray I
Easy

You are given an integer array nums consisting of n elements, and an integer k.

Find a contiguous subarray whose length is equal to k that has the maximum
average value and return this value. Any answer with a calculation error less
than 10^-5 will be accepted.

Example 1:
Input: nums = [1,12,-5,-6,50,3], k = 4
Output: 12.75000
Explanation: Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75

Example 2:
Input: nums = [5], k = 1
Output: 5.00000

Constraints:
n == nums.length
1 <= k <= n <= 10^5
-10^4 <= nums[i] <= 10^4
"""

from typing import List


class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        """Finds maximum average of a contiguous subarray of length k.

        Time Complexity: O(N) where N is len(nums).
        Space Complexity: O(1) auxiliary space.
        """

        current_sum = sum(nums[:k])
        max_sum = current_sum

        for i in range(k, len(nums)):
            current_sum += nums[i] - nums[i - k]
            if current_sum > max_sum:
                max_sum = current_sum

        return max_sum / k

    def findMaxAverage_brute_force(self, nums: List[int], k: int) -> float:
        """Finds maximum average by recomputing sum of each subarray of size k.

        Time Complexity: O(N * k) where N is len(nums).
        Space Complexity: O(1) auxiliary space.
        """

        max_sum = float("-inf")
        for i in range(len(nums) - k + 1):
            sub_sum = sum(nums[i : i + k])
            if sub_sum > max_sum:
                max_sum = sub_sum

        return max_sum / k
