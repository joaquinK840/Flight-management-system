def serialize_tree(tree, depth=0, depth_limit=None):
    """
    Serializa el árbol AVL con cálculos de precios basados en profundidad.
    
    Reglas de precio:
    - Si profundidad <= depth_limit: precio_final = precio_base
    - Si profundidad > depth_limit: precio_final = precio_base * 1.25 (exactamente 25%)
    
    Args:
        tree: Instancia de árbol AVL
        depth: Profundidad inicial (raiz = 0)
        depth_limit: Limite crítico de profundidad (opcional, usa tree.depth_limit si no se proporciona)
        
    Returns:
        dict: {
            "root": árbol serializado con precios recalculados,
            "depth_limit": limit utilizado,
            "rotations": {conteos de rotaciones}
        }
    """
    root = tree.getRoot()
    
    # Determinar el límite de profundidad a usar
    if depth_limit is not None:
        depth_limit_val = depth_limit
    elif hasattr(tree, 'depth_limit'):
        depth_limit_val = tree.depth_limit
    else:
        depth_limit_val = None
    
    def _serialize_node(node, current_depth=0):
        """Serializa un nodo recursivamente con cálculo de precios."""
        if node is None:
            return None

        # Obtener datos del nodo
        node_datos = node.getDatos() if node.getDatos() else {}
        codigo = node_datos.get("codigo", node.getValue())
        precio_base = node_datos.get("precioBase", 0)

        left_child = node.getLeftChild()
        right_child = node.getRightChild()
        left_height = left_child.getHeight() if left_child else 0
        right_height = right_child.getHeight() if right_child else 0
        balance_factor = left_height - right_height

        is_critical = depth_limit_val is not None and current_depth > depth_limit_val
        precio_final = precio_base * 1.25 if is_critical else precio_base

        return {
            "value": node.getValue(),
            "height": node.getHeight(),
            "balance_factor": balance_factor,
            "codigo": codigo,
            "origen": node_datos.get("origen", ""),
            "destino": node_datos.get("destino", ""),
            "horaSalida": node_datos.get("horaSalida", ""),
            "pasajeros": node_datos.get("pasajeros", 0),
            "prioridad": node_datos.get("prioridad", 0),
            "promocion": node_datos.get("promocion", False),
            "alerta": node_datos.get("alerta", ""),
            "precioBase": precio_base,
            "precioFinal": precio_final,
            "nodoCritico": is_critical,
            "profundidad": current_depth,
            "penalizacion": 0.0,
            "datos": node_datos,
            "left": _serialize_node(left_child, current_depth + 1),
            "right": _serialize_node(right_child, current_depth + 1)
        }
    
    serialized_root = _serialize_node(root, depth)
    
    return {
        "root": serialized_root,
        "depth_limit": depth_limit_val,
        "rotations": tree.rotation_counts if hasattr(tree, 'rotation_counts') else {},
        "metrics": {
            "total_nodes": _count_nodes_dict(serialized_root),
            "height": _get_height_dict(serialized_root)
        }
    }


def _count_nodes_dict(node):
    """Cuenta nodos recursivamente en árbol serializado (diccionario)."""
    if node is None:
        return 0
    return 1 + _count_nodes_dict(node.get("left")) + _count_nodes_dict(node.get("right"))


def _get_height_dict(node):
    """Calcula altura del árbol serializado (diccionario)."""
    if node is None:
        return 0
    left_height = _get_height_dict(node.get("left"))
    right_height = _get_height_dict(node.get("right"))
    return 1 + max(left_height, right_height)
