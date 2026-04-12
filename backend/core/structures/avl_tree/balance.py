from .rotations import rotate_left, rotate_right


def get_height(node):
    """
    Obtiene la altura de un nodo en O(1).
    
    Args:
        node: Nodo del árbol
        
    Returns:
        int: Altura del nodo (0 si es None)
    """
    if node is None:
        return 0
    return node.getHeight()


def update_height(node):
    """
    Actualiza la altura de un nodo basada en sus hijos en O(1).
    Debe llamarse después de cualquier cambio en la estructura.
    
    Args:
        node: Nodo a actualizar
    """
    if node is None:
        return
    
    left_height = get_height(node.getLeftChild())
    right_height = get_height(node.getRightChild())
    node.setHeight(1 + max(left_height, right_height))


def get_balance_factor(node):
    """
    Calcula el factor de balance de un nodo en O(1).
    Factor positivo = árbol inclinado a la izquierda
    Factor negativo = árbol inclinado a la derecha
    
    Args:
        node: Nodo a evaluar
        
    Returns:
        int: Factor de balance (h_left - h_right)
    """
    if node is None:
        return 0
    
    left_height = get_height(node.getLeftChild())
    right_height = get_height(node.getRightChild())
    return left_height - right_height


def get_balance_case(node, bf):
    """
    Determina el tipo de desbalance (LL, RR, LR, RL).
    
    Args:
        node: Nodo desbalanceado
        bf: Factor de balance del nodo
        
    Returns:
        str: Tipo de rotación necesaria
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
    Verifica y restaura el balance del árbol AVL desde un nodo hacia la raíz.
    - Actualiza alturas de todos los nodos afectados
    - Aplica rotaciones si el árbol está desbalanceado (|bf| > 1)
    - Respeta tree.stress_mode: si es True, solo actualiza alturas
    - Propaga cambios hacia la raíz
    
    Args:
        tree: Árbol AVL
        node: Nodo desde el cual iniciar el chequeo (típicamente padre del inserido)
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