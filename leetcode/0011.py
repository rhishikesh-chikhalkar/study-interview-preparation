"""
11. Container With Most Water
Medium

You are given an integer array height of length n. There are n vertical lines drawn
such that the two endpoints of the i-th line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container
contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

Example 1:
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7].
In this case, the max area of water the container can contain is 49.

Example 2:
Input: height = [1,1]
Output: 1

Constraints:
n == height.length
2 <= n <= 10^5
0 <= height[i] <= 10^4
"""

from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        """
        Calculates the maximum water a container can store using two pointers.

        Approach:
        1. Place one pointer `left` at index 0 and one pointer `right` at index len(height) - 1.
        2. Calculate the current container area:
           area = min(height[left], height[right]) * (right - left)
        3. Update `max_water` if `current_area` is larger.
        4. Move the pointer pointing to the shorter vertical line inward:
           - The area is constrained by the shorter line (bottleneck).
           - Moving the taller line cannot increase area because the width decreases
             and the height cannot exceed the current shorter line.
           - Moving the shorter line is the only way to potentially find a taller line.
        5. Repeat until `left == right`.

        Time Complexity: O(N) where N is len(height), since each pointer moves inward once.
        Space Complexity: O(1) auxiliary space.
        """

        left = 0
        right = len(height) - 1
        max_water = 0

        while left < right:
            h_left = height[left]
            h_right = height[right]
            current_height = min(h_left, h_right)
            current_width = right - left
            current_area = current_height * current_width

            if current_area > max_water:
                max_water = current_area

            if h_left < h_right:
                left += 1
            else:
                right -= 1

        return max_water

    def maxArea_optimized_skip(self, height: List[int]) -> int:
        """
        Two-pointer approach with fast-skipping lines shorter than the current bottleneck.

        Approach:
        1. Maintain `left` and `right` pointers from outer edges inward.
        2. Identify the shorter line `h_min`.
        3. Advance the pointer on the shorter side until encountering a line strictly taller
           than `h_min`, skipping redundant area calculations for guaranteed smaller areas.

        Time Complexity: O(N) where N is len(height).
        Space Complexity: O(1) auxiliary space.
        """

        left = 0
        right = len(height) - 1
        max_water = 0

        while left < right:
            h_left = height[left]
            h_right = height[right]
            current_width = right - left

            if h_left < h_right:
                area = h_left * current_width
                if area > max_water:
                    max_water = area
                while left < right and height[left] <= h_left:
                    left += 1
            else:
                area = h_right * current_width
                if area > max_water:
                    max_water = area
                while left < right and height[right] <= h_right:
                    right -= 1

        return max_water


def run_test(height: List[int]) -> None:
    result = Solution().maxArea(height)
    print(f"height={height} --> max_water={result}")


if __name__ == "__main__":
    run_test([1, 8, 6, 2, 5, 4, 8, 3, 7])
    run_test([1, 1])
    run_test([4, 3, 2, 1, 4])
    run_test([1, 2, 1])
