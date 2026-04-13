"""
AVL tree insertion operations.

This module handles recursive node insertion while maintaining BST ordering
and triggering balance checks for AVL rebalancing.
"""

from .balance import check_balance


def insert_node(tree, currentRoot, node):
    """
    Recursively insert a node into the AVL tree while maintaining BST property.

    Inserts the node in the correct position based on value comparison,
    sets parent-child relationships, and triggers balance checking.

    Args:
        tree (AVL): The AVL tree instance
        currentRoot (Node): Current node in the recursive traversal
        node (Node): Node to be inserted

    Returns:
        None: Modifies the tree in place
    """
    if node.getValue() == currentRoot.getValue():
        print(f"Value {node.getValue()} already exists.")

    elif node.getValue() > currentRoot.getValue():
        if currentRoot.getRightChild() is None:
            currentRoot.setRightChild(node)
            node.setParent(currentRoot)
            check_balance(tree, currentRoot)
        else:
            insert_node(tree, currentRoot.getRightChild(), node)

    else:
        if currentRoot.getLeftChild() is None:
            currentRoot.setLeftChild(node)
            node.setParent(currentRoot)
            check_balance(tree, currentRoot)
        else:
            insert_node(tree, currentRoot.getLeftChild(), node)