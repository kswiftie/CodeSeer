class Solution:
    def isSameAfterReversals(self, num):
        if (num == 0):
            return True

        num_str = str(num)
        len_num_str = len(num_str)

        return num_str[0] != '0' and num_str[len_num_str - 1] != '0'
