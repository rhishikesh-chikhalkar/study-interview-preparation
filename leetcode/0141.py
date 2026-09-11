"""
141. Linked List Cycle

Easy

Given head, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be reached
again by continuously following the next pointer. Internally, pos is used to denote the
index of the node that tail's next pointer is connected to. Note that pos is not passed
as a parameter.

Return true if there is a cycle in the linked list. Otherwise, return false.

Example 1:
Input: head = [3,2,0,-4], pos = 1
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 1st node.

Example 2:
Input: head = [1,2], pos = 0
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 0th node.

Example 3:
Input: head = [1], pos = -1
Output: false
Explanation: There is no cycle in the linked list.

Constraints:
The number of the nodes in the list is in the range [0, 10^4].
-10^5 <= Node.val <= 10^5
pos is -1 or a valid index in the linked-list.

Follow up: Can you solve it using O(1) (i.e. constant) memory?
"""

from typing import List, Optional, Set


class ListNode:
    """Definition for singly-linked list node."""

    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        """
        Floyd's Tortoise and Hare Cycle-Finding Algorithm (Optimal).

        Approach:
        Use two pointers moving at different speeds: slow moves 1 step at a
        time, fast moves 2 steps. If a cycle exists, the fast pointer will
        eventually lap and meet the slow pointer within the loop.
        If fast reaches None (or fast.next is None), the list is acyclic.

        Time Complexity: O(N) where N is the number of nodes in the list.
        Space Complexity: O(1) auxiliary memory.
        """

        if head is None or head.next is None:
            return False

        slow: Optional[ListNode] = head
        fast: Optional[ListNode] = head

        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True

        return False

    # Alias for snake_case compatibility
    has_cycle = hasCycle

    def hasCycle_hash_set(self, head: Optional[ListNode]) -> bool:
        """
        Hash Set Membership Approach.

        Approach:
        Traverse the linked list while recording each visited node reference
        in a hash set. If a node reference already exists in the set, a cycle
        is detected. If traversal reaches None, the list is acyclic.

        Time Complexity: O(N) where N is the number of nodes in the list.
        Space Complexity: O(N) to store node references in the set.
        """

        visited: Set[ListNode] = set()
        curr = head

        while curr is not None:
            if curr in visited:
                return True
            visited.add(curr)
            curr = curr.next

        return False


def create_linked_list_with_cycle(values: List[int], pos: int) -> Optional[ListNode]:
    """
    Helper function to build a linked list with an optional cycle.

    pos is 0-indexed index of node that tail connects to (-1 means no cycle).
    """

    if not values:
        return None

    nodes = [ListNode(val) for val in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]

    if 0 <= pos < len(nodes):
        nodes[-1].next = nodes[pos]

    return nodes[0]
