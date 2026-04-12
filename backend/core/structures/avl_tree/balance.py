from .rotations import rotate_left, rotate_right


def get_height(node):
    """
    Get node height in O(1).

    Args:
        node: Tree node

    Returns:
        int: Node height (0 if None)
    """
    if node is None:
        return 0
    return node.getHeight()


def update_height(node):
    """
    Update node height from its children in O(1).
    Call after any structural change.

    Args:
        node: Node to update
    """
    if node is None:
        return
    
    left_height = get_height(node.getLeftChild())
    right_height = get_height(node.getRightChild())
    node.setHeight(1 + max(left_height, right_height))


def get_balance_factor(node):
    """
    Compute balance factor in O(1).
    Positive means left heavy, negative means right heavy.

    Args:
        node: Node to evaluate

    Returns:
        int: Balance factor (h_left - h_right)
    """
    if node is None:
        return 0
    
    left_height = get_height(node.getLeftChild())
    right_height = get_height(node.getRightChild())
    return left_height - right_height


def get_balance_case(node, bf):
    """
    Determine imbalance case (LL, RR, LR, RL).

    Args:
        node: Imbalanced node
        bf: Balance factor for the node

    Returns:
        str: Rotation case
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
    Check and restore AVL balance from a node up to the root.

    The four rotation cases are:
    - LL: left-left heavy, rotate right.
    - RR: right-right heavy, rotate left.
    - LR: left-right heavy, rotate left on child then right on node.
    - RL: right-left heavy, rotate right on child then left on node.

    When tree.stress_mode is True, only heights are updated (no rotations).
    """
    
    while node is not None:
        # Actualizar altura del nodo actual
        update_height(node)
        
        # Calcular factor de balance
        bf = get_balance_factor(node)
        
        # Si stress_mode está activo, solo actualizar altura y subir
        if tree.stress_mode:
            node = node.getParent()
            continue
        
        # LEFT HEAVY (bf > 1)
        if bf > 1:
            left_bf = get_balance_factor(node.getLeftChild())
            
            if left_bf >= 0:
                # LL case: rotación simple a la derecha
                tree.rotation_counts["LL"] += 1
                rotate_right(tree, node)
                # Actualizar alturas después de rotación
                update_height(node)
                update_height(node.getParent())
            else:
                # LR case: rotación izquierda-derecha
                tree.rotation_counts["LR"] += 1
                rotate_left(tree, node.getLeftChild())
                # Actualizar alturas del subtree izquierdo después de rotación
                update_height(node.getLeftChild())
                update_height(node)
                rotate_right(tree, node)
                # Actualizar alturas después de rotación derecha
                update_height(node)
                update_height(node.getParent())
        
        # RIGHT HEAVY (bf < -1)
        elif bf < -1:
            right_bf = get_balance_factor(node.getRightChild())
            
            if right_bf <= 0:
                # RR case: rotación simple a la izquierda
                tree.rotation_counts["RR"] += 1
                rotate_left(tree, node)
                # Actualizar alturas después de rotación
                update_height(node)
                update_height(node.getParent())
            else:
                # RL case: rotación derecha-izquierda
                tree.rotation_counts["RL"] += 1
                rotate_right(tree, node.getRightChild())
                # Actualizar alturas del subtree derecho después de rotación
                update_height(node.getRightChild())
                update_height(node)
                rotate_left(tree, node)
                # Actualizar alturas después de rotación izquierda
                update_height(node)
                update_height(node.getParent())
        
        # Subir hacia la raíz
        node = node.getParent()