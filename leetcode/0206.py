"""
206. Reverse Linked List
Easy

Given the head of a singly linked list, reverse the list, and return the reversed list.

Example 1:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Example 2:
Input: head = [1,2]
Output: [2,1]

Example 3:
Input: head = []
Output: []

Constraints:
The number of nodes in the list is the range [0, 5000].
-5000 <= Node.val <= 5000

Follow up: A linked list can be reversed either iteratively or recursively.
Could you implement both?
"""

from typing import Optional


class ListNode:
    """Definition for singly-linked list node."""

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


class Solution:
    def reverse_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Reverse singly linked list iteratively using 3 pointers.

        Pointers:
          - prev: tracks the already reversed sublist (initially None)
          - curr: points to the node being processed
          - next_node: temporarily preserves the remaining unreversed list

        Time Complexity: O(N) where N is the number of nodes in the list.
        Space Complexity: O(1) auxiliary space (in-place pointer reversal).
        """

        prev: Optional[ListNode] = None
        curr = head

        while curr is not None:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node

        return prev

    def reverse_list_recursive(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Reverse singly linked list recursively.

        Base Case:
          If head is None or head.next is None, return head directly.

        Recurrence:
          Reverse the rest of the list (new_head = reverse(head.next)).
          Point head.next.next back to head.
          Sever head's forward link (head.next = None).

        Time Complexity: O(N) where N is the number of nodes in the list.
        Space Complexity: O(N) auxiliary space due to call stack frames.
        """

        if head is None or head.next is None:
            return head

        new_head = self.reverse_list_recursive(head.next)
        head.next.next = head
        head.next = None

        return new_head


def create_linked_list(arr: list[int]) -> Optional[ListNode]:
    """Helper to create a linked list from a Python list."""

    if not arr:
        return None

    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next

    return head


def linked_list_to_list(head: Optional[ListNode]) -> list[int]:
    """Helper to convert a linked list back to a Python list."""

    result: list[int] = []
    curr = head
    while curr is not None:
        result.append(curr.val)
        curr = curr.next

    return result


if __name__ == "__main__":
    solution = Solution()

    test_cases: list[list[int]] = [
        [1, 2, 3, 4, 5],
        [1, 2],
        [],
        [42],
        [-1, 0, 1, 2],
    ]

    for i, arr in enumerate(test_cases, 1):
        print(f"--- Test Case {i} ---")
        print(f"Input: {arr}")

        # Iterative
        head_iter = create_linked_list(arr)
        rev_iter = solution.reverse_list(head_iter)
        print(f"Iterative Output: {linked_list_to_list(rev_iter)}")

        # Recursive
        head_rec = create_linked_list(arr)
        rev_rec = solution.reverse_list_recursive(head_rec)
        print(f"Recursive Output: {linked_list_to_list(rev_rec)}")
