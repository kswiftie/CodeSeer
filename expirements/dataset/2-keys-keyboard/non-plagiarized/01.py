class Solution:
    def minSteps(self, n: int) -> int:
        if n == 1:
            return 0

        self.target_length = n

        def find_min_steps(current_length: int, clipboard_length: int) -> int:
            if current_length == self.target_length:
                return 0
            if current_length > self.target_length:
                return float('inf')

            copy_and_paste = 2 + find_min_steps(current_length * 2, current_length)
            paste_only = 1 + find_min_steps(current_length + clipboard_length, clipboard_length)

            return min(copy_and_paste, paste_only)

        return 1 + find_min_steps(1, 1)
