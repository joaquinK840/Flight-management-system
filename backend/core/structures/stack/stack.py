"""
Stack data structure (LIFO - Last In First Out).

This module implements a stack used for undo functionality in the tree repository.
"""

class Stack:
    """
    LIFO stack data structure.

    Used to implement undo/redo stacks in the tree repository for managing
    tree state history.
    """

    def __init__(self):
        """Initialize an empty stack."""
        self.items = []

    def push(self, item):
        """
        Add an element to the top of the stack.

        Args:
            item: Element to add (any type)
        """
        self.items.append(item)

    def pop(self):
        """
        Remove and return the top element from the stack.

        Returns:
            The top element

        Raises:
            IndexError: If the stack is empty
        """
        if len(self.items) == 0:
            raise IndexError("Pop from empty stack")
        return self.items.pop()

    def peek(self):
        """
        Return the top element without removing it.

        Returns:
            The top element or None if stack is empty
        """
        if len(self.items) == 0:
            return None
        return self.items[-1]

    def is_empty(self):
        """
        Check if the stack is empty.

        Returns:
            bool: True if no elements, False otherwise
        """
        return len(self.items) == 0

    def size(self):
        """
        Return the number of elements in the stack.

        Returns:
            int: Number of elements
        """
        return len(self.items)

    def clear(self):
        """Clear all elements from the stack."""
        self.items = []

    def __str__(self):
        """String representation of the stack."""
        return f"Stack({self.items})"

    def __repr__(self):
        """String representation for debugging."""
        return self.__str__()
