"""
AVL tree traversal algorithms.

This module provides different tree traversal methods: in-order, breadth-first,
pre-order, and post-order traversals.
"""

from collections import deque


def in_order(node):
    """
    Perform in-order traversal of the tree (left, root, right).

    Args:
        node (Node): Root node of the subtree to traverse

    Returns:
        list: List of node values in in-order
    """
    result = []

    def _in_order(n):
        if n is None:
            return
        _in_order(n.getLeftChild())
        result.append(n.getValue())
        _in_order(n.getRightChild())

    _in_order(node)
    return result


def breadth_first_traversal(node):
    """
    Perform breadth-first traversal (level-order) of the tree.

    Args:
        node (Node): Root node of the subtree to traverse

    Returns:
        list: List of node values in BFS order
    """
    if node is None:
        return []

    result = []
    queue = deque([node])

    while queue:
        current = queue.popleft()
        result.append(current.getValue())

        if current.getLeftChild() is not None:
            queue.append(current.getLeftChild())
        if current.getRightChild() is not None:
            queue.append(current.getRightChild())

    return result


def pre_order(node):
    """
    Perform pre-order traversal of the tree (root, left, right).

    Args:
        node (Node): Root node of the subtree to traverse

    Returns:
        list: List of node values in pre-order
    """
    result = []

    def _pre_order(n):
        if n is None:
            return
        result.append(n.getValue())
        _pre_order(n.getLeftChild())
        _pre_order(n.getRightChild())

    _pre_order(node)
    return result


def post_order(node):
    """
    Perform post-order traversal of the tree (left, right, root).

    Args:
        node (Node): Root node of the subtree to traverse

    Returns:
        list: List of node values in post-order
    """
    result = []

    def _post_order(n):
        if n is None:
            return
        _post_order(n.getLeftChild())
        _post_order(n.getRightChild())
        result.append(n.getValue())

    _post_order(node)
    return result