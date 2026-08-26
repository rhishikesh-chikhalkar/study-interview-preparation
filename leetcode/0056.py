"""
56. Merge Intervals
Medium

Given an array of intervals where intervals[i] = [start_i, end_i], merge all
overlapping intervals, and return an array of the non-overlapping intervals
that cover all the intervals in the input.

Example 1:
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

Example 2:
Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping.

Constraints:
1 <= intervals.length <= 10^4
intervals[i].length == 2
0 <= start_i <= end_i <= 10^4
"""

from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Merges overlapping intervals by sorting on start time and accumulating.

        Approach:
        1. Sort intervals ascending by start time: O(N log N).
        2. Iterate through sorted intervals:
           - If result list is empty or current start > last merged end, append.
           - Otherwise, extend the last merged interval end to max(last_end, current_end).

        Time Complexity: O(N log N) due to sorting.
        Space Complexity: O(N) for output list (and O(N) sort auxiliary space in Timsort).
        """

        if not intervals:
            return []

        intervals.sort(key=lambda x: x[0])
        merged: List[List[int]] = [intervals[0]]

        for current in intervals[1:]:
            last = merged[-1]
            if current[0] <= last[1]:
                last[1] = max(last[1], current[1])
            else:
                merged.append(current)

        return merged

    def merge_in_place(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Merges intervals using an in-place write pointer after sorting.

        Approach:
        1. Sort intervals in-place by start time: O(N log N).
        2. Maintain a write index representing the end of merged prefix.
        3. For each subsequent interval, either expand intervals[write] or advance write.
        4. Truncate intervals to length (write + 1).

        Time Complexity: O(N log N)
        Space Complexity: O(1) auxiliary space beyond sorting.
        """

        if not intervals:
            return []

        intervals.sort(key=lambda x: x[0])
        write = 0

        for read in range(1, len(intervals)):
            if intervals[read][0] <= intervals[write][1]:
                intervals[write][1] = max(intervals[write][1], intervals[read][1])
            else:
                write += 1
                intervals[write] = intervals[read]

        return intervals[: write + 1]


def run_test(intervals: List[List[int]]) -> None:
    result = Solution().merge(intervals)
    print(f"intervals={intervals} --> result={result}")


if __name__ == "__main__":
    run_test([[1, 3], [2, 6], [8, 10], [15, 18]])
    run_test([[1, 4], [4, 5]])
    run_test([[1, 4], [2, 3]])
    run_test([[1, 4], [0, 4]])
