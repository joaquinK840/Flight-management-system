"""
Queue data structure (FIFO - First In First Out).

This module implements a FIFO queue used for managing pending flights
in concurrent processing scenarios.
"""

class Queue:
    """Simple FIFO queue data structure."""

    def __init__(self):
        """Initialize an empty queue."""
        self.items = []

    def enqueue(self, item):
        """
        Add an element to the end of the queue.

        Args:
            item: Element to add (typically flight data dict)
        """
        self.items.append(item)

    def dequeue(self):
        """
        Remove and return the first element from the queue.

        Returns:
            The front element

        Raises:
            IndexError: If the queue is empty
        """
        if len(self.items) == 0:
            raise IndexError("Queue is empty")
        return self.items.pop(0)

    def peek(self):
        """
        View the first element without removing it.

        Returns:
            The front element

        Raises:
            IndexError: If the queue is empty
        """
        if len(self.items) == 0:
            raise IndexError("Queue is empty")
        return self.items[0]

    def is_empty(self):
        """
        Check if the queue is empty.

        Returns:
            bool: True if empty, False otherwise
        """
        return len(self.items) == 0

    def size(self):
        """
        Get the number of elements in the queue.

        Returns:
            int: Number of elements
        """
        return len(self.items)

    def clear(self):
        """Clear all elements from the queue."""
        self.items = []

    def get_all(self):
        """
        Get a copy of all elements without modifying the queue.

        Returns:
            list: Copy of all elements in the queue
        """
        return self.items.copy()
