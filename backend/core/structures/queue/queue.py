class Queue:
    """
    Queue implementation using a list.
    """

    def __init__(self):
        self.items = []

    def is_empty(self):
        """
        Check if the queue is empty.
        """
        return len(self.items) == 0

    def enqueue(self, item):
        """
        Add an item to the end of the queue.
        """
        self.items.append(item)

    def dequeue(self):
        """
        Remove and return the item from the front of the queue.
        """
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self.items.pop(0)

    def peek(self):
        """
        Return the item at the front of the queue without removing it.
        """
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self.items[0]

    def size(self):
        """
        Return the number of items in the queue.
        """
        return len(self.items)

    def clear(self):
        """
        Clear all items from the queue.
        """
        self.items = []