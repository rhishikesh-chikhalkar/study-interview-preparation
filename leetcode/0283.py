"""
283. Move Zeroes
Easy

Given an integer array nums, move all 0's to the end of it while maintaining the
relative order of the non-zero elements.

Note that you must do this in-place without making a copy of the array.

Example 1:

Input: nums = [0,1,0,3,12]
Output: [1,3,12,0,0]

Example 2:

Input: nums = [0]
Output: [0]

Constraints:

1 <= nums.length <= 10^4
-2^31 <= nums[i] <= 2^31 - 1

Follow up: Could you minimize the total number of operations done?
"""

from typing import List


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Moves all 0's to the end of nums in-place while maintaining relative order.
        Approach: Two-pointer (Write non-zeros, then fill remainder with zeros).

        Pointers:
          - left (slow pointer): Tracks the target position to place the next non-zero element.
          - right (fast pointer): Scans through the array looking for non-zero elements.

        Time Complexity: O(N) where N is the length of nums.
        Space Complexity: O(1) auxiliary space (in-place modification).
        """

        left = 0
        for right in range(len(nums)):
            if nums[right] != 0:
                nums[left] = nums[right]
                left += 1

        # Fill remaining elements with zeros
        for i in range(left, len(nums)):
            nums[i] = 0

    def moveZeroes_optimal_swaps(self, nums: List[int]) -> None:
        """
        Moves all 0's to the end of nums in-place using optimal swaps.
        Follow-up optimization: Minimizes total operations (writes).

        Pointers:
          - left (slow pointer): Points to the leftmost zero waiting to be swapped with
            a non-zero element.
          - right (fast pointer): Scans ahead looking for non-zero elements to move forward.

        Optimization ('if right != left'):
          - Avoids redundant self-swaps/writes when no zeros have been encountered yet.

        Time Complexity: O(N) where N is the length of nums.
        Space Complexity: O(1) auxiliary space (in-place modification).
        """

        left = 0
        for right in range(len(nums)):
            if nums[right] != 0:
                # Swap only if right and left are at different indices (a zero has been seen)
                if right != left:
                    nums[left], nums[right] = nums[right], nums[left]
                left += 1


if __name__ == "__main__":
    solution = Solution()

    # Test cases: (nums_input, expected_output)
    tests = [
        ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
        ([0], [0]),
        ([1, 2, 3, 4], [1, 2, 3, 4]),
        ([0, 0, 0], [0, 0, 0]),
        ([1, 0, 0, 0, 2], [1, 2, 0, 0, 0]),
        ([0, 0, 1], [1, 0, 0]),
    ]

    for i, (nums_orig, expected) in enumerate(tests, 1):
        print(f"--- Test Case {i} ---")
        print(f"Input: nums = {nums_orig}")
        print(f"Expected: {expected}")

        nums1 = list(nums_orig)
        solution.moveZeroes(nums1)
        print(f"Method 1 (Write & Fill) output:  {nums1}")
        assert nums1 == expected, f"Failed method 1 for {nums_orig}"

        nums2 = list(nums_orig)
        solution.moveZeroes_optimal_swaps(nums2)
        print(f"Method 2 (Optimal Swaps) output: {nums2}")
        assert nums2 == expected, f"Failed method 2 for {nums_orig}"
        print("All checks passed!\n")
