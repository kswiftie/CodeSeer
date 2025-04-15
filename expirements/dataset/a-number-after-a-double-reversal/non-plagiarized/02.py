class Solution:
    def isSameAfterReversals(self, num: int) -> bool:
        def reverse(number):
            result = 0
            while number:
                result = result * 10 + number % 10
                number //= 10
            return result

        return reverse(reverse(num)) == num