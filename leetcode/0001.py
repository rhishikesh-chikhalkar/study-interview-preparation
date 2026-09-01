"""
1. Two Sum

Easy

Given an array of integers nums and an integer target, return indices of the
two numbers such that they add up to target.
You may assume that each input would have exactly one solution, and you may
not use the same element twice.
You can return the answer in any order.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]

Constraints:
2 <= nums.length <= 10^4
-10^9 <= nums[i] <= 10^9
-10^9 <= target <= 10^9
Only one valid answer exists.

Follow-up: Can you come up with an algorithm that is less than O(n^2) time complexity?
"""

from typing import Dict, List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        One-Pass Hash Map (Optimal).

        Approach:
        Iterate through the array while checking if complement (target - num)
        exists in the seen dictionary. If found, return indices immediately;
        otherwise record current number and index.

        Time Complexity: O(N) where N is len(nums).
        Space Complexity: O(N) for the hash map.
        """
        seen: Dict[int, int] = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []

    # Alias for snake_case compatibility
    two_sum = twoSum

    def twoSum_two_pass(self, nums: List[int], target: int) -> List[int]:
        """
        Two-Pass Hash Map.

        Approach:
        1. Populate hash map with value -> index mapping.
        2. Second pass checks if target - nums[i] exists and is not at index i.

        Time Complexity: O(N) where N is len(nums).
        Space Complexity: O(N) for the hash map.
        """
        num_map: Dict[int, int] = {num: i for i, num in enumerate(nums)}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_map and num_map[complement] != i:
                return [i, num_map[complement]]
        return []

    def twoSum_two_pointers(self, nums: List[int], target: int) -> List[int]:
        """
        Two Pointers with Index Sorting.

        Approach:
        1. Pair each number with its original index: (num, original_index).
        2. Sort pairs by value.
        3. Use two pointers from opposite ends inward to find target sum.

        Time Complexity: O(N log N) due to sorting.
        Space Complexity: O(N) to store pairs with original indices.
        """
        indexed_nums = sorted((num, i) for i, num in enumerate(nums))
        left = 0
        right = len(nums) - 1

        while left < right:
            current_sum = indexed_nums[left][0] + indexed_nums[right][0]
            if current_sum == target:
                return [indexed_nums[left][1], indexed_nums[right][1]]
            if current_sum < target:
                left += 1
            else:
                right -= 1

        return []

    def twoSum_brute_force(self, nums: List[int], target: int) -> List[int]:
        """
        Brute Force.

        Approach:
        Check all pairs (i, j) where i < j to see if nums[i] + nums[j] == target.

        Time Complexity: O(N^2) where N is len(nums).
        Space Complexity: O(1) auxiliary space.
        """
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []


def run_test(nums: List[int], target: int) -> None:
    sol = Solution()
    print(f"nums={nums} target={target}")
    print(f"  one_pass:     {sol.twoSum(nums, target)}")
    print(f"  two_pass:     {sol.twoSum_two_pass(nums, target)}")
    print(f"  two_pointers: {sol.twoSum_two_pointers(nums, target)}")
    print(f"  brute_force:  {sol.twoSum_brute_force(nums, target)}")


if __name__ == "__main__":
    run_test([2, 7, 11, 15], 9)
    run_test([3, 2, 4], 6)
    run_test([3, 3], 6)
