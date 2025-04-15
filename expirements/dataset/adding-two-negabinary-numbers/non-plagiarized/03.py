from typing import List


class Solution:
    def addNegabinary(self, arr1: List[int], arr2: List[int]) -> List[int]:
        l = []
        l1 = []
        for i in arr1:
            l.append(str(i))
        for i in arr2:
            l1.append(str(i))
        k = "".join(l)
        k1 = "".join(l1)

        def btd(f):
            f = f[::-1]
            d = 0
            b = -2
            for i, j in enumerate(f):
                if j == "1":
                    d += b**i
            return d

        m = btd(k) + btd(k1)
        if m == 0:
            return [0]

        q = []
        while m != 0:
            remainder = m % -2
            m //= -2
            if remainder < 0:
                remainder += 2
                m += 1
            q.append(remainder)

        return q[::-1]
