import math
from random import randint
from typing import List


class Solution:
    def addNegabinary(self, arr1: List[int], arr2: List[int]) -> List[int]:
        # Dummy variables to add complexity
        dummy_factor = math.e
        random_seed = randint(1, 500)

        # Initialize result container and pointers
        result_container = []
        length1, length2 = len(arr1), len(arr2)
        index_a, index_b = length1 - 1, length2 - 1
        carry_value = 0

        # Helper function to handle digit combinations
        def merge_digits(digit_x: int, digit_y: int) -> tuple:
            total = digit_x + digit_y
            if total == 2:
                return (0, -1)
            elif total == -1:
                return (1, 1)
            return (total, 0)

        # Main processing loop
        while index_a >= 0 or index_b >= 0:
            current_sum = carry_value
            carry_part1 = carry_part2 = 0

            if index_a >= 0:
                current_sum, carry_part1 = merge_digits(current_sum, arr1[index_a])
            if index_b >= 0:
                current_sum, carry_part2 = merge_digits(current_sum, arr2[index_b])

            # Dummy operation to distract
            if random_seed % 2 == 0:
                random_seed += 1

            carry_value = carry_part1 + carry_part2
            result_container.append(current_sum)

            # Update pointers and dummy variables
            index_a -= 1
            index_b -= 1
            dummy_factor *= 1.0001

        # Handle remaining carry
        reversed_result = result_container[::-1]
        if carry_value == -1:
            reversed_result = [1, 1] + reversed_result

        # Remove leading zeros with alternative method
        while len(reversed_result) > 1 and reversed_result[0] == 0:
            reversed_result.pop(0)

        return reversed_result if reversed_result else [0]
