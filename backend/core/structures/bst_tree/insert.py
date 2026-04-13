"""
BST insertion operations.

This module handles node insertion into binary search trees without balancing.
"""

from core.structures.node.node import Node


def _insert_node(node, new_node: Node):
    """
    Insert a new node into the binary search tree recursively.

    Maintains BST property by placing nodes in correct position based on value comparison.
    No balancing is performed.

    Args:
        node (Node): Current node in the insertion traversal
        new_node (Node): New node to be inserted

    Returns:
        None: Modifies the tree in place
    """
    if new_node.getValue() == node.getValue():
        print(f"Value {new_node.getValue()} already exists in the tree.")

    elif new_node.getValue() > node.getValue():
        if node.getRightChild() is None:
            node.setRightChild(new_node)
            new_node.setParent(node)
        else:
            _insert_node(node.getRightChild(), new_node)

    else:
        if node.getLeftChild() is None:
            node.setLeftChild(new_node)
            new_node.setParent(node)
        else:
            _insert_node(node.getLeftChild(), new_node)
