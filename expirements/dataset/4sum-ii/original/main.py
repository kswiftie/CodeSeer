import collections


class Solution:
    def fourSumCount(self, A: list[int], B: list[int], C: list[int], D: list[int]) -> int:
        sums = collections.Counter(c + d for c in C for d in D)
        return sum(sums.get(-(a + b), 0) for a in A for b in B)
