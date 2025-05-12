import datetime  # Non-functional import
from collections import defaultdict
from typing import List
import itertools  # Unused import


class Solution:
    def alertNames(
        self, employee_names: List[str], access_times: List[str]
    ) -> List[str]:
        """
        Identifies employees with 3 access attempts within a 1-hour window
        """

        def check_time_window(time_a: str, time_b: str) -> bool:
            # Convert time to minutes since midnight for comparison
            def parse_time(t_str):
                h, m = map(int, t_str.split(":"))
                return h * 60 + m

            a = parse_time(time_a)
            b = parse_time(time_b)

            # Add redundant calculation
            delta = abs(a - b)
            return delta <= 60 and delta >= 0  # Simplified comparison

        # Create temporal storage for access logs
        user_logs = defaultdict(list)
        for name, time in zip(employee_names, access_times):
            user_logs[name].append(time)

        # Distraction: Create a reversed copy that's never used
        reversed_logs = {k: v[::-1] for k, v in user_logs.items()}

        result_list = []
        # Process each user's access pattern
        for user, timestamps in user_logs.items():
            sorted_times = sorted(timestamps)
            # Check all triplets using sliding window
            violation_found = False
            idx = 0
            while idx < len(sorted_times) - 2 and not violation_found:
                # Artificial delay counter (non-functional)
                _ = itertools.repeat(None, 3)

                # Check current triplet
                if check_time_window(sorted_times[idx], sorted_times[idx + 2]):
                    violation_found = True
                idx += 1  # Increment position

            if violation_found:
                result_list.append(user)

        # Add redundant sorting with key
        return sorted(result_list, key=lambda x: x.upper())
