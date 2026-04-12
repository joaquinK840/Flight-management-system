"""
Servicio de Rentabilidad - Calcula y analiza la rentabilidad de vuelos.
Single Responsibility: Solo maneja cálculos de rentabilidad.
"""


def calculate_rentability(node_datos: dict, penalty_active: bool = False) -> float:
    """
    Calcula la rentabilidad de un vuelo basado en sus datos.
    
    Fórmula:
        rentabilidad = (pasajeros × precioFinal) - descuento_promocion
    
    Donde:
        descuento_promocion = 0.1 × precioFinal si hay promoción, else 0
        penalty = ya incluido en precioFinal (no se suma aquí)
    
    Args:
        node_datos: Dict con datos del vuelo
                    {
                        "codigo": int,
                        "origen": str,
                        "destino": str,
                        "precioBase": float,
                        "precioFinal": float,
                        "pasajeros": int,
                        "promocion": bool,
                        ...
                    }
        penalty_active: No se usa en este cálculo (penalty ya está en precioFinal)
        
    Returns:
        float: Rentabilidad calculada
        
    Raises:
        KeyError: Si faltan campos requeridos en node_datos
    """
    if not node_datos:
        return 0.0
    
    try:
        # Obtener valores
        pasajeros = node_datos.get("pasajeros", 0)
        precio_final = node_datos.get("precioFinal", node_datos.get("precioBase", 0))
        tiene_promocion = node_datos.get("promocion", False)
        
        # Calcular ingresos base
        ingresos_base = pasajeros * precio_final
        
        # Aplicar descuento de promoción (10%)
        descuento_promocion = 0.1 * precio_final if tiene_promocion else 0
        
        # Rentabilidad final
        # Nota: penalty ya está incluido en precioFinal como incremento (+25% si depth > limit)
        rentabilidad = ingresos_base - descuento_promocion
        
        return round(rentabilidad, 2)
    
    except Exception as e:
        print(f"Error calculando rentabilidad: {e}")
        return 0.0


def find_least_profitable(tree) -> tuple:
    """
    Encuentra el nodo de MENOR rentabilidad en el árbol.
    
    Criterios de desempate (en orden):
    1. Menor rentabilidad
    2. Mayor profundidad (más lejano de la raíz)
    3. Mayor código (value)
    
    Args:
        tree: Instancia de árbol AVL/BST
        
    Returns:
        Tupla: (node, rentabilidad, codigo, profundidad)
               Si árbol vacío: (None, None, None, None)
    
    Raises:
        ValueError: Si el árbol está vacío
    """
    root = tree.getRoot() if hasattr(tree, 'getRoot') else None
    
    if root is None:
        raise ValueError("Árbol vacío")
    
    # Estado para guardar el mejor nodo
    best = {
        "node": None,
        "rentability": float('inf'),
        "codigo": 0,
        "profundidad": 0
    }
    
    def traverse(node, depth=0):
        """
        Recorre el árbol en profundidad para encontrar el nodo de menor rentabilidad.
        
        Args:
            node: Nodo actual
            depth: Profundidad actual (0 = raíz)
        """
        if node is None:
            return
        
        # Obtener datos del nodo
        datos = node.getDatos() if hasattr(node, 'getDatos') else {}
        codigo = node.getValue() if hasattr(node, 'getValue') else 0
        
        # Calcular rentabilidad
        rentability = calculate_rentability(datos)
        
        # Criterio de desempate:
        # 1. Menor rentabilidad
        # 2. Si es igual, mayor profundidad
        # 3. Si es igual, mayor código
        should_replace = False
        
        if rentability < best["rentability"]:
            # Es menos rentable
            should_replace = True
        elif rentability == best["rentability"]:
            # Igual rentabilidad
            if depth > best["profundidad"]:
                # Mayor profundidad (más lejano de raíz)
                should_replace = True
            elif depth == best["profundidad"] and codigo > best["codigo"]:
                # Igual profundidad, mayor código
                should_replace = True
        
        if should_replace:
            best["node"] = node
            best["rentability"] = rentability
            best["codigo"] = codigo
            best["profundidad"] = depth
        
        # Recorrer hijos
        left_child = node.getLeftChild() if hasattr(node, 'getLeftChild') else None
        right_child = node.getRightChild() if hasattr(node, 'getRightChild') else None
        
        traverse(left_child, depth + 1)
        traverse(right_child, depth + 1)
    
    # Iniciar recorrido desde raíz
    traverse(root, 0)
    
    if best["node"] is None:
        raise ValueError("No se encontró nodo")
    
    return (best["node"], best["rentability"], best["codigo"], best["profundidad"])


def count_subtree_size(node) -> int:
    """
    Cuenta la cantidad de nodos en un subárbol.
    
    Args:
        node: Nodo raíz del subárbol
        
    Returns:
        int: Cantidad de nodos (incluyendo el nodo actual)
    """
    if node is None:
        return 0
    
    left_count = count_subtree_size(
        node.getLeftChild() if hasattr(node, 'getLeftChild') else None
    )
    right_count = count_subtree_size(
        node.getRightChild() if hasattr(node, 'getRightChild') else None
    )
    
    return 1 + left_count + right_count
