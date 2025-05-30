class Solution:
    def hasIncreasingSubarrays(self, nums: list[int], k: int) -> bool:

        def mono(idx: int) -> bool:

            for i in range(idx, idx + k - 1):
                if nums[i] >= nums[i + 1]:
                    return False

            return True

        for idx in range(len(nums) - k - k + 1):
            if mono(idx) and mono(idx + k):
                return True

        return False
