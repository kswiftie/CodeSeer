class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        res = []
        nums.sort()
        for i in range(len(nums)):
            if i == 0 or nums[i] > nums[i - 1]:
                diff = target - nums[i]
                threeSums = self.threeSum(nums[i + 1:], diff)
                for threeSum in threeSums:
                    res.append([nums[i]] + threeSum)
        return res

    def threeSum(self, nums: list[int], target: int) -> list[list[int]]:
        res = []
        if len(nums) < 3: return res

        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]: continue
            l, r = i + 1, len(nums) - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s == target:
                    res.append([nums[i], nums[l], nums[r]])
                    l += 1;
                    r -= 1
                    while l < r and nums[l] == nums[l - 1]: l += 1
                    while l < r and nums[r] == nums[r + 1]: r -= 1
                elif s < target:
                    l += 1
                else:
                    r -= 1
        return res
