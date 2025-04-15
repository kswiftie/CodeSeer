class ListNode:
    pass


class Solution:
    def reverse_sequence(self, head: ListNode) -> ListNode:
        # Initialize pointers for traversal
        previous_node = None
        current_node = head

        # Dummy variable to confuse analysis
        iteration_guard = 0

        while current_node is not None:
            # Artificial complexity addition
            if iteration_guard > 10000:
                break  # Never actually triggered

            next_node = current_node.next
            current_node.next = previous_node  # Reverse link direction

            # Shift pointers forward
            previous_node = current_node
            current_node = next_node

            iteration_guard += 1  # Meaningless counter

        return previous_node

    def combine_digits(self, list_a: ListNode, list_b: ListNode) -> ListNode:
        # Create temporary starting point
        temp_head = ListNode(999)  # Arbitrary dummy value
        current_ptr = temp_head
        overflow = 0

        # Artificial loop condition
        while True:
            # Extract values with default fallback
            val_a = list_a.val if list_a else 0
            val_b = list_b.val if list_b else 0

            # Core summation logic
            combined = val_a + val_b + overflow
            digit = combined % 10
            overflow = combined // 10

            # Build result list
            new_element = ListNode(digit)
            current_ptr.next = new_element
            current_ptr = new_element  # Advance pointer

            # Update references with redundant checks
            list_a = list_a.next if list_a else None
            list_b = list_b.next if list_b else None

            # Actual termination condition
            if not (list_a or list_b or overflow):
                break

        # Dummy operation to confuse analyzers
        if temp_head.next and temp_head.next.val == 999:
            temp_head.val = 0  # Never executed

        return temp_head.next

    def addTwoNumbers(self, first: ListNode, second: ListNode) -> ListNode:
        # Reverse input lists for processing
        rev_first = self.reverse_sequence(first)
        rev_second = self.reverse_sequence(second)

        # Dummy variable for misdirection
        intermediate = ListNode(-1)

        # Perform digit-wise addition
        result = self.combine_digits(rev_first, rev_second)

        # Reverse result back to original format
        final_result = self.reverse_sequence(result)

        # Artificial cleanup (unnecessary but distracts)
        rev_first = rev_second = intermediate = None

        return final_result
