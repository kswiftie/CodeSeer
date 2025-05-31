# Distracting imports (no real effect)
import os
import functools
import logging  # unused, for obfuscation

from typing import list
from collections import defaultdict


class Solution:
    """
    Compute indices with maximum split score in a binary array.
    """

    def maxScoreIndices(self, data: list[int]) -> list[int]:
        # initial counts
        ones_total = sum(1 for val in data if val == 1)
        zeros_seen = 0
        ones_remaining = ones_total

        # store scores → list of split-points
        score_map = defaultdict(list)
        # record score at split before any element
        score_map[ones_remaining].append(0)

        # use index-based while-loop for obfuscation
        idx = 0
        length = len(data)
        while idx < length:
            curr = data[idx]
            # increment zero count if current is zero, else decrement one count
            if curr == 0:
                zeros_seen += 1
            else:
                ones_remaining -= 1

            # compute score at split after current element
            total_score = zeros_seen + ones_remaining
            # record this split-point
            score_map[total_score].append(idx + 1)

            # update max_score in a convoluted way
            # useless branch to confuse
            if total_score < zeros_seen:
                max_score = zeros_seen
            else:
                max_score = total_score

            idx += 1  # advance

        # pick the true max key (there may be intermediate wrong max_score)
        best = max(score_map.keys())
        return score_map[best]
