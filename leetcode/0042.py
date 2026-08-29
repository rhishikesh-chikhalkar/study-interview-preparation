"""
42. Trapping Rain Water
Hard

Given n non-negative integers representing an elevation map where the width of each bar is 1,
compute how much water it can trap after raining.

Example 1:
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array
[0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.

Example 2:
Input: height = [4,2,0,3,2,5]
Output: 9

Constraints:
n == height.length
1 <= n <= 2 * 10^4
0 <= height[i] <= 10^5
"""

from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        """
        Computes trapped rain water using the optimal two-pointer approach.

        Approach:
        1. Maintain two pointers (`left` at index 0 and `right` at index len(height) - 1).
        2. Track the maximum height seen so far from the left (`left_max`) and right (`right_max`).
        3. At each step, compare `left_max` and `right_max`:
           - If `left_max < right_max`, water trapped at `left` is determined solely by `left_max`
             since `right_max` is guaranteed to be equal or taller. Add `left_max - height[left]`
             to total water and advance `left`.
           - Otherwise, water trapped at `right` is bounded by `right_max`. Add
             `right_max - height[right]` to total water and decrement `right`.
        4. Continue until `left > right`.

        Time Complexity: O(N) single pass through height array.
        Space Complexity: O(1) auxiliary space.
        """

        if not height:
            return 0

        left = 0
        right = len(height) - 1
        left_max = 0
        right_max = 0
        water_trapped = 0

        while left <= right:
            if left_max <= right_max:
                if height[left] >= left_max:
                    left_max = height[left]
                else:
                    water_trapped += left_max - height[left]
                left += 1
            else:
                if height[right] >= right_max:
                    right_max = height[right]
                else:
                    water_trapped += right_max - height[right]
                right -= 1

        return water_trapped

    def trap_monotonic_stack(self, height: List[int]) -> int:
        """
        Computes trapped rain water by tracking bounded basins horizontally using a monotonic stack.

        Approach:
        1. Maintain a monotonic decreasing stack of indices representing bar heights.
        2. Iterate through `height` with index `current`:
           - While stack is non-empty and `height[current] > height[stack[-1]]`:
             - Pop the top index as the bottom of the basin (`bottom = stack.pop()`).
             - If stack becomes empty, there is no left boundary, so break.
             - The new top of stack is the `left` boundary index.
             - Calculate bounded distance: `distance = current - left - 1`.
             - Calculate bounded height: `bounded_h = min(height[left], height[current]) - height[bottom]`.
             - Add `distance * bounded_h` to trapped water.
           - Push `current` onto stack.

        Time Complexity: O(N) where each index is pushed and popped at most once.
        Space Complexity: O(N) auxiliary space for stack.
        """

        stack: List[int] = []
        water_trapped = 0

        for current, h in enumerate(height):
            while stack and h > height[stack[-1]]:
                bottom = stack.pop()
                if not stack:
                    break
                left = stack[-1]
                distance = current - left - 1
                bounded_height = min(height[left], h) - height[bottom]
                water_trapped += distance * bounded_height
            stack.append(current)

        return water_trapped

    def trap_dp(self, height: List[int]) -> int:
        """
        Computes trapped rain water using prefix and suffix maximum arrays.

        Approach:
        1. Precompute `left_max` array where `left_max[i] = max(height[0..i])`.
        2. Precompute `right_max` array where `right_max[i] = max(height[i..n-1])`.
        3. For each index `i`, trapped water is `min(left_max[i], right_max[i]) - height[i]`.

        Time Complexity: O(N) with three linear passes.
        Space Complexity: O(N) auxiliary space for prefix and suffix arrays.
        """

        n = len(height)
        if n <= 2:
            return 0

        left_max = [0] * n
        right_max = [0] * n

        left_max[0] = height[0]
        for i in range(1, n):
            left_max[i] = max(left_max[i - 1], height[i])

        right_max[n - 1] = height[n - 1]
        for i in range(n - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], height[i])

        water_trapped = 0
        for i in range(n):
            water_trapped += min(left_max[i], right_max[i]) - height[i]

        return water_trapped


def run_test(height: List[int]) -> None:
    result = Solution().trap(height)
    print(f"height={height} --> trapped_water={result}")


if __name__ == "__main__":
    run_test([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    run_test([4, 2, 0, 3, 2, 5])
    run_test([])
    run_test([3, 0, 2, 0, 4])
