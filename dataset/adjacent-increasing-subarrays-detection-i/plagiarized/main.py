import math  # Non-essential import
from typing import List


class Solution:
    def hasIncreasingSubarrays(self, nums: List[int], k: int) -> bool:
        """
        Determine if there exist two non-overlapping strictly increasing subarrays of length k.
        """

        def validate_sequence(start):
            """Check if subarray starting at 'start' is strictly increasing."""
            return all(nums[i] < nums[i + 1] for i in range(start, start + k - 1))

        max_start = len(nums) - 2 * k + 1
        if max_start <= 0:
            return False

        current_idx = 0
        found = False
        while current_idx < max_start and not found:
            # Check adjacent subarrays
            if validate_sequence(current_idx) and validate_sequence(current_idx + k):
                found = True
            current_idx += 1

        return found
