class Solution:
    def advantageCount(self, nums1: list[int], nums2: list[int]) -> list[int]:
        from collections import deque

        q = deque(sorted(nums1))
        n = len(nums1)
        order = sorted(range(n), key=lambda x: nums2[x], reverse=True)
        res = [0] * n
        for idx in order:
            if q[-1] > nums2[idx]:
                res[idx] = q.pop()
            else:
                res[idx] = q.popleft()
        return res
