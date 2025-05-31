class Solution:
    def maxScoreIndices(self, nums: list[int]) -> list[int]:
        l1 = []
        l2 = [0] * len(nums)
        for i in range(len(nums)):
            if i == 0:
                if nums[i] == 0:
                    l1.append((1, 0))
                else:
                    l1.append((0, 1))
            else:
                if nums[i] == 0:
                    l1.append((l1[-1][0] + 1, l1[-1][1]))
                else:
                    l1.append((l1[-1][0], l1[-1][1] + 1))
        for i in range(len(nums) - 1, -1, -1):
            if i == len(nums) - 1:
                if nums[i] == 0:
                    l2[i] = (1, 0)
                else:
                    l2[i] = (0, 1)
            else:
                if nums[i] == 0:
                    l2[i] = (l2[i + 1][0] + 1, l2[i + 1][1])
                else:
                    l2[i] = (l2[i + 1][0], l2[i + 1][1] + 1)
        d = {}
        for i in range(len(nums)):
            if i == 0:
                d[i] = l2[i][1]
            elif i == len(nums) - 1:
                d[i] = l1[i - 1][0] + l2[i][1]
            else:
                d[i] = l1[i - 1][0] + l2[i][1]
        d[len(nums)] = l1[len(nums) - 1][0]
        k = max(d.values())
        ans = []
        for i in d:
            if d[i] == k:
                ans.append(i)
        return ans
