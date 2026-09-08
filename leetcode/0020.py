"""
20. Valid Parentheses
Easy

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

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

1 <= s.length <= 10^4
s consists of parentheses only '()[]{}'.
"""


class Solution:
    def is_valid(self, s: str) -> bool:
        """Stack + hash map approach for bracket matching.

        Time Complexity: O(N) where N is the length of s.
        Space Complexity: O(N) auxiliary space (worst case all openers).
        """

        if len(s) % 2 != 0:
            return False

        closer_to_opener: dict[str, str] = {
            ")": "(",
            "]": "[",
            "}": "{",
        }
        stack: list[str] = []

        for char in s:
            if char in closer_to_opener:
                if not stack or stack[-1] != closer_to_opener[char]:
                    return False
                stack.pop()
            else:
                stack.append(char)

        return not stack

    def is_valid_complement_push(self, s: str) -> bool:
        """Complement push variant: pushes expected closer instead of opener.

        On an opener, push the matching closer onto the stack. On a closer,
        pop and compare directly -- no hash map lookup needed at comparison.

        Time Complexity: O(N) where N is the length of s.
        Space Complexity: O(N) auxiliary space (worst case all openers).
        """

        if len(s) % 2 != 0:
            return False

        stack: list[str] = []

        for char in s:
            if char == "(":
                stack.append(")")
            elif char == "[":
                stack.append("]")
            elif char == "{":
                stack.append("}")
            elif not stack or stack.pop() != char:
                return False

        return not stack


if __name__ == "__main__":
    solution = Solution()

    tests: list[tuple[str, bool]] = [
        ("(", False),
        ("()", True),
        ("([{}])", True),
        ("([)]", False),
        ("(((", False),
        (")))", False),
        ("(){}[]", True),
        ("{[()]}", True),
    ]

    for i, (s, expected) in enumerate(tests, 1):
        print(f"--- Test Case {i} ---")
        print(f"Input: s = {s!r}")
        print(f"Expected: {expected}")

        r1 = solution.is_valid(s)
        print(f"Method 1 (Stack + Hash Map):    {r1}")
        assert r1 == expected, f"Failed method 1 for {s!r}"

        r2 = solution.is_valid_complement_push(s)
        print(f"Method 2 (Complement Push):     {r2}")
        assert r2 == expected, f"Failed method 2 for {s!r}"
        print("All checks passed!\n")
