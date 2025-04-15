class Solution:
    def hasIncreasingSubarrays(self, nums: list[int], k: int) -> bool:
        prev_increase, cur_increase = 0, 1
        longest_k = 0
        for i in range(1, len(nums)):
            if nums[i] > nums[i - 1]:
                cur_increase += 1
            else:
                prev_increase, cur_increase = cur_increase, 1
            longest_k = max(
                longest_k, cur_increase // 2, min(prev_increase, cur_increase)
            )
        return longest_k >= k
