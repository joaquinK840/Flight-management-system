"""
This module provides a function to delete a node from a binary search tree (BST).
The main function, `_delete_node`, takes a node and a value as input and deletes
the node with the specified value from the BST. The function handles three cases:
1. If the node to be deleted has no children, it simply removes the node.
2. If the node has one child, it replaces the node with its child.
3. If the node has two children, it finds the in-order successor
    (the smallest node in the right subtree), replaces the value of the node to be
    deleted with the value of the successor, and then deletes the successor node
    from the right subtree.
"""


def __min_value_node(node):
    current = node
    while current.left is not None:
        current = current.left
    return current


def __delete_one_child(node):
    if node.left is not None:
        return node.left
    return node.right


def __delete_two_children(node):
    successor = __min_value_node(node.right)
    node.value = successor.value
    node.right = _delete_node(node.right, successor.value)
    return node


def _delete_node(node, value):
    """
    Delete a node with the given value from the binary search tree.
    @param node: The current node in the tree.
    @param value: The value to be deleted.
    """
    if node is None:
        return node

    if value < node.value:
        node.left = _delete_node(node.left, value)
    elif value > node.value:
        node.right = _delete_node(node.right, value)
    else:
        if not (node.left and node.right):
            return __delete_one_child(node)

        return __delete_two_children(node)

    return node
