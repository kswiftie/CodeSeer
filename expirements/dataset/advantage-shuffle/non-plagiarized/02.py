class Solution:
    def advantageCount(self, A: list[int], B: list[int]) -> list[int]:
        sorted_a = sorted(A, reverse=True)  # descending order
        sorted_b = sorted(enumerate(B), key=lambda x: (x[1], x[0]),
                          reverse=True)  # descending order with original index
        n, j = len(B), 0
        ans = [-1] * n
        for i, (ori_idx, val) in enumerate(sorted_b):  # A greedily tries to cover value in B as large as possible
            if sorted_a[j] > val: ans[ori_idx], j = sorted_a[j], j + 1
        for i in range(n):  # assign rest value in A to ans
            if ans[i] == -1: ans[i], j = sorted_a[j], j + 1
        return ans
