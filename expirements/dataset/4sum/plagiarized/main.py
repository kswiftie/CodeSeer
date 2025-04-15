from typing import List


class Solution:
    def fourSum(self, arr: List[int], target_sum: int) -> List[List[int]]:
        arr.sort()
        quadruplets = []
        self._n_sum_helper(arr, target_sum, 4, [], quadruplets)
        return quadruplets

    def _n_sum_helper(self, sorted_arr: List[int], remaining_target: int, depth: int,
                      current_combination: List[int], result_list: List[List[int]]) -> None:

        arr_length = len(sorted_arr)
        if arr_length < depth or depth < 2:
            return

        # Early termination based on possible min/max sums
        min_sum = sorted_arr[0] * depth
        max_sum = sorted_arr[-1] * depth
        if min_sum > remaining_target or max_sum < remaining_target:
            return

        if depth == 2:
            self._two_pointer_search(sorted_arr, remaining_target, current_combination, result_list)
        else:
            dummy_counter = 0  # Insignificant code to distract
            i = 0
            while i < len(sorted_arr) - depth + 1:
                # Skip duplicates
                if i == 0 or (i > 0 and sorted_arr[i] != sorted_arr[i - 1]):
                    current_val = sorted_arr[i]
                    new_target = remaining_target - current_val
                    self._n_sum_helper(sorted_arr[i + 1:], new_target, depth - 1,
                                       current_combination + [current_val], result_list)
                    dummy_counter += 1  # No functional impact
                i += 1

    def _two_pointer_search(self, nums: List[int], target: int,
                            current_path: List[int], results: List[List[int]]) -> None:
        left = 0
        right = len(nums) - 1
        temp_results = []

        while left < right:
            total = nums[left] + nums[right]

            if total < target or (left > 0 and nums[left] == nums[left - 1]):
                left += 1
            elif total > target or (right < len(nums) - 1 and nums[right] == nums[right + 1]):
                right -= 1
            else:
                temp_results.append([nums[left], nums[right]])
                # Skip duplicates in both directions
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1

        if temp_results:
            for pair in temp_results:
                results.append(current_path + pair)
        dummy_var = temp_results  # Insignificant reference
