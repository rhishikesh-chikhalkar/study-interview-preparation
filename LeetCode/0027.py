"""
27. Remove Element
Easy

Given an integer array nums and an integer val, remove all occurrences of val in nums in-place. The order of the elements may be changed. Then return the number of elements in nums which are not equal to val.

Consider the number of elements in nums which are not equal to val be k, to get accepted, you need to do the following things:

Change the array nums such that the first k elements of nums contain the elements which are not equal to val. The remaining elements of nums are not important as well as the size of nums.
Return k.

Custom Judge:

The judge will test your solution with the following code:

int[] nums = [...]; // Input array
int val = ...; // Value to remove
int[] expectedNums = [...]; // The expected answer with correct length.
                            // It is sorted with no values equaling val.

int k = removeElement(nums, val); // Calls your implementation

assert k == expectedNums.length;
sort(nums, 0, k); // Sort the first k elements of nums
for (int i = 0; i < actualLength; i++) {
    assert nums[i] == expectedNums[i];
}
If all assertions pass, then your solution will be accepted.

Example 1:
Input: nums = [3,2,2,3], val = 3
Output: 2, nums = [2,2,_,_]
Explanation: Your function should return k = 2, with the first two elements of nums being 2.
It does not matter what you leave beyond the returned k (hence they are underscores).

Example 2:
Input: nums = [0,1,2,2,3,0,4,2], val = 2
Output: 5, nums = [0,1,4,0,3,_,_,_]
Explanation: Your function should return k = 5, with the first five elements of nums containing 0, 0, 1, 3, and 4.
Note that the five elements can be returned in any order.
It does not matter what you leave beyond the returned k (hence they are underscores).

Constraints:
0 <= nums.length <= 100
0 <= nums[i] <= 50
0 <= val <= 100
"""

from typing import List


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        """
        Removes all occurrences of val in nums in-place and returns the number of elements not equal to val (k).

        Time Complexity: O(N) where N is the length of nums.
        Space Complexity: O(1) auxiliary space.
        """
        k = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[k] = nums[i]
                k += 1
        return k

    def removeElement_swap(self, nums: List[int], val: int) -> int:
        """
        Alternative approach: Swapping elements with the end of the array.
        Optimized for scenarios where elements to remove are rare (fewer writes).

        Time Complexity: O(N) where N is the length of nums.
        Space Complexity: O(1) auxiliary space.
        """
        i = 0
        n = len(nums)
        while i < n:
            if nums[i] == val:
                nums[i] = nums[n - 1]
                n -= 1
            else:
                i += 1
        return n


if __name__ == "__main__":
    solution = Solution()

    # Test cases
    tests = [
        # (nums, val, expected_k, expected_elements)
        ([3, 2, 2, 3], 3, 2, [2, 2]),
        ([0, 1, 2, 2, 3, 0, 4, 2], 2, 5, [0, 1, 3, 0, 4]),
        ([], 0, 0, []),
        ([1], 1, 0, []),
        ([2], 3, 1, [2]),
    ]

    for i, (nums_orig, val, exp_k, exp_elems) in enumerate(tests, 1):
        print(f"--- Test Case {i} ---")
        print(f"Input: nums = {nums_orig}, val = {val}")

        # Test Method 1
        nums1 = list(nums_orig)
        k1 = solution.removeElement(nums1, val)
        actual_elems1 = sorted(nums1[:k1])
        expected_sorted = sorted(exp_elems)
        success1 = k1 == exp_k and actual_elems1 == expected_sorted
        print(
            f"Method 1 Output: k = {k1}, modified nums (first k) = {nums1[:k1]} -> Success: {success1}"
        )

        # Test Method 2
        nums2 = list(nums_orig)
        k2 = solution.removeElement_swap(nums2, val)
        actual_elems2 = sorted(nums2[:k2])
        success2 = k2 == exp_k and actual_elems2 == expected_sorted
        print(
            f"Method 2 Output: k = {k2}, modified nums (first k) = {nums2[:k2]} -> Success: {success2}"
        )
        print()
