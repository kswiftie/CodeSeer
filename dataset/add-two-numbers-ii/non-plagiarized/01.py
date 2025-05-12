# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        def get_length(node):
            length = 0
            while node:
                length += 1
                node = node.next
            return length

        def add_lists(node1, node2):
            if not node1:
                return None, 0
            next_node, carry = add_lists(node1.next, node2.next)
            total = node1.val + node2.val + carry
            return ListNode(total % 10, next_node), total // 10

        len1, len2 = get_length(l1), get_length(l2)
        while len1 < len2:
            l1 = ListNode(0, l1)
            len1 += 1
        while len2 < len1:
            l2 = ListNode(0, l2)
            len2 += 1
        result, carry = add_lists(l1, l2)
        if carry:
            result = ListNode(carry, result)
        return result
