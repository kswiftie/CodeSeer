import sys

# Use 'sys.stdin.readline' for fast input
input = sys.stdin.readline

MOD = 987654103  # The modulus for hash calculation

n = int(input())  # Number of characters in the string
t = input().strip()  # The input string

# Arrays to store information about the places, boundaries, and conditions
place = []
first_pos = []
end_pos = []

# State variables
hash_state = []
current_pos = 0
group_count = 0

# Iterate over the string to calculate positions and boundaries
for i in range(n):
    char = t[i]
    if char == "0":
        if group_count:
            end_pos.append(i - 1)
            if group_count % 2 == 1:
                hash_state.append(1)
                current_pos += 1
                end_pos.append(-1)
                first_pos.append(-1)
            group_count = 0
        else:
            first_pos.append(-1)
            end_pos.append(-1)

        place.append(current_pos)
        current_pos += 1
        hash_state.append(0)
    else:
        if group_count == 0:
            first_pos.append(i)
        group_count += 1
        place.append(current_pos)

# Handle the last group if present
if group_count:
    if group_count % 2 == 1:
        hash_state.append(1)
    else:
        hash_state.append(0)
    current_pos += 1
    end_pos.append(n - 1)
    end_pos.append(-1)
    first_pos.append(-1)
place.append(current_pos)

# Prefix hashes for the states
prefix_hash = [0]
current_hash = 0
for state in hash_state:
    current_hash *= 3
    current_hash += state + 1
    current_hash %= MOD
    prefix_hash.append(current_hash)

# Number of queries
q = int(input())

# Output list to store the results
output = []


# Function to calculate hash for a substring based on the start and end indices
def compute_substring_hash(start, end):
    start_map = place[start]
    end_map = place[end]

    if t[end] == "1":
        end_map -= 1
    if hash_state[start_map] == 1:
        start_map += 1

    pre_hash = 0
    length = 0
    if start_map <= end_map:
        length = end_map - start_map + 1
        pre_hash = prefix_hash[end_map + 1]
        pre_hash -= prefix_hash[start_map] * pow(3, length, MOD)
        pre_hash %= MOD

    return pre_hash, length


# Process each query
for _ in range(q):
    l1, l2, length = map(int, input().split())
    l1 -= 1  # Convert to zero-based indexing
    l2 -= 1  # Convert to zero-based indexing

    starts = (l1, l2)
    hashes = []

    for start in starts:
        end = start + length - 1

        pre_hash, substring_length = compute_substring_hash(start, end)

        prep = app = False
        if t[start] == "1":
            last_pos = end_pos[place[start]]
            last_pos = min(last_pos, end)
            count = last_pos - start + 1
            if count % 2:
                prep = True
        if t[end] == "1":
            first_pos_val = first_pos[place[end]]
            first_pos_val = max(first_pos_val, start)
            count = end - first_pos_val + 1
            if count % 2:
                app = True

        # Adjust the hash if there are any 'prep' or 'app' conditions
        if prep:
            pre_hash += pow(3, substring_length, MOD) * 2
            substring_length += 1
        if app:
            pre_hash *= 3
            pre_hash += 2

        pre_hash %= MOD
        hashes.append(pre_hash)

    # Compare the hashes for both starts
    if hashes[0] == hashes[1]:
        output.append("Yes")
    else:
        output.append("No")

# Print all the results of the queries
print("\n".join(output))
