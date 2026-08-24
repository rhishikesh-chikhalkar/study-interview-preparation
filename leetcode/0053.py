"""
53. Maximum Subarray
Medium
Topics
premium lock icon
Companies
Given an integer array nums, find the subarray with the largest sum, and return its sum.

Example 1:
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.

Example 2:
Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.

Example 3:
Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.

Constraints:
1 <= nums.length <= 10^5
-10^4 <= nums[i] <= 10^4

Follow up: If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.
"""

from typing import List, Tuple


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        """
        Kadane's Algorithm (Optimal).

        Maintains the maximum subarray sum ending at each position.
        At each element, we decide whether to add it to the existing subarray sum
        or start a new subarray from the current element.

        Time Complexity: O(N) where N is the length of nums.
        Space Complexity: O(1) auxiliary space.
        """
        current_sum = max_sum = nums[0]

        for num in nums[1:]:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)

        return max_sum

    def maxSubArray_divide_and_conquer(self, nums: List[int]) -> int:
        """
        Divide and Conquer Approach (Follow-up).

        Splits the array into left and right halves recursively. For each range,
        tracks: (total_sum, max_prefix, max_suffix, max_subarray).

        Time Complexity: O(N) because T(N) = 2T(N/2) + O(1).
        Space Complexity: O(log N) due to recursion stack depth.
        """

        def solve(left: int, right: int) -> Tuple[int, int, int, int]:
            if left == right:
                val = nums[left]
                return (val, val, val, val)

            mid = (left + right) // 2
            left_sum, left_pref, left_suff, left_max = solve(left, mid)
            right_sum, right_pref, right_suff, right_max = solve(mid + 1, right)

            total_sum = left_sum + right_sum
            max_prefix = max(left_pref, left_sum + right_pref)
            max_suffix = max(right_suff, right_sum + left_suff)
            max_subarray = max(left_max, right_max, left_suff + right_pref)

            return (total_sum, max_prefix, max_suffix, max_subarray)

        _, _, _, max_sub = solve(0, len(nums) - 1)
        return max_sub

    def maxSubArray_dp(self, nums: List[int]) -> int:
        """
        Explicit Dynamic Programming approach with DP array.

        dp[i] stores the maximum subarray sum ending at index i.
        dp[i] = max(nums[i], dp[i - 1] + nums[i])

        Time Complexity: O(N) where N is the length of nums.
        Space Complexity: O(N) to store the DP array.
        """
        n = len(nums)
        dp = [0] * n
        dp[0] = nums[0]

        for i in range(1, n):
            dp[i] = max(nums[i], dp[i - 1] + nums[i])

        return max(dp)

    def maxSubArray_with_subarray(self, nums: List[int]) -> Tuple[int, List[int]]:
        """
        Kadane's Algorithm variation that also returns the maximum subarray itself.

        Time Complexity: O(N)
        Space Complexity: O(1) auxiliary (excluding output subarray).
        """
        max_sum = nums[0]
        current_sum = nums[0]

        best_start = 0
        best_end = 0
        temp_start = 0

        for i in range(1, len(nums)):
            if nums[i] > current_sum + nums[i]:
                current_sum = nums[i]
                temp_start = i
            else:
                current_sum += nums[i]

            if current_sum > max_sum:
                max_sum = current_sum
                best_start = temp_start
                best_end = i

        return max_sum, nums[best_start : best_end + 1]


if __name__ == "__main__":
    solution = Solution()

    # Test inputs
    tests = [
        [-2, 1, -3, 4, -1, 2, 1, -5, 4],
        [1],
        [5, 4, -1, 7, 8],
        [-1],
        [-2, -1],
    ]

    for i, nums in enumerate(tests, 1):
        print(f"--- Example {i} ---")
        print(f"Input: nums = {nums}")
        print(f"Kadane's output:           {solution.maxSubArray(nums)}")
        print(
            f"Divide & Conquer output:   {solution.maxSubArray_divide_and_conquer(nums)}"
        )
        print(f"DP table output:           {solution.maxSubArray_dp(nums)}")
        max_s, sub_arr = solution.maxSubArray_with_subarray(nums)
        print(f"Max Subarray with range:   sum={max_s}, subarray={sub_arr}")
        print()
