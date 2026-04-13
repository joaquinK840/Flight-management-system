"""
BST search operations.

This module provides binary search functionality for BST trees.
"""


def _search_node(node, value):
    """
    Search for a node with the given value in the binary search tree.

    Performs recursive binary search traversal.

    Args:
        node (Node): Current node in the search traversal
        value (int): The value to search for

    Returns:
        Node or None: The node with the specified value, or None if not found
    """
    if node is None:
        return None

    if node.getValue() == value:
        return node

    if value > node.getValue():
        return _search_node(node.getRightChild(), value)

    return _search_node(node.getLeftChild(), value)
