"""
724. Find Pivot Index
Easy

Given an array of integers nums, calculate the pivot index of this array.

The pivot index is the index where the sum of all the numbers strictly to the left of the
index is equal to the sum of all the numbers strictly to the index's right.

If the index is on the left edge of the array, then the left sum is 0 because there are no
elements to the left. This also applies to the right edge of the array.

Return the leftmost pivot index. If no such index exists, return -1.

Example 1:
Input: nums = [1,7,3,6,5,6]
Output: 3
Explanation:
The pivot index is 3.
Left sum = nums[0] + nums[1] + nums[2] = 1 + 7 + 3 = 11
Right sum = nums[4] + nums[5] = 5 + 6 = 11

Example 2:
Input: nums = [1,2,3]
Output: -1
Explanation:
There is no index that satisfies the conditions in the problem statement.

Example 3:
Input: nums = [2,1,-1]
Output: 0
Explanation:
The pivot index is 0.
Left sum = 0 (no elements to the left of index 0)
Right sum = nums[1] + nums[2] = 1 + -1 = 0

Constraints:
1 <= nums.length <= 10^4
-1000 <= nums[i] <= 1000
"""

from typing import List


class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        """
        Finds the leftmost pivot index using total sum tracking.

        Approach:
        1. Calculate the total sum of all elements in the array.
        2. Maintain a running left sum starting at 0.
        3. Iterate through nums with index i and value num:
           - Right sum is: total_sum - left_sum - num.
           - If left_sum == total_sum - left_sum - num (or 2 * left_sum + num == total_sum),
             then i is the pivot index.
           - Otherwise, add num to left_sum.
        4. If loop completes without finding pivot, return -1.

        Time Complexity: O(N) where N is the number of elements in nums.
        Space Complexity: O(1) auxiliary space.
        """

        total_sum = sum(nums)
        left_sum = 0

        for i, num in enumerate(nums):
            # right_sum = total_sum - left_sum - num
            if left_sum == total_sum - left_sum - num:
                return i
            left_sum += num

        return -1

    def pivotIndex_prefix_array(self, nums: List[int]) -> int:
        """
        Finds the leftmost pivot index using an explicit prefix sum array.

        Approach:
        1. Compute prefix_sums array where prefix_sums[i] is the sum of nums[0...i-1].
        2. prefix_sums has length N + 1 with prefix_sums[0] = 0.
        3. For each index i, left_sum = prefix_sums[i], total_sum = prefix_sums[N].
        4. right_sum = total_sum - prefix_sums[i + 1].
        5. Check if left_sum == right_sum.

        Time Complexity: O(N) where N is the length of nums.
        Space Complexity: O(N) auxiliary space to store prefix sums.
        """

        n = len(nums)
        prefix_sums = [0] * (n + 1)

        for i in range(n):
            prefix_sums[i + 1] = prefix_sums[i] + nums[i]

        total_sum = prefix_sums[n]

        for i in range(n):
            left_sum = prefix_sums[i]
            right_sum = total_sum - prefix_sums[i + 1]
            if left_sum == right_sum:
                return i

        return -1


if __name__ == "__main__":
    solution = Solution()

    tests = [
        ([1, 7, 3, 6, 5, 6], 3),
        ([1, 2, 3], -1),
        ([2, 1, -1], 0),
        ([0, 0, 0, 0], 0),
        ([-1, -1, 0, 1, 1, 0], 5),
    ]

    for index, (nums_input, expected) in enumerate(tests, 1):
        print(f"--- Test Case {index} ---")
        print(f"Input: nums = {nums_input}")
        print(f"Expected Output: {expected}")

        result1 = solution.pivotIndex(list(nums_input))
        print(f"pivotIndex Output: {result1}")
        assert result1 == expected, f"Failed pivotIndex for {nums_input}"

        result2 = solution.pivotIndex_prefix_array(list(nums_input))
        print(f"pivotIndex_prefix_array Output: {result2}")
        assert result2 == expected, f"Failed pivotIndex_prefix_array for {nums_input}"

    print("\nAll main test cases passed successfully.")
