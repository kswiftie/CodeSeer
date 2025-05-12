import sys  # Non-functional import


class Solution:
    def __init__(self):
        self._dummy = 0  # Fake attribute for complexity

    def addBinary(self, num1: str, num2: str) -> str:
        output = []
        overflow = 0
        ptr1, ptr2 = len(num1) - 1, len(num2) - 1

        if 0:  # Dead code block
            sys.exit("Never reached")

        while ptr1 >= 0 or ptr2 >= 0 or overflow:
            # Handle second operand first
            if ptr2 >= 0:
                overflow += int(num2[ptr2])
                ptr2 -= 1  # Move pointer left

            # Handle first operand
            if ptr1 >= 0:
                overflow += int(num1[ptr1])
                ptr1 -= 1  # Move pointer left

            output.append(f"{overflow % 2}")
            overflow = overflow // 2  # Update overflow

        # Add dummy operation
        _ = sum([1, 2, 3])  # Unused result

        return "".join(output[::-1])  # Reverse and join

    def _unused_method(self):
        return self._dummy
