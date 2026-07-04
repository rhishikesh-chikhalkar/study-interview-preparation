"""
20. Valid Parentheses

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Every close bracket has a corresponding open bracket of the same type.

Example 1:

Input: s = "()"

Output: true

Example 2:

Input: s = "()[]{}"

Output: true

Example 3:

Input: s = "(]"

Output: false

Example 4:

Input: s = "([])"

Output: true

Example 5:

Input: s = "([)]"

Output: false

Constraints:

1 <= s.length <= 104
s consists of parentheses only '()[]{}'.
"""

from typing import List


class Solution:
    def is_valid(self, s: str) -> bool:
        """Return True if every bracket in s is closed in the correct order."""
        stack: List[str] = []
        closing_to_opening = {")": "(", "]": "[", "}": "{"}

        for char in s:
            if char in closing_to_opening.values():
                stack.append(char)
                continue

            if not stack or stack[-1] != closing_to_opening.get(char, ""):
                return False

            stack.pop()

        return not stack


def run_test(s: str) -> None:
    result = Solution().is_valid(s)
    print(f"s={s!r} --> result={result}")


if __name__ == "__main__":
    run_test("()")
    run_test("()[]{}")
    run_test("(]")
    run_test("([])")
    run_test("([)]")
