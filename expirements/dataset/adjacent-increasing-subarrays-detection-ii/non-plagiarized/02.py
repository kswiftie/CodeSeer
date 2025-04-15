class Solution:
    def maxIncreasingSubarrays(self, nums: list[int]) -> int:
        n = len(nums)
        f = [0] * (n + 2)
        g = [0] * (n + 2)

        f[0] = 0
        for i in range(1, n + 1):
            if i > 1 and nums[i - 2] < nums[i - 1]:
                f[i] = f[i - 1] + 1
            else:
                f[i] = 1

        for i in range(n, 0, -1):
            if i < n and nums[i - 1] < nums[i]:
                g[i] = g[i + 1] + 1
            else:
                g[i] = 1

        ans = 0
        for i in range(1, n + 1):
            ans = max(ans, min(f[i - 1], g[i]))

        return ans
