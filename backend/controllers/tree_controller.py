"""
Tree controller for basic AVL operations.

This module provides a simple controller that delegates operations
to the AVL service layer.
"""

from services.avl_service import tree_service


class TreeController:
    """
    Controller for basic tree operations.

    Acts as a thin wrapper around the AVL service, providing
    a simple interface for tree manipulation.
    """

    def insert_value(self, value: int):
        """
        Insert a value into the tree.

        Args:
            value (int): Value to insert

        Returns:
            dict: Insertion result from service
        """
        return tree_service.insert_node(value)

    def get_tree(self):
        """
        Get the current tree state.

        Returns:
            dict: Serialized tree data
        """
        return tree_service.get_tree()

    def search_value(self, value: int):
        """
        Search for a value in the tree.

        Args:
            value (int): Value to search for

        Returns:
            dict: Search result
        """
        return tree_service.search_value(value)

    def cancel_value(self, value: int):
        """
        Cancel (delete subtree) for a value.

        Args:
            value (int): Root value of subtree to cancel

        Returns:
            dict: Cancellation result
        """
        return tree_service.cancel_value(value)

    def delete_value(self, value: int):
        """
        Delete a single node by value.

        Args:
            value (int): Value to delete

        Returns:
            dict: Deletion result
        """
        return tree_service.delete_value(value)

    def reset_tree(self):
        """
        Reset the tree to empty state.

        Returns:
            dict: Reset confirmation
        """
        return tree_service.reset_tree()


# Global controller instance
tree_controller = TreeController()
