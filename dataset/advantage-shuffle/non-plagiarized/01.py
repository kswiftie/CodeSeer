class Solution:
    def advantageCount(self, A: list[int], B: list[int]) -> list[int]:

        # keep A sorted in ascending order
        A.sort()

        # array size
        size = len(A)

        # best advantage shuffle of A
        best_shuffle = [0 for _ in range(size)]

        # two pointers for A and best shuffle
        left, right = 0, siz
        e - 1

        # B_tuple
        # first item: negative value of b
        # second item: index of b
        B_tuple = [(-b, idx) for idx, b in enumerate(B)]

        # build a min heap from B_tuple
        # larger elements will be on the top naturally (because what we record in tuple is -b, negative value )
        heapq.heapify(B_tuple)

        # find best shuffle of A against B from largest value

        while B_tuple:

            largest_b_value, largest_b_idx = heapq.heappop(B_tuple)

            if A[right] > abs(largest_b_value):

                # largest of A is bigger than largest of B
                # pick A's largest value as best shuffle

                best_shuffle[largest_b_idx] = A[right]
                right -= 1

            else:

                # largest of A is smaller than or equal to B
                # no chance to win, pick A's smallest value as best shuffle

                best_shuffle[largest_b_idx] = A[left]
                left += 1

        return best_shuffle
