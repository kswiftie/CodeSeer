class Solution:
    def isSameAfterReversals(self, num: int) -> bool:
        # False cases are those if last the digit of any 2(+) digit number = 0
        if len(str(num)) > 1 and str(num)[-1] == "0":
            return False
        else:
            # Else, every integer is true
            return True
