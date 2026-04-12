"""
Calculador de precios basado en profundidad del árbol.
Responsabilidad única: cálculo de precios (SRP).

Reglas:
- Si profundidad <= depth_limit: precio_final = precio_base (sin cambios)
- Si profundidad > depth_limit: precio_final = precio_base * 1.25 (exactamente 25%)
"""


def calculate_final_price(precio_base: float, depth: int, limit: int) -> tuple:
    """
    Calcula el precio final y si el nodo es crítico basado en la profundidad.
    
    Args:
        precio_base: Precio base del vuelo
        depth: Profundidad actual en el árbol (0 = raíz)
        limit: Limite de profundidad crítica (depth_limit)
        
    Returns:
        tuple: (precio_final: float, nodoCritico: bool)
        
    Ejemplo:
        >>> calculate_final_price(100.0, 2, 3)  # depth <= limit
        (100.0, False)
        
        >>> calculate_final_price(100.0, 5, 3)  # depth > limit
        (125.0, False)  # 100 * 1.25 = 125
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
