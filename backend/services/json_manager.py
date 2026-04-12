import json
from core.structures.node.node import Node
from core.structures.avl_tree.tree import AVL
from core.structures.avl_tree.balance import update_height
from core.structures.bst_tree.bst import BST


def validate_flight_data(data: dict) -> bool:
    """
    Validate the minimum flight payload structure.

    Args:
        data: Flight data dict

    Returns:
        bool: True when valid
    """
    required_fields = ["codigo"]
    for field in required_fields:
        if field not in data:
            return False
    return True


def load_from_topology(json_data: dict) -> tuple:
    """
    Load a tree from JSON in Topology mode.
    Rebuilds the exact structure without balancing.

    Args:
        json_data: Dict payload { "type": "topology", "root": {...} }

    Returns:
        tuple: (avl, bst) reconstructed trees
    """
    if "root" not in json_data:
        raise ValueError("Modo topology requiere un campo 'root'")

    avl = AVL()
    bst = BST()

    def reconstruct_node_recursive(node_data):
        """
        Rebuild a node and its children from JSON.
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
        left_payload = None
        if "left" in node_data:
            left_payload = node_data["left"]
        elif "izquierdo" in node_data:
            left_payload = node_data["izquierdo"]

        if left_payload is not None:
            left_child = reconstruct_node_recursive(left_payload)
            node.setLeftChild(left_child)
            left_child.setParent(node)

        right_payload = None
        if "right" in node_data:
            right_payload = node_data["right"]
        elif "derecho" in node_data:
            right_payload = node_data["derecho"]

        if right_payload is not None:
            right_child = reconstruct_node_recursive(right_payload)
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
    Load a tree from JSON in insertion mode.
    Inserts flights into AVL (balanced) and BST (unbalanced).

    Args:
        json_data: Dict payload { "type": "insertion", "flights": [...] }

    Returns:
        tuple: (avl, bst) populated trees
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
    Load trees from a JSON string.

    Args:
        json_content: JSON content as string

    Returns:
        tuple: (avl, bst, load_type)

    Raises:
        ValueError: Invalid JSON format
        json.JSONDecodeError: Invalid JSON syntax
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
    Export the AVL tree to a topology JSON payload.
    Preserves the exact structure (not just a flight list).

    The exported JSON can be reloaded with POST /avl/load-file
    (idempotent: export + reimport yields the same tree).

    Args:
        tree: AVL tree instance

    Returns:
        dict: JSON structure with:
            - type: "topology"
            - depth_limit: int
            - rotation_counts: {LL, RR, LR, RL}
            - mass_cancellation_count: int
            - root: recursively serialized root node
    """
    def serialize_node_recursive(node, current_depth=0):
        """
        Serialize a node and its children recursively.

        Args:
            node: Node to serialize
            current_depth: Current depth (for tracking)

        Returns:
            dict: Serialized node with full structure
        """
        if node is None:
            return None
        
        node_datos = node.getDatos() if node.getDatos() else {}
        codigo = node_datos.get("codigo", node.getValue())
        altura = node.getHeight() if hasattr(node, "getHeight") else node.height

        left_child = node.getLeftChild() if hasattr(node, "getLeftChild") else node.leftChild
        right_child = node.getRightChild() if hasattr(node, "getRightChild") else node.rightChild

        left_height = (left_child.getHeight() if hasattr(left_child, "getHeight") else left_child.height) if left_child else 0
        right_height = (right_child.getHeight() if hasattr(right_child, "getHeight") else right_child.height) if right_child else 0
        balance_factor = left_height - right_height

        depth_limit = getattr(tree, "depth_limit", None)
        is_critical = depth_limit is not None and current_depth > depth_limit
        precio_base = float(node_datos.get("precioBase", 0))
        precio_final = precio_base * 1.25 if is_critical else precio_base
        penalizacion = round(precio_final - precio_base, 2) if is_critical else 0.0

        serialized_node = {
            "value": node.getValue(),
            "altura": altura,
            "factorEquilibrio": balance_factor,
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
            "penalizacion": penalizacion,
            "izquierdo": serialize_node_recursive(left_child, current_depth + 1),
            "derecho": serialize_node_recursive(right_child, current_depth + 1)
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
        "stress_mode_at_export": bool(getattr(tree, "stress_mode", False)),
        "root": serialize_node_recursive(root, 0)
    }
    
    return export_data
