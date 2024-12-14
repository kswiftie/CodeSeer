class Node:
    def __init__(self, value=0, next_node=None):
        """
        Node represents an individual element in the linked list.
        Each node stores a value and a reference to the next node.
        """
        self.value = value  # The value held by this node.
        self.next_node = next_node  # The next node in the list.


class MyLinkedList:
    def __init__(self):
        """
        MyLinkedList is a simple singly linked list that supports adding, getting, and deleting nodes.
        """
        self.head = None  # The head node of the list (start of the list).
        self.size = 0  # Size of the linked list.

    def get(self, index: int) -> int:
        """
        Retrieves the value of the node at the specified index. Returns -1 if the index is invalid.
        """
        if index < 0 or index >= self.size:
            return -1  # Invalid index, return -1

        current_node = self.head  # Start from the head of the list.

        # Traverse to the desired node by moving along the list.
        for _ in range(index):
            current_node = current_node.next_node

        return current_node.value  # Return the value of the found node.

    def addAtHead(self, value: int) -> None:
        """
        Adds a node with the specified value at the beginning of the linked list.
        """
        new_node = Node(
            value, self.head
        )  # Create a new node pointing to the current head.
        self.head = new_node  # Update the head to the new node.
        self.size += 1  # Increase the size of the list.

    def addAtTail(self, value: int) -> None:
        """
        Adds a node with the specified value at the end of the linked list.
        """
        if self.size == 0:
            # If the list is empty, add at the head.
            self.addAtHead(value)
        else:
            current_node = self.head  # Start from the head.

            # Traverse to the last node in the list.
            while current_node.next_node:
                current_node = current_node.next_node

            current_node.next_node = Node(
                value
            )  # Create a new node and add it as the next node.
            self.size += 1  # Increase the size of the list.

    def addAtIndex(self, index: int, value: int) -> None:
        """
        Adds a node with the specified value at the given index. If index is invalid, do nothing.
        """
        if index < 0 or index > self.size:
            return  # Index is out of bounds, do nothing.

        if index == 0:
            # If index is 0, add at the head.
            self.addAtHead(value)
        else:
            current_node = self.head  # Start from the head.

            # Traverse to the node just before the index position.
            for _ in range(index - 1):
                current_node = current_node.next_node

            # Insert the new node at the correct position.
            new_node = Node(value, current_node.next_node)  # Create the new node.
            current_node.next_node = new_node  # Link the previous node to the new node.
            self.size += 1  # Increase the size of the list.

    def deleteAtIndex(self, index: int) -> None:
        """
        Deletes the node at the given index. If the index is invalid, do nothing.
        """
        if index < 0 or index >= self.size:
            return  # Index is out of bounds, do nothing.

        if index == 0:
            # If index is 0, remove the head node.
            self.head = self.head.next_node
        else:
            current_node = self.head  # Start from the head.

            # Traverse to the node just before the node to be deleted.
            for _ in range(index - 1):
                current_node = current_node.next_node

            # Delete the node by skipping it in the list.
            current_node.next_node = current_node.next_node.next_node

        self.size -= 1  # Decrease the size of the list.
