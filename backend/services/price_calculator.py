"""
Price calculator based on tree depth.

Single responsibility: price calculation (SRP).

Rules:
- If depth <= depth_limit: final_price = base_price (no changes)
- If depth > depth_limit: final_price = base_price * 1.25 (exactly 25%)
"""


def calculate_final_price(precio_base: float, depth: int, limit: int) -> tuple:
    """
    Calculate the final price and whether the node is critical based on depth.

    Args:
        precio_base (float): Base price of the flight
        depth (int): Current depth in the tree (0 = root)
        limit (int): Critical depth limit (depth_limit)

    Returns:
        tuple: (final_price: float, is_critical: bool)

    Example:
        >>> calculate_final_price(100.0, 2, 3)  # depth <= limit
        (100.0, False)

        >>> calculate_final_price(100.0, 5, 3)  # depth > limit
        (125.0, True)  # 100 * 1.25 = 125
    """
    # Validar inputs
    if precio_base is None or precio_base < 0:
        precio_base = 0
    
    if limit is None:
        # Sin límite de profundidad → sin penalización
        return (float(precio_base), False)
    
    # Determinar si nodo está en profundidad crítica
    es_critico = depth > limit
    
    # Calcular precio final
    if es_critico:
        # Profundidad > limit → aplicar penalización exacta del 25%
        precio_final = precio_base * 1.25
    else:
        # Profundidad <= limit → precio normal
        precio_final = float(precio_base)
    
    return (precio_final, es_critico)


def is_node_critical(depth: int, limit: int) -> bool:
    """
    Verifica si un nodo está en profundidad crítica.
    
    Args:
        depth: Profundidad actual en el árbol
        limit: Limite de profundidad crítica (depth_limit)
        
    Returns:
        bool: True si está en profundidad crítica (depth > limit)
    """
    if limit is None:
        return False
    return depth > limit
