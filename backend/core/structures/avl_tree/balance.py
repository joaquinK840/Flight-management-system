"""
AVL tree balance factor calculations and rebalancing operations.

This module provides functions to calculate balance factors, determine rotation cases,
and perform rebalancing operations to maintain AVL tree properties.
"""

from .rotations import rotate_left, rotate_right


def get_height(node):
    """
    Get the height of a node in O(1).

    Args:
        node (Node): Tree node

    Returns:
        int: Node height (0 if None)
    """
    if node is None:
        return 0
    return node.getHeight()


def update_height(node):
    """
    Update node height based on its children's heights in O(1).

    Should be called after any structural change to the tree.

    Args:
        node (Node): Node to update
    """
    if node is None:
        return

    left_height = get_height(node.getLeftChild())
    right_height = get_height(node.getRightChild())
    node.setHeight(1 + max(left_height, right_height))


def get_balance_factor(node):
    """
    Compute the balance factor of a node in O(1).

    Positive values indicate left-heavy, negative indicate right-heavy.

    Args:
        node (Node): Node to evaluate

    Returns:
        int: Balance factor (left_height - right_height)
    """
    if node is None:
        return 0

    left_height = get_height(node.getLeftChild())
    right_height = get_height(node.getRightChild())
    return left_height - right_height


def get_balance_case(node, bf):
    """
    Determine the type of imbalance that requires rotation.

    Args:
        node (Node): Imbalanced node
        bf (int): Balance factor of the node

    Returns:
        str or None: "LL", "RR", "LR", "RL" or None if balanced
    """
    if bf > 1:
        if get_balance_factor(node.getLeftChild()) >= 0:
            return "LL"
        else:
            return "LR"

    if bf < -1:
        if get_balance_factor(node.getRightChild()) <= 0:
            return "RR"
        else:
            return "RL"

    return None


def check_balance(tree, node):
    """
    Check and restore AVL balance from the given node up to the root.

    Handles four rotation cases:
    - LL: Left-left heavy, single right rotation
    - RR: Right-right heavy, single left rotation
    - LR: Left-right heavy, left rotation on child then right on node
    - RL: Right-left heavy, right rotation on child then left on node

    When tree.stress_mode is True, only updates heights without rotations.

    Args:
        tree (AVL): The AVL tree instance
        node (Node): Starting node for balance check (travels up to root)
    """
    while node is not None:
        # Update current node height
        update_height(node)

        # Calculate balance factor
        bf = get_balance_factor(node)

        # In stress mode, only update heights and continue up
        if tree.stress_mode:
            node = node.getParent()
            continue

        # LEFT HEAVY (bf > 1)
        if bf > 1:
            left_bf = get_balance_factor(node.getLeftChild())

            if left_bf >= 0:
                # LL case: single right rotation
                tree.rotation_counts["LL"] += 1
                rotate_right(tree, node)
                # Update heights after rotation
                update_height(node)
                update_height(node.getParent())
            else:
                # LR case: left-right double rotation
                tree.rotation_counts["LR"] += 1
                rotate_left(tree, node.getLeftChild())
                # Update heights of left subtree after rotation
                update_height(node.getLeftChild())
                update_height(node)
                rotate_right(tree, node)
                # Update heights after right rotation
                update_height(node)
                update_height(node.getParent())

        # RIGHT HEAVY (bf < -1)
        elif bf < -1:
            right_bf = get_balance_factor(node.getRightChild())

            if right_bf <= 0:
                # RR case: single left rotation
                tree.rotation_counts["RR"] += 1
                rotate_left(tree, node)
                # Update heights after rotation
                update_height(node)
                update_height(node.getParent())
            else:
                # RL case: right-left double rotation
                tree.rotation_counts["RL"] += 1
                rotate_right(tree, node.getRightChild())
                # Update heights of right subtree after rotation
                update_height(node.getRightChild())
                update_height(node)
                rotate_left(tree, node)
                # Update heights after left rotation
                update_height(node)
                update_height(node.getParent())

        # Move up towards root
        node = node.getParent()