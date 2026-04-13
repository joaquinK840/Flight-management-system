"""
BST deletion operations.

This module provides functions to delete nodes from a binary search tree.
Handles three deletion cases: leaf nodes, nodes with one child, and nodes with two children.
"""


def __min_value_node(node):
    """
    Find the node with minimum value in a subtree.

    Args:
        node (Node): Root of subtree to search

    Returns:
        Node: Node with minimum value
    """
    current = node
    while current.getLeftChild() is not None:
        current = current.getLeftChild()
    return current


def __delete_one_child(node):
    """
    Handle deletion of node with zero or one child.

    Args:
        node (Node): Node to delete

    Returns:
        Node or None: The child node, or None if leaf
    """
    if node.getLeftChild() is not None:
        return node.getLeftChild()
    return node.getRightChild()


def __delete_two_children(node):
    """
    Handle deletion of node with two children using successor replacement.

    Args:
        node (Node): Node to delete

    Returns:
        Node: Modified node with successor's value
    """
    successor = __min_value_node(node.getRightChild())
    node.value = successor.getValue()
    node.setRightChild(_delete_node(node.getRightChild(), successor.getValue()))
    return node


def _delete_node(node, value):
    """
    Delete a node with the given value from the binary search tree.

    Handles three cases:
    1. Leaf node: simply remove
    2. One child: replace with child
    3. Two children: replace with in-order successor

    Args:
        node (Node): Current node in traversal
        value (int): Value to delete

    Returns:
        Node or None: Modified subtree root
    """
    if node is None:
        return node

    if value < node.getValue():
        node.setLeftChild(_delete_node(node.getLeftChild(), value))
    elif value > node.getValue():
        node.setRightChild(_delete_node(node.getRightChild(), value))
    else:
        if not (node.getLeftChild() and node.getRightChild()):
            return __delete_one_child(node)
        return __delete_two_children(node)

    return node
