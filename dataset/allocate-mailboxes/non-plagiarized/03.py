class Solution:
    def minDistance(self, houses: list[int], k: int) -> int:
        houses.sort()

        @cache
        def minDistanceOneMailbox(l: int, r: int) -> int:
            if l >= r:
                return 0

            return houses[r] - houses[l] + minDistanceOneMailbox(l + 1, r - 1)

        @cache
        def dp(i: int, kPrime: int) -> int:
            """Returns the answer for houses=houses[:i], k=kPrime"""
            if i == 0:
                return 0
            if kPrime == 0:
                return inf

            return min(dp(j, kPrime - 1) + minDistanceOneMailbox(j, i - 1) for j in range(i))

        return dp(len(houses), k)