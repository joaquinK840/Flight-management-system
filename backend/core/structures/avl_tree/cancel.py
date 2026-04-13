"""
AVL tree subtree cancellation operations.

This module provides functionality to cancel (delete) entire subtrees
rooted at a specific node, useful for mass flight cancellations.
"""

from .balance import check_balance
from .search import search_node


def __cancel(tree, node):
    """
    Cancel (delete) the entire subtree rooted at the given node.

    Disconnects the subtree from its parent and triggers rebalancing.

    Args:
        tree (AVL): The AVL tree instance
        node (Node): Root of the subtree to cancel
    """
    parent = node.getParent()

    if parent is not None:
        if parent.getLeftChild() == node:
            parent.setLeftChild(None)
        else:
            parent.setRightChild(None)
        check_balance(tree, parent)
    else:
        tree.root = None


def cancel(tree, value):
    """
    Cancel a subtree by finding the node with the given value.

    Args:
        tree (AVL): The AVL tree instance
        value (int): Value of the node whose subtree should be cancelled

    Raises:
        Exception: If value is not found in the tree
    """
    node = search_node(tree.root, value)
    if node is None:
        raise Exception(f"Value {value} not found in the tree")
    __cancel(tree, node)