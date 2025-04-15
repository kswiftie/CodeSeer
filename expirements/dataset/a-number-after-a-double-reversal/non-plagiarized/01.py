class Solution:
    def isSameAfterReversals(self, num: int) -> bool:
        dup = num
        rev = 0
        while dup != 0:
            d = dup % 10
            rev = rev * 10 + d
            dup = dup // 10
        while rev != 0:
            d = rev % 10
            dup = dup * 10 + d
            rev = rev // 10
        if dup == num:
            return True
        else:
            return False
