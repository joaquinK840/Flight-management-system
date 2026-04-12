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
