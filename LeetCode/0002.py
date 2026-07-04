"""
Adding two numbers using linked list
"""

from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next_node: Optional["ListNode"] = None):
        self.val = val
        self.next = next_node


class Solution:
    def addTwoNumbers(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:
        dummy = ListNode(0)
        current = dummy
        carry = 0

        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            total = val1 + val2 + carry
            carry = total // 10

            current.next = ListNode(total % 10)
            current = current.next

            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next

        return dummy.next


# ---------- Helper Functions for Testing ----------


def build_linked_list(values: list[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    current = dummy
    for val in values:
        current.next = ListNode(val)
        current = current.next
    return dummy.next


def linked_list_to_list(node: Optional[ListNode]) -> list[int]:
    result: list[int] = []
    while node:
        result.append(node.val)
        node = node.next
    return result


def run_test(l1_vals: list[int], l2_vals: list[int]) -> None:
    l1 = build_linked_list(l1_vals)
    l2 = build_linked_list(l2_vals)
    result = Solution().addTwoNumbers(l1, l2)
    print(f"l1={l1_vals}, l2={l2_vals} --> result={linked_list_to_list(result)}")


# ---------- Sample Tests ----------

run_test([2, 4, 3], [5, 6, 4])  # Expected: [7, 0, 8]
run_test([0], [0])  # Expected: [0]
run_test([9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9])  # Expected: [8,9,9,9,0,0,0,1]
