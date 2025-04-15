class Solution:
    def fourSumCount(self, A: list[int], B: list[int], C: list[int], D: list[int]) -> int:
        res, d = 0, {}
        for n1 in A:
            for n2 in B:
                tmp = n1 + n2
                if tmp in d:
                    d[tmp] += 1
                else:
                    d[tmp] = 1

        for n1 in C:
            for n2 in D:
                tmp = 0 - (n1 + n2)
                if tmp in d:
                    res += d[tmp]
        return res
