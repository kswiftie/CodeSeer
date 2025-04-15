from collections import defaultdict


class Solution:
    def fourSumCount(self, nums1: list[int], nums2: list[int], nums3: list[int], nums4: list[int]) -> int:

        # hashmap and final result count
        nums12, res = defaultdict(int), 0

        # storing all possible combinations of sum
        for i in nums1:
            for j in nums2:
                nums12[i + j] += 1

        # iterating the left out two array to find negation of same value
        for k in nums3:
            for l in nums4:
                res += nums12[-(k + l)]

        return res
