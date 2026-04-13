"""
AVL tree metrics calculation service.

This module provides functionality to calculate various metrics and analytics
for AVL trees, including height, node counts, rotation statistics, and traversal data.
"""

from core.structures.avl_tree.balance import get_balance_factor, get_height
from core.structures.avl_tree.traversal import (breadth_first_traversal,
                                                in_order)


def get_metrics(avl) -> dict:
    """
    Calculate and return all real-time analytics for the AVL tree.

    Args:
        avl: The AVL tree instance to analyze

    Returns:
        dict: Dictionary containing tree metrics including:
            - height: Tree height
            - leaves: Number of leaf nodes
            - total_nodes: Total number of nodes
            - rotation_counts: Dictionary of rotation types and counts
            - total_rotations: Sum of all rotations
            - mass_cancellations: Count of mass cancellation operations
            - stress_mode: Current stress mode status
            - depth_limit: Current depth limit setting
            - traversals: Dictionary with inorder and BFS traversal results
    """
    root = avl.getRoot()
    total_rotations = sum(avl.rotation_counts.values())
    
    return {
        "height": get_height(root),
        "leaves": avl.contar_hojas(),
        "total_nodes": _count_nodes(root),
        "rotation_counts": avl.rotation_counts,
        "total_rotations": total_rotations,
        "mass_cancellations": avl.mass_cancellation_count,
        "stress_mode": avl.stress_mode,
        "depth_limit": avl.depth_limit,
        "traversals": {
            "inorder": in_order(root),
            "bfs": breadth_first_traversal(root)
        }
    }


def _count_nodes(node) -> int:
    """
    Count total nodes in the tree.

    Args:
        node: The root node of the subtree to count

    Returns:
        int: Total number of nodes in the subtree
    """
    if node is None:
        return 0
    return 1 + _count_nodes(node.getLeftChild()) + _count_nodes(node.getRightChild())
