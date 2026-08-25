"""
15. 3Sum
Medium

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that
i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Example 1:
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation:
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.

Example 2:
Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.

Example 3:
Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.

Constraints:
3 <= nums.length <= 3000
-10^5 <= nums[i] <= 10^5
"""

from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        Finds all unique triplets that sum to zero using sorting and two pointers.

        Approach:
        1. Sort the input array in ascending order.
        2. Iterate through nums with index i as the first element:
           - If nums[i] > 0, stop early (sum of 3 positive numbers cannot be 0).
           - If i > 0 and nums[i] == nums[i - 1], skip duplicate first elements.
        3. Use two pointers (left = i + 1, right = len(nums) - 1):
           - If total == 0: record triplet, advance left and right skipping duplicates.
           - If total < 0: increment left to increase the sum.
           - If total > 0: decrement right to decrease the sum.

        Time Complexity: O(N^2) where N is len(nums).
        Space Complexity: O(1) auxiliary space (or O(N) depending on Python's Timsort).
        """

        nums.sort()
        n = len(nums)
        triplets: List[List[int]] = []

        for i in range(n - 2):
            # If the current smallest value is greater than 0, remaining sum cannot be 0
            if nums[i] > 0:
                break

            # Skip duplicate first elements
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            left, right = i + 1, n - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]

                if total == 0:
                    triplets.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1

                    # Skip duplicate second elements
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1

                    # Skip duplicate third elements
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1

                elif total < 0:
                    left += 1
                else:
                    right -= 1

        return triplets

    def threeSum_hashset(self, nums: List[int]) -> List[List[int]]:
        """
        Finds all unique triplets using sorting and a hash set for the inner pair search.

        Approach:
        1. Sort the array to simplify duplicate triplet handling.
        2. For each unique element nums[i], maintain a hash set of visited values.
        3. For each j > i, check if complement (-nums[i] - nums[j]) exists in the set.
        4. Advance j, skipping duplicates to avoid redundant triplets.

        Time Complexity: O(N^2) where N is len(nums).
        Space Complexity: O(N) auxiliary space for the hash set.
        """

        nums.sort()
        n = len(nums)
        triplets: List[List[int]] = []

        for i in range(n - 2):
            if nums[i] > 0:
                break
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            seen = set()
            j = i + 1
            while j < n:
                complement = -nums[i] - nums[j]
                if complement in seen:
                    triplets.append([nums[i], complement, nums[j]])
                    while j + 1 < n and nums[j] == nums[j + 1]:
                        j += 1
                seen.add(nums[j])
                j += 1

        return triplets

    def threeSum_no_sort(self, nums: List[int]) -> List[List[int]]:
        """
        Finds all unique triplets without sorting the original input array.

        Approach:
        1. Maintain an outer set of seen elements to avoid duplicate outer searches.
        2. Maintain a map/set of seen pairs to deduplicate found triplets.
        3. For each element nums[i], perform a two-sum lookup using a local hash set.

        Time Complexity: O(N^2) where N is len(nums).
        Space Complexity: O(N) auxiliary space for hash sets.
        """

        res = set()
        dups = set()
        seen: dict[int, int] = {}

        for i, val1 in enumerate(nums):
            if val1 in dups:
                continue
            dups.add(val1)

            for j in range(i + 1, len(nums)):
                val2 = nums[j]
                complement = -val1 - val2
                if complement in seen and seen[complement] == i:
                    triplet = tuple(sorted((val1, val2, complement)))
                    res.add(triplet)
                seen[val2] = i

        return [list(t) for t in res]


def run_test(nums: List[int]) -> None:
    result = Solution().threeSum(nums)
    print(f"nums={nums} --> result={result}")


if __name__ == "__main__":
    run_test([-1, 0, 1, 2, -1, -4])
    run_test([0, 1, 1])
    run_test([0, 0, 0])
