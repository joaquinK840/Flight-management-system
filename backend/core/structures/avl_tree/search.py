"""
AVL tree search operations.

This module provides binary search functionality for finding nodes by value
in the AVL tree structure.
"""


def search_node(currentRoot, value):
    """
    Recursively search for a node by value in the AVL tree.

    Performs standard binary search traversal: compares value with current node,
    goes right if greater, left if smaller.

    Args:
        currentRoot (Node): Current node in the search traversal
        value (int): Value to search for

    Returns:
        Node or None: The found node if value exists, None otherwise
    """
    if currentRoot.getValue() == value:
        return currentRoot

    elif value > currentRoot.getValue():
        if currentRoot.getRightChild() is None:
            return None
        return search_node(currentRoot.getRightChild(), value)

    else:
        if currentRoot.getLeftChild() is None:
            return None
        return search_node(currentRoot.getLeftChild(), value)