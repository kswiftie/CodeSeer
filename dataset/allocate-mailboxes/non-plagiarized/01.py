class Solution:
    def minDistance(self, houses: list[int], k: int) -> int:
        houses.sort()
        n = len(houses)

        @cache
        def helper(i, j, k):
            # from house i to house j, k boxes
            if i == j:
                return 0
            if k == 1:
                l = j - i + 1
                mid = i + l // 2
                dist = 0
                for idx in range(i, j + 1):
                    dist += abs(houses[mid] - houses[idx])
                return dist
            else:
                result = inf
                for idx in range(i, j):
                    result = min(result, helper(i, idx, 1) + helper(idx + 1, j, k - 1))
                return result

        return helper(0, n - 1, k)
