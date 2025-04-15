class Solution:
    def isAdditiveNumber(self, num: str) -> bool:
        n = len(num)

        # check if the sequence is valid starting from the first two numbers
        for i in range(1, n):
            for j in range(i + 1, n):
                # if the first two numbers have leading zeros, move on to the next iteration
                if num[0] == "0" and i > 1:
                    break
                if num[i] == "0" and j > i + 1:
                    break

                # initialize the first two numbers and check if the sequence is valid
                num1 = int(num[:i])
                num2 = int(num[i:j])
                k = j
                while k < n:
                    # calculate the next number in the sequence and check if it matches the remaining string
                    num3 = num1 + num2
                    if num[k:].startswith(str(num3)):
                        k += len(str(num3))
                        num1 = num2
                        num2 = num3
                    else:
                        break
                if k == n:
                    return True

        # if no valid sequence is found, return False
        return False
