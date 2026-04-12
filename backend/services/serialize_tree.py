from services.price_calculator import calculate_final_price


def serialize_tree(tree, depth_limit=None):
    """
    Serializa el árbol AVL con cálculos de precios basados en profundidad.
    
    Reglas de precio:
    - Si profundidad <= depth_limit: precio_final = precio_base
    - Si profundidad > depth_limit: precio_final = precio_base * 1.25 (exactamente 25%)
    
    Args:
        tree: Instancia de árbol AVL
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
        precio_base = node_datos.get('precioBase', 0)
        codigo = node.getValue()
        
        # Calcular precio final y estado crítico
        precio_final, es_critico = calculate_final_price(precio_base, current_depth, depth_limit_val)
        
        return {
            "value": codigo,
            "codigo": codigo,
            "profundidad": current_depth,
            "nodoCritico": es_critico,
            "precioBase": precio_base,
            "precioFinal": round(precio_final, 2),
            "datos": node_datos,
            "left": _serialize_node(node.getLeftChild(), current_depth + 1),
            "right": _serialize_node(node.getRightChild(), current_depth + 1)
        }
    
    return {
        "root": _serialize_node(root, 0),
        "depth_limit": depth_limit_val,
        "rotations": tree.rotation_counts if hasattr(tree, 'rotation_counts') else {},
        "metrics": {
            "total_nodes": _count_nodes(root),
            "height": _get_height(root)
        }
    }


def _count_nodes(node):
    """Cuenta nodos recursivamente."""
    if node is None:
        return 0
    return 1 + _count_nodes(node.get("left")) + _count_nodes(node.get("right"))


def _get_height(node):
    """Calcula altura del árbol serializado."""
    if node is None:
        return 0
    left_height = _get_height(node.get("left"))
    right_height = _get_height(node.get("right"))
    return 1 + max(left_height, right_height)
