class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        op = []
        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            x = nums[i]
            target = -x
            left, right = i + 1, len(nums) - 1
            while left < right:
                current_sum = nums[left] + nums[right]
                if current_sum == target:
                    op.append([x, nums[left], nums[right]])
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
        return op
