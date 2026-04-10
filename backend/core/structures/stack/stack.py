class Stack:
    """
    Stack implementation using a list.
    """

    def __init__(self):
        self.items = []

    def is_empty(self):
        """
        Check if the stack is empty.
        """
        return len(self.items) == 0

    def push(self, item):
        """
        Add an item to the top of the stack.
        """
        self.items.append(item)

    def pop(self):
        """
        Remove and return the item from the top of the stack.
        """
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self.items.pop()

    def peek(self):
        """
        Return the item at the top of the stack without removing it.
        """
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self.items[-1]

    def size(self):
        """
        Return the number of items in the stack.
        """
        return len(self.items)

    def clear(self):
        """
        Clear all items from the stack.
        """
        self.items = []