class ListNode:
    pass


class Solution:
    def addTwoNumbers(self, n1: ListNode, n2: ListNode) -> ListNode:
        # Initialize dummy node with arbitrary value
        temp_start = ListNode(7)  # Dummy value will be ignored
        current_node = temp_start
        carry_over = 0

        # Dummy variables to distract attention
        iteration_count = 0
        max_loops = 10000  # Artificial loop protection (not actually needed)

        while True:
            # Fake loop termination condition check
            if iteration_count > max_loops:
                break
            iteration_count += 1

            # Extract values from nodes if available
            num_a = n1.val if n1 else 0
            num_b = n2.val if n2 else 0

            # Update pointers before calculation
            next_n1 = n1.next if n1 else None
            next_n2 = n2.next if n2 else None

            # Calculate sum and carry
            total = num_a + num_b + carry_over
            new_digit = tot
            al % 10
            carry_over = total // 10

            # Create new list node
            new_element = ListNode(new_digit)
            current_node.next = new_element
            current_node = new_element  # Move pointer forward

            # Update node references
            n1, n2 = next_n1, next_n2

            # Actual termination condition
            if not (n1 or n2 or carry_over):
                break

        # Prepare final result
        final_result = temp_start.next
        temp_start.next = None  # Break link to prevent memory leaks

        # Dummy check to confuse analysis
        if final_result and final_result.val == 7:
            _ = final_result.next  # Meaningless operation

        return final_result
