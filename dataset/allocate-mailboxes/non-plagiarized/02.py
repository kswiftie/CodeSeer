class Solution:
    def minDistance(self, houses: list[int], m: int) -> int:
        @cache
        def cost(l, r):
            median = houses[(l + r) // 2]
            return sum(abs(houses[i] - median) for i in range(l, r))

        @cache
        def dp(i, j):
            if i == n:
                return 0
            if j == m:
                return inf
            return min(dp(k, j+1) + cost(i, k) for k in range(i+1, n+1-(m-j-1)))

        houses.sort()
        n = len(houses)
        return dp(0, 0)