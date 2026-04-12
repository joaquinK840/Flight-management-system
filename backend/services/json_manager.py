import json
from core.structures.node.node import Node
from core.structures.avl_tree.tree import AVL
from core.structures.avl_tree.balance import update_height
from core.structures.bst_tree.bst import BST


def validate_flight_data(data: dict) -> bool:
    """
    Valida que un diccionario tenga la estructura mínima de vuelo.
    
    Args:
        data: Diccionario de datos de vuelo
        
    Returns:
        bool: True si es válido
    """
    required_fields = ["codigo"]
    for field in required_fields:
        if field not in data:
            return False
    return True


def load_from_topology(json_data: dict) -> tuple:
    """
    Carga un árbol desde JSON en modo Topología.
    Reconstruye exactamente la estructura sin aplicar balanceo.
    
    Args:
        json_data: Dict con estructura { "type": "topology", "root": {...} }
        
    Returns:
        tuple: (avl, bst) - árboles reconstruidos
    """
    if "root" not in json_data:
        raise ValueError("Modo topology requiere un campo 'root'")

    avl = AVL()
    bst = BST()

    def reconstruct_node_recursive(node_data):
        """
        Reconstruye un nodo y sus hijos desde JSON.
        """
        if node_data is None:
            return None

        value = node_data.get("codigo") or node_data.get("value")
        if value is None:
            raise ValueError("Cada nodo debe tener 'codigo' o 'value'")

        # Crear nodo con datos
        datos = node_data.copy()
        if "left" in datos:
            del datos["left"]
        if "right" in datos:
            del datos["right"]

        node = Node(value, datos=datos if datos else None)

        # Reconstruir subárboles
        if "left" in node_data and node_data["left"] is not None:
            left_child = reconstruct_node_recursive(node_data["left"])
            node.setLeftChild(left_child)
            left_child.setParent(node)

        if "right" in node_data and node_data["right"] is not None:
            right_child = reconstruct_node_recursive(node_data["right"])
            node.setRightChild(right_child)
            right_child.setParent(node)

        return node

    # Reconstruir árbol desde JSON
    root = reconstruct_node_recursive(json_data["root"])

    # Establecer raíz en árboles
    avl.root = root
    bst.root = root

    # Calcular alturas correctas en todo el árbol
    def calculate_all_heights(node):
        if node is None:
            return
        calculate_all_heights(node.getLeftChild())
        calculate_all_heights(node.getRightChild())
        update_height(node)

    calculate_all_heights(root)

    return avl, bst


def load_from_insertion(json_data: dict) -> tuple:
    """
    Carga un árbol desde JSON en modo Inserción.
    Inserta vuelos uno a uno en AVL (con balanceo) y BST (sin balanceo).
    
    Args:
        json_data: Dict con estructura { "type": "insertion", "flights": [...] }
        
    Returns:
        tuple: (avl, bst) - árboles con vuelos insertados
    """
    if "flights" not in json_data:
        raise ValueError("Modo insertion requiere un campo 'flights'")

    flights = json_data["flights"]
    if not isinstance(flights, list):
        raise ValueError("El campo 'flights' debe ser una lista")

    avl = AVL()
    bst = BST()

    for flight_data in flights:
        if not isinstance(flight_data, dict):
            raise ValueError("Cada vuelo debe ser un diccionario")

        # Validar estructura mínima
        if not validate_flight_data(flight_data):
            continue  # Saltar vuelos inválidos

        value = flight_data.get("codigo")

        # Crear nodo con datos completos
        node_avl = Node(value, datos=flight_data.copy())
        node_bst = Node(value, datos=flight_data.copy())

        # Insertar en ambos árboles
        avl.insert(node_avl)
        bst.insert(node_bst)

    return avl, bst


def load_trees_from_json(json_content: str) -> tuple:
    """
    Carga árboles desde una cadena JSON.
    
    Args:
        json_content: Contenido JSON como string
        
    Returns:
        tuple: (avl, bst, load_type)
        
    Raises:
        ValueError: Si el JSON tiene formato inválido
        json.JSONDecodeError: Si el JSON no es válido
    """
    try:
        json_data = json.loads(json_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON inválido: {str(e)}")

    if not isinstance(json_data, dict):
        raise ValueError("El JSON debe ser un objeto (diccionario)")

    load_type = json_data.get("type")

    if load_type == "topology":
        avl, bst = load_from_topology(json_data)
        return avl, bst, "topology"

    elif load_type == "insertion":
        avl, bst = load_from_insertion(json_data)
        return avl, bst, "insertion"

    else:
        raise ValueError(f"Tipo de carga no soportado: {load_type}. Usar 'topology' o 'insertion'")


def export_tree_to_json(tree) -> dict:
    """
    Exporta el árbol AVL completo a una estructura JSON.
    Guarda la estructura real del árbol (no solo lista de vuelos).
    
    El JSON exportado puede ser recargado exactamente con POST /avl/load-file
    (idempotencia: exportar + reimportar produce el mismo árbol).
    
    Args:
        tree: Instancia de árbol AVL
        
    Returns:
        dict: Estructura JSON con:
            - type: "topology"
            - depth_limit: int
            - rotation_counts: {LL, RR, LR, RL}
            - mass_cancellation_count: int
            - root: nodo raíz serializado recursivamente
    """
    def serialize_node_recursive(node, current_depth=0):
        """
        Serializa un nodo y sus hijos recursivamente.
        
        Args:
            node: Nodo a serializar
            current_depth: Profundidad actual (para tracking)
            
        Returns:
            dict: Nodo serializado con estructura completa
        """
        if node is None:
            return None
        
        # Obtener datos del nodo
        node_datos = node.getDatos() if node.getDatos() else {}
        codigo = node.getValue()
        altura = node.getHeight() if hasattr(node, 'getHeight') else node.height
        
        # Calcular balance factor
        left_child = node.getLeftChild() if hasattr(node, 'getLeftChild') else node.leftChild
        right_child = node.getRightChild() if hasattr(node, 'getRightChild') else node.rightChild
        
        left_height = (left_child.getHeight() if hasattr(left_child, 'getHeight') else left_child.height) if left_child else 0
        right_height = (right_child.getHeight() if hasattr(right_child, 'getHeight') else right_child.height) if right_child else 0
        balance_factor = left_height - right_height
        
        # Serializar nodo con todos sus atributos
        serialized_node = {
            "codigo": codigo,
            "height": altura,
            "balance_factor": balance_factor,
            "profundidad": current_depth,
            "datos": node_datos,
            "left": serialize_node_recursive(left_child, current_depth + 1),
            "right": serialize_node_recursive(right_child, current_depth + 1)
        }
        
        return serialized_node
    
    # Obtener raíz del árbol
    root = tree.getRoot() if hasattr(tree, 'getRoot') else tree.root
    
    # Obtener metadatos del árbol
    rotation_counts = getattr(tree, 'rotation_counts', {"LL": 0, "RR": 0, "LR": 0, "RL": 0})
    mass_cancellation_count = getattr(tree, 'mass_cancellation_count', 0)
    depth_limit = getattr(tree, 'depth_limit', 3)
    
    # Construir estructura JSON de exportación
    export_data = {
        "type": "topology",
        "depth_limit": depth_limit,
        "rotation_counts": rotation_counts,
        "mass_cancellation_count": mass_cancellation_count,
        "root": serialize_node_recursive(root, 0)
    }
    
    return export_data
