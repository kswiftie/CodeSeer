class Solution:
    def minSteps(self, n: int) -> int:
        curr = 1  # current number of 'A's on the screen
        clipboard = 0  # number of 'A's in the clipboard
        steps = 0  # number of steps taken to reach n 'A's
        # loop until curr equals n
        while curr < n:
            # if n is divisible by curr, perform copy and paste operations
            if n % curr == 0:
                clipboard = curr
                steps += 1
            # if n is not divisible by curr, perform only paste operation
            curr += clipboard
            steps += 1

        return steps
