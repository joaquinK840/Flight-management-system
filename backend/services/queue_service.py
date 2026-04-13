"""
Queue service for concurrency simulation.

Handles FIFO operations of pending flights to be processed.
"""

from core.shared_instances import flight_queue  # Use shared instance
from core.structures.avl_tree.balance import get_balance_factor
from core.structures.node.node import Node
from core.structures.queue.queue import Queue
from services.serialize_tree import serialize_tree


def add_flight_to_queue(flight_data: dict) -> dict:
    """
    Add a flight to the queue without processing it yet.

    Args:
        flight_data (dict): Dictionary containing flight information
            {codigo, origen, destino, horaSalida, precioBase, pasajeros, prioridad}

    Returns:
        dict: Dictionary with status, message, queue_size, and pending_flights
    """
    flight_queue.enqueue(flight_data)
    
    return {
        "status": "success",
        "message": f"Vuelo {flight_data.get('codigo')} agregado a la cola",
        "queue_size": flight_queue.size(),
        "pending_flights": flight_queue.get_all()
    }


def get_pending_flights() -> dict:
    """
    Get the list of pending flights in the queue.

    Returns:
        dict: Dictionary with status, pending_count, and flights list
    """
    pending = flight_queue.get_all()
    
    return {
        "status": "success",
        "pending_count": flight_queue.size(),
        "flights": pending
    }


def process_one_flight(tree) -> dict:
    """
    Extract the first flight from the queue and insert it into the tree.

    Detects conflicts if the balance factor > 2.

    Args:
        tree: AVL tree instance

    Returns:
        dict: Dictionary containing:
            - status: Operation status
            - flight_inserted: Inserted flight data or null
            - tree_after: Serialized tree after insertion
            - conflict: Boolean indicating if conflict was detected
            - conflict_detail: Conflict description or null
            - queue_remaining: Number of flights remaining in queue
    """
    if flight_queue.is_empty():
        return {
            "status": "info",
            "message": "No hay vuelos en la cola",
            "flight_inserted": None,
            "tree_after": None,
            "conflict": False,
            "conflict_detail": None,
            "queue_remaining": 0
        }
    
    # Extraer vuelo de la cola
    flight_data = flight_queue.dequeue()
    codigo = flight_data.get("codigo")
    
    try:
        # Crear nodo e insertar en el árbol
        node = Node(codigo, flight_data)
        tree.insert(node)
        
        # Detectar conflictos si stress_mode y balance factor > 1
        root = tree.getRoot()
        bf = get_balance_factor(root)
        has_conflict = tree.stress_mode and abs(bf) > 1
        conflict_detail = None
        
        if has_conflict:
            if bf > 2:
                conflict_detail = f"Árbol muy inclinado a la izquierda (BF={bf}). Posible degradación de performance."
            else:
                conflict_detail = f"Árbol muy inclinado a la derecha (BF={bf}). Posible degradación de performance."
        
        # Serializar árbol actual
        tree_after = serialize_tree(tree, depth=0, depth_limit=tree.depth_limit)["root"]
        
        return {
            "status": "success",
            "message": f"Vuelo {codigo} procesado exitosamente",
            "flight_inserted": flight_data,
            "tree_after": tree_after,
            "conflict": has_conflict,
            "conflict_detail": conflict_detail,
            "queue_remaining": flight_queue.size()
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error al procesar vuelo: {str(e)}",
            "flight_inserted": flight_data,
            "tree_after": None,
            "conflict": False,
            "conflict_detail": None,
            "queue_remaining": flight_queue.size()
        }


def process_all_flights(tree) -> dict:
    """
    Process all flights from the queue one by one.

    Args:
        tree: AVL tree instance

    Returns:
        dict: Dictionary containing:
            - status: Operation status
            - total_processed: Number of flights processed
            - results: List of individual process results
            - tree_final: Final serialized tree
            - total_conflicts: Total number of conflicts detected
    """
    results = []
    total_conflicts = 0
    queue_size_initial = flight_queue.size()
    
    if queue_size_initial == 0:
        return {
            "status": "info",
            "message": "No hay vuelos en la cola para procesar",
            "total_processed": 0,
            "results": [],
            "tree_final": _serialize_tree_simple(tree.getRoot()),
            "total_conflicts": 0
        }
    
    # Procesar vuelos uno a uno
    for _ in range(queue_size_initial):
        result = process_one_flight(tree)
        results.append(result)
        
        if result.get("conflict", False):
            total_conflicts += 1
    
    # Serializar árbol final
    tree_final = _serialize_tree_simple(tree.getRoot())
    
    return {
        "status": "success",
        "message": f"Procesados {len(results)} vuelos de la cola",
        "total_processed": len(results),
        "results": results,
        "tree_final": tree_final,
        "total_conflicts": total_conflicts,
        "queue_remaining": flight_queue.size()
    }


def clear_queue() -> dict:
    """
    Clear the queue without processing anything.

    Returns:
        dict: Dictionary with status, message, and cleared_count
    """
    count = flight_queue.size()
    flight_queue.clear()
    
    return {
        "status": "success",
        "message": f"Cola vaciada. Se eliminaron {count} vuelos pendientes.",
        "cleared_count": count
    }


def _serialize_tree_simple(node):
    """
    Serialize tree in a simple format.

    Args:
        node: Root node of the tree to serialize

    Returns:
        dict or None: Serialized tree structure or None if node is None
    """
    if node is None:
        return None
    
    return {
        "value": node.getValue(),
        "codigo": node.getValue(),
        "left": _serialize_tree_simple(node.getLeftChild()),
        "right": _serialize_tree_simple(node.getRightChild())
    }
