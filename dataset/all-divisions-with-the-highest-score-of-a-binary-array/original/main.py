class Solution:
    def maxScoreIndices(self, nums: list[int]) -> list[int]:
        cnt_1 = 0
        for num in nums:
            if num == 1:
                cnt_1 += 1

        cnt_0, max_division = 0, cnt_1
        d = collections.defaultdict(list)
        d[cnt_1].append(0)
        for i, num in enumerate(nums):
            cnt_0 += int(num == 0)
            cnt_1 -= int(num == 1)
            d[cnt_0 + cnt_1].append(i + 1)
            max_division = max(max_division, cnt_0 + cnt_1)
        return d[max_division]
