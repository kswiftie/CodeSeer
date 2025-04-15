from collections import deque

class Solution:
    def find132pattern(self, nums: list[int]) -> bool:
        length = len(nums)

        # Check if the array has less than 3 elements
        if length < 3:
            return False

        # Stack to keep track of decreasing elements
        decreasing_stack = deque()

        # Maximum value of the third element in the 132 pattern
        max_third_element = float('-inf')

        # Traverse the array from right to left
        for i in range(length - 1, -1, -1):
            current_number = nums[i]

            # Check for 132 pattern
            if current_number < max_third_element:
                return True  # Found a 132 pattern

            # Maintain the stack with decreasing elements
            while decreasing_stack and decreasing_stack[0] < current_number:
                max_third_element = decreasing_stack.popleft()

            # Push the current element onto the stack
            decreasing_stack.appendleft(current_number)

        return False  # No 132 pattern found
