class MyCircularDeque:
    def __init__(self, k: int):
        self.buffer = [0] * k
        self.front = -1
        self.rear = 0
        self.capacity = k

    def insertFront(self, value: int) -> bool:

        if self.isFull():
            return False

        if self.front == -1:

            self.front = 0

        else:

            self.front = (self.front - 1 + self.capacity) % self.capacity

        self.buffer[self.front] = value

        return True

    def insertLast(self, value: int) -> bool:

        if self.isFull():
            return False

        self.buffer[self.rear] = value

        self.rear = (self.rear + 1) % self.capacity

        if self.front == -1:
            self.front = 0

        return True

    def deleteFront(self) -> bool:

        if self.isEmpty():
            return False

        if self.front == self.rear - 1:

            self.front = -1

        else:

            self.front = (self.front + 1) % self.capacity

        return True

    def deleteLast(self) -> bool:

        if self.isEmpty():
            return False

        if self.front == self.rear - 1:

            self.rear = 0

            self.front = -1

        else:

            self.rear = (self.rear - 1 + self.capacity) % self.capacity

        return True

    def getFront(self) -> int:

        if self.isEmpty():
            return -1

        return self.buffer[self.front]

    def getRear(self) -> int:

        if self.isEmpty():
            return -1

        return self.buffer[(self.rear - 1 + self.capacity) % self.capacity]

    def isEmpty(self) -> bool:

        return self.front == -1

    def isFull(self) -> bool:

        return self.front == self.rear
