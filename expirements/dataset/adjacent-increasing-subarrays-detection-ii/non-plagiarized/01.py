class Solution:
    def maxIncreasingSubarrays(self, nums: list[int]) -> int:

        n, beg, curr, mx = len(nums) - 1, 0, 0, 1

        while beg < n:
            prev, ptr = curr, beg + 1

            while ptr <= n and nums[ptr - 1] < nums[ptr]: ptr += 1

            curr, beg = ptr - beg, ptr
            k = min(prev, curr)
            mx = max(mx, curr // 2, k)

        return mx
