# Python3
# Better Solution
from collections import defaultdict


class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        n = len(nums)
        ans = set()
        hmap = defaultdict(int)
        for i in nums:
            hmap[i] += 1

        for i in range(n - 3):
            hmap[nums[i]] -= 1
            for j in range(i + 1, n - 2):
                hmap[nums[j]] -= 1
                for k in range(j + 1, n - 1):
                    hmap[nums[k]] -= 1
                    rem = target - (nums[i] + nums[j] + nums[k])
                    if rem in hmap and hmap[rem] > 0:
                        ans.add(tuple(sorted((nums[i], nums[j], nums[k], rem))))
                    hmap[nums[k]] += 1
                hmap[nums[j]] += 1
            hmap[nums[i]] += 1

        res = []
        for i in ans:
            res += (list(i),)
        return res
