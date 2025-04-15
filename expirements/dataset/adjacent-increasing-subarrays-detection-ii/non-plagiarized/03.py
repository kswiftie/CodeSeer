class Solution:
    def check(self, v, k):
        for i in range(len(v) - k):
            if v[i] >= k and v[i + k] >= k:
                return True
        return False

    def maxIncreasingSubarrays(self, nums):
        n = len(nums)
        if n == 2:
            return 1

        dp = [1] * n
        for i in range(1, n):
            if nums[i] <= nums[i - 1]:
                dp[i] = 1
            else:
                dp[i] = dp[i - 1] + 1

        ans = 1
        low, high = 1, n // 2

        while low <= high:
            mid = low + (high - low) // 2
            if self.check(dp, mid):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        return ans
