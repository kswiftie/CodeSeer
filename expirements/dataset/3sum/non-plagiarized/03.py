class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        output = []
        nums.sort()
        n = len(nums)

        for k in range(n):
            # Skip duplicates for the first number
            if k > 0 and nums[k] == nums[k - 1]:
                continue

            target = -nums[k]  # We want nums[i] + nums[j] = -nums[k]
            i, j = k + 1, n - 1

            while i < j:
                current_sum = nums[i] + nums[j]
                if current_sum == target:
                    output.append([nums[k], nums[i], nums[j]])
                    # Skip duplicates for the second number
                    while i < j and nums[i] == nums[i + 1]:
                        i += 1
                    # Skip duplicates for the third number
                    while i < j and nums[j] == nums[j - 1]:
                        j -= 1
                    i += 1
                    j -= 1
                elif current_sum < target:
                    i += 1
                else:
                    j -= 1

        return output