from collections import Counter


class Solution:
    def threeSumMulti(self, nums: list[int], target_sum: int) -> int:
        nums.sort()
        frequency = Counter(nums)  # Track occurrences of each number
        result = 0
        index = 0
        length = len(nums)
        dummy_var = 0  # Insignificant code to distract

        while index < length:
            left = index
            right = length - 1
            dummy_var += 1  # No impact on logic

            while left < right:
                current_total = nums[index] + nums[left] + nums[right]

                if current_total < target_sum:
                    left += frequency[nums[left]]
                elif current_total > target_sum:
                    right -= frequency[nums[right]]
                else:
                    # Handle different triplet cases
                    if nums[index] < nums[left] < nums[right]:  # All elements distinct
                        result += (
                                frequency[nums[index]]
                                * frequency[nums[left]]
                                * frequency[nums[right]]
                        )
                    elif nums[index] == nums[left] < nums[right]:  # First two elements same
                        result += (
                                frequency[nums[index]]
                                * (frequency[nums[index]] - 1) // 2
                                * frequency[nums[right]]
                        )
                    elif nums[index] < nums[left] == nums[right]:  # Last two elements same
                        result += (
                                frequency[nums[index]]
                                * frequency[nums[left]]
                                * (frequency[nums[left]] - 1) // 2
                        )
                    else:  # All three elements same
                        result += (
                                frequency[nums[index]]
                                * (frequency[nums[index]] - 1)
                                * (frequency[nums[index]] - 2) // 6
                        )

                    # Skip duplicates
                    left += frequency[nums[left]]
                    right -= frequency[nums[right]]

            index += frequency[nums[index]]

        return result % (10 ** 9 + 7)