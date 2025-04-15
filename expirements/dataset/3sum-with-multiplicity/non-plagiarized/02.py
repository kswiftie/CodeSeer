from collections import Counter


class Solution:
    def threeSumMulti(self, arr: list[int], target: int) -> int:

        ## dictionary
        # key : distinct number
        # value : occurrence of distinct number
        counts = Counter(arr)

        # total method count, and modulo constant
        result, constant = 0, (10 ** 9 + 7)

        # find the method count where i + j + k = target
        # all numbers are bounded in interval [0, 100]

        for i in range(101):

            if counts[i] == 0:
                # number i doesn't show up in input array
                continue

            j, k = i, 100

            # find j, k with two-pointers
            while j <= k:

                if j + k > target - i:

                    # j + k is too large, try to make it smaller
                    k -= 1

                elif j + k < target - i:

                    # j + k is too small, try to make it larger
                    j += 1

                else:

                    # update result with different combination cases

                    if i == j == k:

                        # all repeated: (i, j, k) = (i, i, i)
                        result += counts[i] * (counts[i] - 1) * (counts[i] - 2) // 6

                    elif i == j:
                        # i, j repeated: (i, j, k) = (i, i, k)
                        result += counts[i] * (counts[i] - 1) * counts[k] // 2

                    elif j == k:
                        # i, k repeated: (i, j, k) = (i, j, j)
                        result += counts[i] * counts[j] * (counts[j] - 1) // 2

                    else:
                        # all distinct: (i, j, k)
                        result += counts[i] * counts[j] * counts[k]

                    # update two pointers for j, k
                    j += 1
                    k -= 1

        return result % constant
