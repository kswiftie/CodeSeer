class ListNode:
    pass

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:

        n1 = n2 = 0
        ptr1, ptr2 = l1, l2
        stack = []

        while ptr1: n1 += 1; ptr1 = ptr1.next
        while ptr2: n2 += 1; ptr2 = ptr2.next
        max_len = max(n1, n2)

        while max_len:
            a = b = 0
            if max_len <= n1: a = l1.val; l1 = l1.next
            if max_len <= n2: b = l2.val; l2 = l2.next
            stack.append(a + b)
            max_len -= 1

        sumval, head = 0, None
        while stack or sumval:
            if stack: sumval += stack.pop()
            node = ListNode(sumval % 10)
            node.next = head
            head = node
            sumval //= 10
        return head
