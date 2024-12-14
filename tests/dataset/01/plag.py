class CircularDeque:
    def __init__(self, max_size: int):
        # Initialize the deque with a fixed size, front and rear pointers, and capacity.
        self.buffer = [0] * max_size  # The deque's storage
        self.front_index = -1  # Front pointer
        self.rear_index = 0  # Rear pointer
        self.capacity = max_size  # The maximum size of the deque

    def insert_at_front(self, value: int) -> bool:
        # Inserts a value at the front of the deque.
        if self.is_full():
            return False  # Cannot insert if deque is full

        if self.front_index == -1:
            self.front_index = 0  # Set the front index if deque is empty
        else:
            # Move front index backwards (circularly)
            self.front_index = (self.front_index - 1 + self.capacity) % self.capacity

        self.buffer[self.front_index] = value  # Insert the value at the front
        return True

    def insert_at_end(self, value: int) -> bool:
        # Inserts a value at the end of the deque.
        if self.is_full():
            return False  # Cannot insert if deque is full

        self.buffer[self.rear_index] = value  # Insert the value at the rear
        self.rear_index = (self.rear_index + 1) % self.capacity  # Move rear index forward

        if self.front_index == -1:
            self.front_index = 0  # Set the front index if deque was empty initially

        return True

    def delete_from_front(self) -> bool:
        # Deletes an element from the front of the deque.
        if self.is_empty():
            return False  # Cannot delete if deque is empty

        # Check if the deque will be empty after deletion
        if self.front_index == self.rear_index - 1:
            self.front_index = -1  # Reset front pointer if deque becomes empty
        else:
            # Move front index forward (circularly)
            self.front_index = (self.front_index + 1) % self.capacity

        return True

    def delete_from_end(self) -> bool:
        # Deletes an element from the end of the deque.
        if self.is_empty():
            return False  # Cannot delete if deque is empty

        # If only one element is left, reset both front and rear pointers
        if self.front_index == self.rear_index - 1:
            self.rear_index = 0
            self.front_index = -1
        else:
            # Move rear index backward (circularly)
            self.rear_index = (self.rear_index - 1 + self.capacity) % self.capacity

        return True

    def get_front(self) -> int:
        # Returns the value at the front of the deque.
        if self.is_empty():
            return -1  # Return -1 if deque is empty
        return self.buffer[self.front_index]  # Return front value

    def get_rear(self) -> int:
        # Returns the value at the end of the deque.
        if self.is_empty():
            return -1  # Return -1 if deque is empty
        # Circularly access the element at rear
        return self.buffer[(self.rear_index - 1 + self.capacity) % self.capacity]

    def is_empty(self) -> bool:
        # Checks if the deque is empty.
        return self.front_index == -1

    def is_full(self) -> bool:
        # Checks if the deque is full.
        return (self.rear_index == self.front_index)
