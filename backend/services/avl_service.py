"""
AVL tree service for managing tree operations.

Provides a unified interface for AVL and BST tree operations including
insertion, search, deletion, and serialization.
"""

from core.structures.avl_tree.tree import AVL
from core.structures.bst_tree.tree import BST
from core.structures.node.node import Node
from services.serialize_tree import serialize_tree


class TreeService:
    """
    Service class for managing AVL and BST tree operations.

    Provides methods for inserting, searching, deleting nodes and
    serializing tree structures.
    """

    def __init__(self, avl=None, bst=None):
        """
        Initialize the tree service.

        Args:
            avl: AVL tree instance (optional, creates new if not provided)
            bst: BST tree instance (optional, creates new if not provided)
        """
        self.avl = avl or AVL()
        self.bst = bst or BST()

    def set_trees(self, avl, bst):
        """
        Set the AVL and BST tree instances.

        Args:
            avl: AVL tree instance
            bst: BST tree instance
        """

    def insert_node(self, value: int):
        """
        Insert a node with the given value into the AVL tree.

        Args:
            value (int): Value to insert

        Returns:
            dict: Dictionary containing insertion result with message, root value, and serialized tree
        """

    def get_tree(self):
        """
        Get the current AVL tree structure.

        Returns:
            dict: Dictionary containing the serialized tree
        """

    def search_value(self, value: int):
        """
        Search for a value in the AVL tree.

        Args:
            value (int): Value to search for

        Returns:
            dict: Dictionary indicating if value was found and the value itself
        """

    def cancel_value(self, value: int):
        """
        Cancel (remove) a value from the AVL tree.

        Args:
            value (int): Value to cancel

        Returns:
            dict: Dictionary with cancellation result and updated tree
        """

    def delete_value(self, value: int):
        """
        Delete a value from the AVL tree.

        Args:
            value (int): Value to delete

        Returns:
            dict: Dictionary with deletion result and updated tree
        """

    def reset_tree(self):
        """
        Reset both AVL and BST trees to empty state.

        Returns:
            dict: Dictionary with reset confirmation message
        """

# Singleton instance to persist tree state across requests if not using a DB
tree_service = TreeService()
