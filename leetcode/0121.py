"""
121. Best Time to Buy and Sell Stock
Easy
Topics
premium lock icon
Companies
You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

Example 1:

Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.
Example 2:

Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.

Constraints:

1 <= prices.length <= 105
0 <= prices[i] <= 104

"""

from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """
        Groups the current single pass approach.

        Time Complexity: O(N) where N is the length of prices.
        Space Complexity: O(1) auxiliary space.
        """
        min_price = float("inf")
        max_profit = 0
        for price in prices:
            if price < min_price:
                min_price = price
            elif price - min_price > max_profit:
                max_profit = price - min_price
        return max_profit

    def maxProfit_two_pointers(self, prices: List[int]) -> int:
        """
        Sliding Window / Two Pointers approach.

        Time Complexity: O(N) where N is the length of prices.
        Space Complexity: O(1) auxiliary space.
        """
        left = 0  # Buy day
        right = 1  # Sell day
        max_profit = 0
        while right < len(prices):
            if prices[left] < prices[right]:
                profit = prices[right] - prices[left]
                max_profit = max(max_profit, profit)
            else:
                left = right
            right += 1
        return max_profit

    def maxProfit_kadane(self, prices: List[int]) -> int:
        """
        Kadane's Algorithm (Maximum Subarray Sum) on daily price differences.

        Time Complexity: O(N) where N is the length of prices.
        Space Complexity: O(1) auxiliary space.
        """
        max_profit = 0
        current_profit = 0
        for i in range(1, len(prices)):
            diff = prices[i] - prices[i - 1]
            current_profit = max(0, current_profit + diff)
            max_profit = max(max_profit, current_profit)
        return max_profit


if __name__ == "__main__":
    solution = Solution()

    # Test inputs
    tests = [
        [7, 1, 5, 3, 6, 4],
        [7, 6, 4, 3, 1],
    ]

    for i, prices in enumerate(tests, 1):
        print(f"--- Example {i} ---")
        print(f"Input: prices = {prices}")
        print(f"One pass output:       {solution.maxProfit(prices)}")
        print(f"Two pointers output:   {solution.maxProfit_two_pointers(prices)}")
        print(f"Kadane's output:       {solution.maxProfit_kadane(prices)}")
        print()
