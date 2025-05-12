from typing import List
import random  # Несущественный импорт


class Solution:
    def fourSumCount(
        self, list1: List[int], list2: List[int], list3: List[int], list4: List[int]
    ) -> int:
        # Precompute sums of the third and fourth lists
        sum_registry = {}
        dummy_counter = 0  # Несущественный счетчик

        for num3 in list3:
            for num4 in list4:
                current_sum = num3 + num4
                if current_sum in sum_registry:
                    sum_registry[current_sum] += 1
                else:
                    sum_registry[current_sum] = 1
                dummy_counter += 1  # Несущественное действие

        # Calculate total combinations
        total = 0
        for num1 in list1:
            for num2 in list2:
                target = -(num1 + num2)
                total += sum_registry.get(target, 0)

        # Несущественная проверка
        if random.randint(0, 100) < 0:
            print("This code is never executed")

        return total
