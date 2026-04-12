from core.structures.avl_tree.balance import get_balance_factor, get_height


def serialize_tree(tree, depth=0, depth_limit=None):
    """
    Serialize the AVL tree with depth-based pricing.

    Pricing rules:
    - If depth <= depth_limit: precio_final = precio_base
    - If depth > depth_limit: precio_final = precio_base * 1.25 (exact 25%)

    Args:
        tree: AVL tree instance
        depth_limit: Critical depth limit (optional, uses tree.depth_limit if not provided)

    Returns:
        dict: {
            "root": serialized tree with recalculated prices,
            "depth_limit": applied limit,
            "rotations": rotation counts
        }
    """
    root = tree.getRoot()

    # Determinar el limite de profundidad a usar
    if depth_limit is not None:
        depth_limit_val = depth_limit
    elif hasattr(tree, 'depth_limit'):
        depth_limit_val = tree.depth_limit
    else:
        depth_limit_val = None

    def _serialize_node(node, current_depth):
        """Serialize a node recursively with price calculation."""
        if node is None:
            return None

        node_datos = node.getDatos() if node.getDatos() else {}
        codigo = node_datos.get("codigo", node.getValue())
        precio_base = float(node_datos.get("precioBase", 0))
        is_critical = depth_limit_val is not None and current_depth > depth_limit_val
        precio_final = precio_base * 1.25 if is_critical else precio_base

        return {
            "value": node.getValue(),
            "height": get_height(node),
            "balance_factor": get_balance_factor(node),
            "codigo": codigo,
            "origen": node_datos.get("origen", ""),
            "destino": node_datos.get("destino", ""),
            "horaSalida": node_datos.get("horaSalida", ""),
            "pasajeros": node_datos.get("pasajeros", 0),
            "prioridad": node_datos.get("prioridad", 0),
            "promocion": node_datos.get("promocion", False),
            "alerta": node_datos.get("alerta", False),
            "precioBase": precio_base,
            "precioFinal": round(precio_final, 2),
            "nodoCritico": is_critical,
            "profundidad": current_depth,
            "penalizacion": 0.0,
            "left": _serialize_node(node.getLeftChild(), current_depth + 1),
            "right": _serialize_node(node.getRightChild(), current_depth + 1)
        }

    return {
        "root": _serialize_node(root, depth),
        "depth_limit": depth_limit_val,
        "rotations": tree.rotation_counts if hasattr(tree, 'rotation_counts') else {},
        "metrics": {
            "total_nodes": _count_nodes(root),
            "height": _get_height(root)
        }
    }


def _count_nodes(node):
    """Count nodes recursively."""
    if node is None:
        return 0
    return 1 + _count_nodes(node.getLeftChild()) + _count_nodes(node.getRightChild())


def _get_height(node):
    """Compute tree height."""
    if node is None:
        return 0
    left_height = _get_height(node.getLeftChild())
    right_height = _get_height(node.getRightChild())
    return 1 + max(left_height, right_height)
