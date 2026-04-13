"""
AVL tree deletion operations.

This module handles node deletion while maintaining AVL balance.
Supports three deletion cases: leaf nodes, nodes with one child, and nodes with two children.
"""

from .balance import check_balance
from .search import search_node


def __identifyDeletionCase(node):
    """
    Identify the deletion case for a node.

    Returns:
        int: 1 for leaf node, 2 for one child, 3 for two children
    """
    if node.getLeftChild() is None and node.getRightChild() is None:
        return 1
    elif node.getLeftChild() is not None and node.getRightChild() is not None:
        return 3
    else:
        return 2


def __deleteLeafNode(tree, node):
    """
    Delete a leaf node and rebalance from its parent.

    Args:
        tree (AVL): The AVL tree instance
        node (Node): Leaf node to delete
    """
    parent = node.getParent()
    if parent is None:
        tree.root = None
    else:
        if parent.getLeftChild() == node:
            parent.setLeftChild(None)
        else:
            parent.setRightChild(None)
        node.setParent(None)
    check_balance(tree, parent)


def __deleteNodeWithOneChild(tree, node):
    """
    Delete a node with a single child and reconnect the subtree.

    Args:
        tree (AVL): The AVL tree instance
        node (Node): Node with one child to delete
    """
    parent = node.getParent()
    child = node.getLeftChild() if node.getLeftChild() else node.getRightChild()
    if parent is None:
        tree.root = child
        child.setParent(None)
    else:
        if parent.getLeftChild() == node:
            parent.setLeftChild(child)
        else:
            parent.setRightChild(child)
        child.setParent(parent)
    node.setParent(None)
    check_balance(tree, parent)


def __deleteNodeWithTwoChildren(tree, node):
    """
    Delete a node with two children using its in-order successor.

    Finds the minimum node in the right subtree (successor), copies its
    value and data to the node being deleted, then deletes the successor.

    Args:
        tree (AVL): The AVL tree instance
        node (Node): Node with two children to delete
    """
    # Find successor (minimum of right subtree)
    successor = node.getRightChild()
    while successor.getLeftChild() is not None:
        successor = successor.getLeftChild()
    # Copy successor's value and data to node being deleted
    node.value = successor.getValue()
    node.setDatos(successor.getDatos())
    # Delete successor (which has at most one right child)
    if successor.getRightChild() is not None:
        __deleteNodeWithOneChild(tree, successor)
    else:
        __deleteLeafNode(tree, successor)


def __delete(tree, node):
    """
    Dispatch deletion logic based on the node case.

    Args:
        tree (AVL): The AVL tree instance
        node (Node): Node to delete
    """
    case = __identifyDeletionCase(node)
    if case == 1:
        __deleteLeafNode(tree, node)
    elif case == 2:
        __deleteNodeWithOneChild(tree, node)
    elif case == 3:
        __deleteNodeWithTwoChildren(tree, node)


def delete(tree, value):
    """
    Public interface to delete a node by value.

    Handles the three classic BST deletion cases while maintaining AVL balance.

    Args:
        tree (AVL): The AVL tree instance
        value (int): Value to delete

    Raises:
        Exception: If value is not found in the tree
    """
    node = search_node(tree.root, value)
    if node is None:
        raise Exception(f"Value {value} not found in the tree")
    __delete(tree, node)