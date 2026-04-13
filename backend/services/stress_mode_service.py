"""
Service for Stress Mode operations.

- Post-order rebalancing
- Tree integrity auditing
"""

from core.structures.avl_tree.balance import (get_balance_case,
                                              get_balance_factor, get_height,
                                              update_height)
from core.structures.avl_tree.rotations import rotate_left, rotate_right


def rebalance_tree_postorder(tree):
    """
    Rebalance the tree by traversing in post-order.

    - Visits leaves first
    - For each unbalanced node, applies necessary rotation
    - Records rotations in tree.rotation_counts

    Args:
        tree: AVL tree to rebalance

    Returns:
        dict: Dictionary containing:
            - status: Operation status
            - total_rotations: Total number of rotations performed
            - rotation_counts: Dictionary with LL, RR, LR, RL rotation counts
            - nodes_rebalanced: Number of nodes that were rebalanced
            - imbalanced_before: List of imbalanced nodes before rebalancing
    """
    if tree.root is None:
        return {
            'status': 'success',
            'total_rotations': 0,
            'rotation_counts': {'LL': 0, 'RR': 0, 'LR': 0, 'RL': 0},
            'nodes_rebalanced': 0,
            'imbalanced_before': []
        }
    
    # Guardar conteos iniciales
    initial_counts = {
        'LL': tree.rotation_counts['LL'],
        'RR': tree.rotation_counts['RR'],
        'LR': tree.rotation_counts['LR'],
        'RL': tree.rotation_counts['RL']
    }
    
    # Coleccionar nodos desbalanceados antes
    imbalanced_before = []
    
    # Rebalancear recursivamente en postorden
    nodes_rebalanced = _rebalance_recursively(tree, tree.root, imbalanced_before)
    
    # Calcular rotaciones aplicadas en esta operación
    rotations_applied = {
        'LL': tree.rotation_counts['LL'] - initial_counts['LL'],
        'RR': tree.rotation_counts['RR'] - initial_counts['RR'],
        'LR': tree.rotation_counts['LR'] - initial_counts['LR'],
        'RL': tree.rotation_counts['RL'] - initial_counts['RL']
    }
    
    total_rotations = sum(rotations_applied.values())
    
    return {
        'status': 'success',
        'total_rotations': total_rotations,
        'rotation_counts': rotations_applied,
        'nodes_rebalanced': nodes_rebalanced,
        'imbalanced_before': imbalanced_before,
        'current_tree_metrics': {
            'height': get_height(tree.root),
            'total_nodes': _count_nodes(tree.root)
        }
    }


def _rebalance_recursively(tree, node, imbalanced_list):
    """
    Traverse in post-order (left, right, node).

    Args:
        tree: AVL tree
        node: Current node
        imbalanced_list: List to accumulate imbalanced nodes found

    Returns:
        int: Number of nodes rebalanced in this subtree
    """
    if node is None:
        return 0
    
    rebalanced_count = 0
    
    # POSTORDEN: primero procesar subárbol izquierdo
    if node.getLeftChild() is not None:
        rebalanced_count += _rebalance_recursively(tree, node.getLeftChild(), imbalanced_list)
    
    # POSTORDEN: procesar subárbol derecho
    if node.getRightChild() is not None:
        rebalanced_count += _rebalance_recursively(tree, node.getRightChild(), imbalanced_list)
    
    # POSTORDEN: ahora procesar el nodo actual
    # Actualizar altura
    update_height(node)
    
    # Calcular factor de balance
    bf = get_balance_factor(node)
    
    # Verificar si está desbalanceado
    if abs(bf) > 1:
        # Registrar en imbalanced_before
        imbalanced_list.append({
            'codigo': node.getValue(),
            'balance_factor': bf,
            'height': get_height(node)
        })
        
        # Determinar tipo de rotación
        rotation_case = get_balance_case(node, bf)
        
        # LEFT HEAVY (bf > 1)
        if bf > 1:
            left_bf = get_balance_factor(node.getLeftChild())
            
            if left_bf >= 0:
                # LL case
                tree.rotation_counts['LL'] += 1
                rotate_right(tree, node)
                update_height(node)
                if node.getParent() is not None:
                    update_height(node.getParent())
            else:
                # LR case
                tree.rotation_counts['LR'] += 1
                rotate_left(tree, node.getLeftChild())
                update_height(node.getLeftChild())
                update_height(node)
                rotate_right(tree, node)
                update_height(node)
                if node.getParent() is not None:
                    update_height(node.getParent())
        
        # RIGHT HEAVY (bf < -1)
        elif bf < -1:
            right_bf = get_balance_factor(node.getRightChild())
            
            if right_bf <= 0:
                # RR case
                tree.rotation_counts['RR'] += 1
                rotate_left(tree, node)
                update_height(node)
                if node.getParent() is not None:
                    update_height(node.getParent())
            else:
                # RL case
                tree.rotation_counts['RL'] += 1
                rotate_right(tree, node.getRightChild())
                update_height(node.getRightChild())
                update_height(node)
                rotate_left(tree, node)
                update_height(node)
                if node.getParent() is not None:
                    update_height(node.getParent())
        
        rebalanced_count += 1
    
    return rebalanced_count


def audit_tree(tree):
    """
    Audit the integrity of the AVL tree.

    Verifies:
    - Balance factor ∈ {-1, 0, 1} for all nodes
    - Correct height according to formula: 1 + max(left_h, right_h)

    Args:
        tree: AVL tree to audit

    Returns:
        dict: Dictionary containing:
            - valid: Boolean indicating if tree is valid
            - nodes_checked: Number of nodes checked
            - inconsistent_nodes: List of nodes with inconsistencies
    """
    if tree.root is None:
        return {
            'valid': True,
            'nodes_checked': 0,
            'inconsistent_nodes': []
        }
    
    inconsistent_nodes = []
    nodes_checked = [0]  # Usar lista para poder modificar en función anidada
    
    def _audit_recursively(node):
        """Auditar recursivamente cada nodo."""
        if node is None:
            return True
        
        nodes_checked[0] += 1
        
        # Auditar subárbol izquierdo
        left_valid = _audit_recursively(node.getLeftChild())
        
        # Auditar subárbol derecho
        right_valid = _audit_recursively(node.getRightChild())
        
        # Calcular altura esperada
        left_h = get_height(node.getLeftChild())
        right_h = get_height(node.getRightChild())
        expected_height = 1 + max(left_h, right_h)
        actual_height = node.getHeight()
        
        # Calcular factor de balance
        bf = get_balance_factor(node)
        
        # Verificar consistencia
        is_consistent = True
        height_consistent = (expected_height == actual_height)
        balance_consistent = (abs(bf) <= 1)
        
        if not height_consistent or not balance_consistent:
            is_consistent = False
            inconsistent_nodes.append({
                'codigo': node.getValue(),
                'balance_factor': bf,
                'expected_balance': abs(bf) <= 1,
                'expected_height': expected_height,
                'actual_height': actual_height
            })
        
        return left_valid and right_valid and is_consistent
    
    is_valid = _audit_recursively(tree.root)
    
    return {
        'valid': is_valid and len(inconsistent_nodes) == 0,
        'nodes_checked': nodes_checked[0],
        'inconsistent_nodes': inconsistent_nodes
    }


def _count_nodes(node):
    """
    Count nodes recursively.

    Args:
        node: Root node of the subtree to count

    Returns:
        int: Number of nodes in the subtree
    """
    if node is None:
        return 0
    return 1 + _count_nodes(node.getLeftChild()) + _count_nodes(node.getRightChild())
