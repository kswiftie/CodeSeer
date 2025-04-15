from typing import List  # Importing List for type hinting


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        result = []  # Initialize the result list
        nums.sort()  # Sort the input list

        # Iterate through the sorted list
        for index in range(len(nums)):
            # Skip duplicate values
            if index > 0 and nums[index] == nums[index - 1]:
                continue  # Skip the same element to avoid duplicates

            left = index + 1  # Initialize left pointer
            right = len(nums) - 1  # Initialize right pointer

            # Use two pointers to find the triplets
            while left < right:
                current_sum = (
                    nums[index] + nums[left] + nums[right]
                )  # Calculate the sum

                if current_sum > 0:  # If the sum is greater than zero
                    right -= 1  # Move the right pointer left
                elif current_sum < 0:  # If the sum is less than zero
                    left += 1  # Move the left pointer right
                else:  # If the sum is zero
                    result.append(
                        [nums[index], nums[left], nums[right]]
                    )  # Add the triplet to the result
                    left += 1  # Move the left pointer right

                    # Skip duplicates for the left pointer
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1  # Move left pointer to the next unique element

        return result  # Return the list of triplets
