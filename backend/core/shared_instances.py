"""
Global configuration and shared singleton instances across routes.

This module provides shared instances of AVL tree, BST tree, flight queue,
and a singleton TreeRepository for managing tree operations across the application.
"""

from core.structures.avl_tree.tree import AVL
from core.structures.bst_tree.bst import BST
from core.structures.queue.queue import Queue
from services.tree_repository import TreeRepository

# Global shared instances
avl = AVL()
bst = BST()
flight_queue = Queue()


class SharedTreeRepository(TreeRepository):
    """
    Singleton repository using shared tree instances.

    This class implements the singleton pattern to ensure only one instance
    of the tree repository exists, managing undo/redo operations for the shared AVL tree.
    """

    _instance = None

    def __new__(cls):
        """
        Create or return the singleton instance.

        Returns:
            SharedTreeRepository: The single shared instance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.tree = avl
            cls._instance.use_bst = False
            # Initialize undo/redo stacks
            from core.structures.stack.stack import Stack
            cls._instance.undo_stack = Stack()
            cls._instance.redo_stack = Stack()
        return cls._instance


# Global singleton instance
flight_repository = SharedTreeRepository()