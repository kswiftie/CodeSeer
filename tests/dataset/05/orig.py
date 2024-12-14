class Node:

    def __init__(self, val=0, next=None):

        self.val = val

        self.next = next



class MyLinkedList:

    def __init__(self):

        self.head = None

        self.size = 0



    def get(self, index: int) -> int:

        if index < 0 or index >= self.size:

            return -1

        cur = self.head

        for _ in range(index):

            cur = cur.next

        return cur.val



    def addAtHead(self, val: int) -> None:

        self.head = Node(val, self.head)

        self.size += 1



    def addAtTail(self, val: int) -> None:

        if self.size == 0:

            self.addAtHead(val)

        else:

            cur = self.head

            while cur.next:

                cur = cur.next

            cur.next = Node(val)

            self.size += 1



    def addAtIndex(self, index: int, val: int) -> None:

        if index < 0 or index > self.size:

            return

        if index == 0:

            self.addAtHead(val)

        else:

            cur = self.head

            for _ in range(index - 1):

                cur = cur.next

            cur.next = Node(val, cur.next)

            self.size += 1



    def deleteAtIndex(self, index: int) -> None:

        if index < 0 or index >= self.size:

            return

        if index == 0:

            self.head = self.head.next

        else:

            cur = self.head

            for _ in range(index - 1):

                cur = cur.next

            cur.next = cur.next.next

        self.size -= 1

