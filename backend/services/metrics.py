from core.structures.avl_tree.balance import get_height, get_balance_factor
from core.structures.avl_tree.traversal import in_order, breadth_first_traversal


def get_metrics(avl) -> dict:
    """Calculate and return all real-time analytics for the AVL tree."""
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
    """Count total nodes in the tree."""
    if node is None:
        return 0
    return 1 + _count_nodes(node.getLeftChild()) + _count_nodes(node.getRightChild())
