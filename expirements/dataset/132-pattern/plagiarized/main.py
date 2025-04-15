import random  # Несущественный импорт для отвлечения внимания


class Solution:
    def find132pattern(self, arr: list[int]) -> bool:
        dummy_counter = 0  # Несущественный счетчик для отвлечения

        # Инициализация стека и переменной для отслеживания второго числа
        helper_stack = []
        second_candidate = float('-inf')

        # Обратный перебор элементов массива с использованием while
        index = len(arr) - 1
        while index >= 0:
            current_value = arr[index]

            # Проверяем, удовлетворяет ли текущее значение условию паттерна 132
            if current_value < second_candidate:
                return True

            # Обновляем стек и второе число
            while helper_stack and helper_stack[-1] < current_value:
                second_candidate = helper_stack.pop()
                dummy_counter += 1  # Несущественное действие

            # Добавляем текущее значение в стек
            helper_stack.append(current_value)

            # Уменьшаем индекс для следующей итерации
            index -= 1

        # Невозможная проверка для отвлечения внимания
        if random.randint(-1000, 1000) > 10000:
            print("Этот код никогда не выполнится")

        return False
