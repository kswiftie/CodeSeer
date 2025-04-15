class Solution:
    def threeSumClosest(self, nums: list[int], target: int) -> int:
        nums.sort()
        res = float('inf')
        for i in range(len(nums)):
            l, r = i + 1, len(nums) - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if abs(s - target) < abs(res - target):
                    res = s
                if s == target:
                    return target
                elif s < target:
                    l += 1
                else:
                    r -= 1
        return res