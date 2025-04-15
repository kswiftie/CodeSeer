from collections import deque
from typing import List  # Importing List for type hinting


class Solution:
    def updateMatrix(self, matrix: List[List[int]]) -> List[List[int]]:
        # Check if the matrix is empty
        if not matrix or not matrix[0]:
            return []  # Return an empty list if the matrix is invalid

        rows, cols = len(matrix), len(matrix[0])  # Get dimensions of the matrix
        queue = deque()  # Initialize a queue
        MAX_DIST = rows * cols  # Define a maximum distance value

        # Populate the queue with all 0s and set 1s to MAX_DIST
        for x in range(rows):
            for y in range(cols):
                if matrix[x][y] == 0:
                    queue.append((x, y))  # Add coordinates of 0s to the queue
                else:
                    matrix[x][y] = MAX_DIST  # Set 1s to MAX_DIST

        # Define possible directions for movement
        move_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # Process the queue until it's empty
        while queue:
            current_row, current_col = queue.popleft()  # Get the front of the queue
            for delta_row, delta_col in move_directions:
                new_row, new_col = current_row + delta_row, current_col + delta_col  # Calculate new position
                # Check if the new position is valid and update if necessary
                if 0 <= new_row < rows and 0 <= new_col < cols and matrix[new_row][new_col] > matrix[current_row][
                    current_col] + 1:
                    queue.append((new_row, new_col))  # Add new position to the queue
                    matrix[new_row][new_col] = matrix[current_row][current_col] + 1  # Update distance

        # Return the updated matrix
        return matrix  # Final result
