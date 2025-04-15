class Solution:
    def isAdditiveNumber(self, num: str) -> bool:
        def isValid(s: str) -> bool:
            return len(s) == 1 or s[0] != '0'

        def validSeq(f: str, s: str, l: str) -> bool:
            if len(l) == 0:
                return True
            sum_str = str(int(f) + int(s))
            if not l.startswith(sum_str):
                return False
            return validSeq(s, sum_str, l[len(sum_str):])

        n = len(num)
        for i in range(1, n // 2 + 1):
            for j in range(i + 1, n - i + 1):
                f, s, l = num[:i], num[i:j], num[j:]
                if isValid(f) and isValid(s) and validSeq(f, s, l):
                    return True

        return False
