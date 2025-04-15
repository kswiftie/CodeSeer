class Solution:
    def find132pattern(self, nums: list[int]) -> bool:
        ## RC ##
        ## APPROACH : STACK ##
        ## LOGIC ##
        ## 1. We Create Minimum Array, till that position => O(n)
        ## 2. We start iterating from reverse of given array.
        ## 3. Remember we are using Stack and TopOfStack to determine, 2 in 132 pattern. ( so we have to check)
        ## 4. At any position, we push all elements IF greater than minimum (possible 2 in 132 pattern)
        ## 5. At any position, we pop all stack elements IF topOfStack is less or EQUAL to minimum (invalid element to form 132 pattern)
        ## 6. SATISFYING CONDITION : at any stage if min_nums[i] < stack[-1] < nums[i] we return True.

        ## TIME COMPLEXITY : O(N) ##
        ## SPACE COMPLEXITY : O(N) ##

        ## EDGE CASE : While checking the conditions 4,5,6. We should perform pop operation first i.e remove invalid elements before inserting the current element into the stack.

        if len(set(nums)) < 3:
            return False

        min_nums = [nums[0]]
        for i in range(1, len(nums)):
            min_nums.append(min(nums[i], min_nums[-1]))

        stack = []
        i = len(nums) - 1
        for i in range(len(nums) - 1, -1, -1):
            # 4
            if nums[i] > min_nums[i]:
                # 5
                while stack and stack[-1] <= min_nums[i]:
                    stack.pop()
                # 6
                if stack and min_nums[i] < stack[-1] < nums[i]:
                    return True
                # 4
                stack.append(nums[i])
        return False
