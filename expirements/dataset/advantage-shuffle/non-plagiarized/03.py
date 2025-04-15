class Solution:
    def advantageCount(self, nums1: list[int], nums2: list[int]) -> list[int]:
        sorted_nums1 = sorted(nums1)
        sorted_nums2 = sorted((num, i) for i, num in enumerate(nums2))
        res = [0] * len(nums1)
        remaining = []
        j = 0

        for num in sorted_nums1:
            if num > sorted_nums2[j][0]:
                res[sorted_nums2[j][1]] = num
                j += 1
            else:
                remaining.append(num)

        for i in range(len(nums2)):
            if res[i] == 0:
                res[i] = remaining.pop()

        return res
