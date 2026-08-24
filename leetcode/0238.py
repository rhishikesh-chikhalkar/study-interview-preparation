"""
238. Product of Array Except Self
Medium

Given an integer array nums, return an array answer such that answer[i] is equal to the product
of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operator.

Example 1:
Input: nums = [1,2,3,4]
Output: [24,12,8,6]

Example 2:
Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]

Constraints:
2 <= nums.length <= 10^5
-30 <= nums[i] <= 30
The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

Follow up: Can you solve the problem in O(1) extra space complexity? (The output array does not
count as extra space for space complexity analysis.)
"""

from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """
        Computes product of array except self using prefix and suffix passes in O(1) auxiliary space.

        Approach:
        1. Initialize an output array where each element initially stores the product of all
           numbers to its left (prefix product).
        2. Set output[0] = 1, and for each i from 1 to n - 1:
           output[i] = output[i - 1] * nums[i - 1]
        3. Maintain a running suffix product starting at 1.
        4. Traverse backward from n - 1 to 0:
           output[i] *= suffix_product
           suffix_product *= nums[i]
        5. Return output array.

        Time Complexity: O(N) where N is the length of nums (two passes).
        Space Complexity: O(1) auxiliary space (output array is excluded per problem specification).
        """

        n = len(nums)
        answer = [1] * n

        # Step 1: Prefix products stored in answer
        for i in range(1, n):
            answer[i] = answer[i - 1] * nums[i - 1]

        # Step 2: Multiply by suffix products in reverse
        suffix = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= suffix
            suffix *= nums[i]

        return answer

    def productExceptSelf_prefix_suffix_arrays(self, nums: List[int]) -> List[int]:
        """
        Computes product of array except self using explicit prefix and suffix arrays.

        Approach:
        1. Create prefix array of size N where prefix[i] = product(nums[0]...nums[i-1]).
        2. Create suffix array of size N where suffix[i] = product(nums[i+1]...nums[n-1]).
        3. For each index i: answer[i] = prefix[i] * suffix[i].

        Time Complexity: O(N) where N is len(nums).
        Space Complexity: O(N) auxiliary space for prefix and suffix arrays.
        """

        n = len(nums)
        prefix = [1] * n
        suffix = [1] * n
        answer = [1] * n

        for i in range(1, n):
            prefix[i] = prefix[i - 1] * nums[i - 1]

        for i in range(n - 2, -1, -1):
            suffix[i] = suffix[i + 1] * nums[i + 1]

        for i in range(n):
            answer[i] = prefix[i] * suffix[i]

        return answer
