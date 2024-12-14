import sys

# Set input method to read from stdin
input = sys.stdin.readline

# Read n (number of elements) and m (number of queries)
num_elements, num_queries = map(int, input().split())

# Read the list p, which contains the jump lengths for each element
jump_lengths = list(map(int, input().split()))

# Define a constant for the block size
BLOCK_SIZE = 410

# Create block indices for each element based on its position
block_indices = [i // BLOCK_SIZE for i in range(num_elements)]

# Initialize lists for storing jump results and the end positions for each element
jumps = [0] * num_elements
end_positions = [0] * num_elements

# Compute the jumps and end positions in reverse order
for idx in range(num_elements - 1, -1, -1):
    next_position = idx + jump_lengths[idx]

    if next_position >= num_elements:
        # If the next position is beyond the last element
        jumps[idx] = 1
        end_positions[idx] = idx + num_elements
    elif block_indices[next_position] > block_indices[idx]:
        # If the next element is in a higher block
        jumps[idx] = 1
        end_positions[idx] = next_position
    else:
        # Otherwise, use the precomputed jumps from the next position
        jumps[idx] = jumps[next_position] + 1
        end_positions[idx] = end_positions[next_position]

# Store results of the queries
output = []

# Process each query
for _ in range(num_queries):
    query = input().strip()

    if query[0] == '0':
        # Update query: update the jump length for an element
        _, index_str, new_jump_str = query.split()
        index = int(index_str) - 1  # Convert to zero-based index
        new_jump = int(new_jump_str)

        # Update the jump length
        jump_lengths[index] = new_jump

        # Recalculate jumps and end positions for the modified block
        curr_idx = index
        while curr_idx >= 0 and block_indices[curr_idx] == block_indices[index]:
            next_position = curr_idx + jump_lengths[curr_idx]

            if next_position >= num_elements:
                jumps[curr_idx] = 1
                end_positions[curr_idx] = curr_idx + num_elements
            elif block_indices[next_position] > block_indices[curr_idx]:
                jumps[curr_idx] = 1
                end_positions[curr_idx] = next_position
            else:
                jumps[curr_idx] = jumps[next_position] + 1
                end_positions[curr_idx] = end_positions[next_position]

            curr_idx -= 1

    else:
        # Query to find the number of jumps and final position
        _, start_str = query.split()
        curr_idx = int(start_str) - 1  # Convert to zero-based index

        total_jumps = 0
        while curr_idx < num_elements:
            total_jumps += jumps[curr_idx]
            curr_idx = end_positions[curr_idx]

        # The final position is adjusted by subtracting n to get a valid result
        output.append(f'{curr_idx - num_elements + 1} {total_jumps}')

# Output all the results for the queries
print('\n'.join(output))
