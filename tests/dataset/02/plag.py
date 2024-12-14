class CircularDeque:
    def __init__(self, max_size: int):
        """
        Initializes the circular deque with a fixed capacity.
        The deque stores values in a circular manner using a buffer.
        """
        self.buffer = [0] * max_size  # The deque's internal storage (buffer)
        self.front_index = (
            -1
        )  # Index to the front element (initialized to -1 for empty deque)
        self.rear_index = 0  # Index to the rear element
        self.capacity = max_size  # Maximum capacity of the deque

    def insert_at_front(self, value: int) -> bool:
        """
        Inserts an element at the front of the deque.
        Returns True if the operation was successful, False if the deque is full.
        """
        if self.is_full():
            return False  # Cannot insert if deque is full

        # If deque is empty, set front_index to 0
        if self.front_index == -1:
            self.front_index = 0
        else:
            # Move front index circularly (backwards)
            self.front_index = (self.front_index - 1 + self.capacity) % self.capacity

        self.buffer[self.front_index] = value  # Insert the value at the front
        return True

    def insert_at_end(self, value: int) -> bool:
        """
        Inserts an element at the end of the deque.
        Returns True if the operation was successful, False if the deque is full.
        """
        if self.is_full():
            return False  # Cannot insert if deque is full

        self.buffer[self.rear_index] = value  # Insert the value at the rear

        # Move rear index circularly (forward)
        self.rear_index = (self.rear_index + 1) % self.capacity

        # If deque was empty, set front index to 0
        if self.front_index == -1:
            self.front_index = 0

        return True

    def delete_from_front(self) -> bool:
        """
        Deletes an element from the front of the deque.
        Returns True if the operation was successful, False if the deque is empty.
        """
        if self.is_empty():
            return False  # Cannot delete if deque is empty

        # If the deque will become empty after deletion, reset front_index
        if self.front_index == self.rear_index - 1:
            self.front_index = -1
        else:
            # Move front index circularly (forward)
            self.front_index = (self.front_index + 1) % self.capacity

        return True

    def delete_from_end(self) -> bool:
        """
        Deletes an element from the end of the deque.
        Returns True if the operation was successful, False if the deque is empty.
        """
        if self.is_empty():
            return False  # Cannot delete if deque is empty

        # If there is only one element left, reset both front and rear indices
        if self.front_index == self.rear_index - 1:
            self.rear_index = 0
            self.front_index = -1
        else:
            # Move rear index circularly (backwards)
            self.rear_index = (self.rear_index - 1 + self.capacity) % self.capacity

        return True

    def get_front(self) -> int:
        """
        Retrieves the element at the front of the deque.
        Returns -1 if the deque is empty.
        """
        if self.is_empty():
            return -1  # Return -1 if deque is empty
        return self.buffer[self.front_index]  # Return the front element

    def get_rear(self) -> int:
        """
        Retrieves the element at the end of the deque.
        Returns -1 if the deque is empty.
        """
        if self.is_empty():
            return -1  # Return -1 if deque is empty
        # Access the element at rear using circular indexing
        return self.buffer[(self.rear_index - 1 + self.capacity) % self.capacity]

    def is_empty(self) -> bool:
        """
        Checks if the deque is empty.
        """
        return self.front_index == -1  # Empty if front_index is -1

    def is_full(self) -> bool:
        """
        Checks if the deque is full.
        """
        # The deque is full when rear_index equals front_index (circular condition)
        return self.front_index == self.rear_index
