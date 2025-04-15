class Solution:
    def threeSumClosest(self, nums: list[int], target: int) -> int:

        n = len(nums)
        nums.sort()
        diff = 20001
        val = 0
        for i in range(n):
            a = i + 1
            b = n - 1
            while (a < b):
                cc = nums[i] + nums[a] + nums[b]
                kk = abs(cc - target)
                if (kk < diff):
                    diff = kk
                    val = cc
                if (cc == target):
                    return target
                elif (cc < target):
                    a += 1
                else:
                    b -= 1

        return val