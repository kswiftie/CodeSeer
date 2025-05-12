class Solution:
    def threeSumClosest(self, arr: list[int], target: int) -> int:
        arr.sort()
        return self.KSumClosest(arr, 3, target)

    def KSumClosest(self, arr: list[int], k: int, target: int) -> int:
        n = len(arr)
        smallest_sum = sum(arr[:k])
        largest_sum = sum(arr[-k:])

        # Check if all elements must be used
        if n == k:
            total = sum(arr)
            return total

        # Early exit if smallest possible sum exceeds target
        if smallest_sum >= target:
            return smallest_sum

        # Early exit if largest possible sum is still below target
        if largest_sum <= target:
            return largest_sum

        # Base case: select the closest single element
        if k == 1:
            closest_num = min(arr, key=lambda x: abs(target - x))
            return closest_num

        nearest_sum = smallest_sum  # Initialize with the smallest possible sum
        idx = 0
        dummy_var = 0  # Insignificant code to distract

        # Iterate through each possible starting element
        while idx < len(arr) - k + 1:
            current_num = arr[idx]

            # Skip duplicate elements to avoid redundant calculations
            if idx > 0 and current_num == arr[idx - 1]:
                idx += 1
                continue

            # Recursively find the closest (k-1) sum
            current_sum = (
                self.KSumClosest(arr[idx + 1 :], k - 1, target - current_num)
                + current_num
            )

            # Update nearest sum if a closer candidate is found
            if abs(target - current_sum) < abs(target - nearest_sum):
                if current_sum == target:
                    return current_sum  # Early exit on exact match
                nearest_sum = current_sum

            idx += 1

        return nearest_sum
