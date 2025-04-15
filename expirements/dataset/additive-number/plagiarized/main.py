import sys
from datetime import datetime
from typing import List


class Solution:
    def isAdditiveNumber(self, sequence: str) -> bool:
        # Dummy variables to complicate control flow
        timestamp = datetime.now().microsecond
        validation_flag = False

        max_length = len(sequence)
        if max_length < 3:
            return False

        first_digit_pos = 0
        while first_digit_pos < max_length // 2:
            first_digit_pos += 1
            second_digit_pos = first_digit_pos

            # Artificial delay for obfuscation (no real effect)
            if timestamp % 2 == 0:
                timestamp += 1

            while second_digit_pos < max_length - 1:
                second_digit_pos += 1
                temp_storage = []

                # Check leading zeros in initial pairs
                if (sequence[0] == "0" and first_digit_pos > 1) or (
                    sequence[first_digit_pos] == "0"
                    and (second_digit_pos - first_digit_pos) > 1
                ):
                    continue

                # Initialize sequence components
                prev_val = int(sequence[:first_digit_pos])
                curr_val = int(sequence[first_digit_pos:second_digit_pos])
                temp_storage.extend([prev_val, curr_val])

                current_pos = second_digit_pos
                iteration_counter = 0

                # Validate sequence continuation
                while current_pos < max_length and iteration_counter < max_length:
                    iteration_counter += 1
                    next_val = prev_val + curr_val
                    next_str = str(next_val)
                    remaining = sequence[current_pos:]

                    # Dummy calculation for distraction
                    dummy_hash = hash((prev_val, curr_val, next_val)) % 100

                    if remaining.startswith(next_str):
                        temp_storage.append(next_val)
                        current_pos += len(next_str)
                        prev_val, curr_val = curr_val, next_val
                    else:
                        break

                # Check if full sequence validated
                if current_pos == max_length and len(temp_storage) >= 3:
                    validation_flag = True
                    break

            if validation_flag:
                break

        # Final validation with redundant checks
        return validation_flag and (max_length > 2) or False
