"""
1480. Running Sum of 1d Array
Easy

Given an array nums. We define a running sum of an array as runningSum[i] = sum(nums[0]…nums[i]).

Return the running sum of nums.

Example 1:
Input: nums = [1,2,3,4]
Output: [1,3,6,10]
Explanation: Running sum is obtained as follows: [1, 1+2, 1+2+3, 1+2+3+4].

Example 2:
Input: nums = [1,1,1,1,1]
Output: [1,2,3,4,5]
Explanation: Running sum is obtained as follows: [1, 1+1, 1+1+1, 1+1+1+1, 1+1+1+1+1].

Example 3:
Input: nums = [3,1,2,10,1]
Output: [3,4,6,16,17]

Constraints:
1 <= nums.length <= 1000
-10^6 <= nums[i] <= 10^6
"""

from itertools import accumulate
from typing import List


class Solution:
    def runningSum(self, nums: List[int]) -> List[int]:
        """Computes running sum without mutating the input array.

        Time Complexity: O(N) where N is len(nums).
        Space Complexity: O(N) for output array.
        """

        n = len(nums)
        result = [0] * n
        current_sum = 0

        for i in range(n):
            current_sum += nums[i]
            result[i] = current_sum

        return result

    def runningSum_inplace(self, nums: List[int]) -> List[int]:
        """Computes running sum in-place by mutating the input array.

        Time Complexity: O(N) where N is len(nums).
        Space Complexity: O(1) auxiliary space.
        """

        for i in range(1, len(nums)):
            nums[i] += nums[i - 1]

        return nums

    def runningSum_accumulate(self, nums: List[int]) -> List[int]:
        """Computes running sum using itertools.accumulate stream iterator.

        Time Complexity: O(N) where N is len(nums).
        Space Complexity: O(N) for output list.
        """

        return list(accumulate(nums))
