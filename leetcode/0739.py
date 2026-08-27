"""
739. Daily Temperatures
Medium

Given an array of integers temperatures represents the daily temperatures,
return an array answer such that answer[i] is the number of days you have
to wait after the i-th day to get a warmer temperature. If there is no future
day for which this is possible, keep answer[i] == 0 instead.

Example 1:
Input: temperatures = [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]

Example 2:
Input: temperatures = [30,40,50,60]
Output: [1,1,1,0]

Example 3:
Input: temperatures = [30,60,90]
Output: [1,1,0]

Constraints:
1 <= temperatures.length <= 10^5
30 <= temperatures[i] <= 100
"""

from typing import List


class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        """
        Calculates wait days to the next warmer temperature using a monotonic stack.

        Approach:
        1. Maintain a monotonic decreasing stack storing indices of unresolved temperatures.
        2. For each day index `curr_idx` with temperature `curr_temp`:
           - Pop indices from the stack while `curr_temp > temperatures[stack[-1]]`.
           - For each popped index `prev_idx`, set `answer[prev_idx] = curr_idx - prev_idx`.
        3. Push `curr_idx` onto the stack.

        Time Complexity: O(N) since every index is pushed and popped at most once.
        Space Complexity: O(N) auxiliary space for the monotonic stack.
        """

        n = len(temperatures)
        answer: List[int] = [0] * n
        stack: List[int] = []

        for curr_idx, curr_temp in enumerate(temperatures):
            while stack and curr_temp > temperatures[stack[-1]]:
                prev_idx = stack.pop()
                answer[prev_idx] = curr_idx - prev_idx
            stack.append(curr_idx)

        return answer

    def dailyTemperatures_dp(self, temperatures: List[int]) -> List[int]:
        """
        Calculates wait days by iterating backwards and jumping using computed answers.

        Approach:
        1. Traverse from right to left (index N-1 down to 0).
        2. For day `i`, search forward starting at `j = i + 1`.
        3. If `temperatures[j] > temperatures[i]`, next warmer day is found: `answer[i] = j - i`.
        4. Else if `answer[j] == 0`, no future day is warmer than `temperatures[j]`,
           meaning no warmer day exists for `temperatures[i]`; break with `answer[i] = 0`.
        5. Else, jump forward directly to `j += answer[j]` and continue checking.

        Time Complexity: O(N) amortized.
        Space Complexity: O(1) auxiliary space (output array excluded).
        """

        n = len(temperatures)
        answer: List[int] = [0] * n

        for i in range(n - 1, -1, -1):
            j = i + 1
            while j < n:
                if temperatures[j] > temperatures[i]:
                    answer[i] = j - i
                    break
                if answer[j] == 0:
                    break
                j += answer[j]

        return answer


def run_test(temperatures: List[int]) -> None:
    result = Solution().dailyTemperatures(temperatures)
    print(f"temperatures={temperatures} --> result={result}")


if __name__ == "__main__":
    run_test([73, 74, 75, 71, 69, 72, 76, 73])
    run_test([30, 40, 50, 60])
    run_test([30, 60, 90])
