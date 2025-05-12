class Solution:
    def hasIncreasingSubarrays(self, nums: list[int], k: int) -> bool:
        # i is start of the current window
        i, j = 0, 1

        # Set to store indices of the ends of valid subarrays
        valid_ends = set()

        while j < len(nums) + 1:

            # Expand the window only if its strictly increasing and within size k
            while j < len(nums) and nums[j] > nums[j - 1] and j - i + 1 <= k:
                j += 1

            # If the just processed window is valid (of size k)
            if j - i == k:
                # If there's an adjacent valid subarray before the current one
                if (i - 1) in valid_ends:
                    return True
                valid_ends.add(j - 1)

            # Update pointers for next subarray
            i += 1
            j = i + 1

        return False
