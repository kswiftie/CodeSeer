from collections import defaultdict


def threeSumMulti(self, arr: list[int], target: int) -> int:
    total = 0
    mod = 10 ** 9 + 7

    ones = defaultdict(int)
    twos = defaultdict(int)

    for t, v in enumerate(arr):  # O(N)
        total = (total + twos[target - v]) % mod
        for k, c in ones.items():  # O(W)
            twos[k + v] += c
        ones[v] += 1

    return total
