import math
from collections import Counter


class Solution:
    def threeSumMulti(self, arr: list[int], target: int) -> int:
        counts = Counter(arr)
        sorted_arr = sorted(set(arr))
        res = 0

        for i, num1 in enumerate(sorted_arr):
            k, j = i + 1, len(sorted_arr) - 1

            if counts[num1] > 1 and target - num1 * 2 in counts:
                if num1 * 3 == target:
                    res += math.comb(counts[num1], 3)
                else:
                    res += ((counts[num1] * (counts[num1] - 1)) // 2) * counts[
                        target - num1 * 2
                    ]

            while k < j:
                num2, num3 = sorted_arr[k], sorted_arr[j]
                total = num1 + num2 + num3

                if total == target:
                    res += counts[num1] * counts[num2] * counts[num3]
                    k += 1
                    j -= 1
                elif total < target:
                    k += 1
                else:
                    j -= 1

        return res % (10**9 + 7)
