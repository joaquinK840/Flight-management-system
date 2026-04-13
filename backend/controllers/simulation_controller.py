"""
Queue simulation controller for flight processing.

This module handles queue management and simulation processing used by
/avl/queue endpoints. Provides wrappers around the shared queue and tree insertion.
"""

from core.shared_instances import flight_queue
from core.structures.avl_tree.balance import get_balance_factor
from core.structures.node.node import Node


def enqueue_flight(flight: dict) -> dict:
    """
    Add a flight to the shared queue without inserting into the tree.

    Args:
        flight (dict): Flight data dictionary

    Returns:
        dict: Response with message, queue size, and pending flights list
    """
    flight_queue.enqueue(flight)
    return {
        "message": f"Flight {flight.get('codigo')} added to queue",
        "queue_size": flight_queue.size(),
        "pending_flights": flight_queue.get_all()
    }


def list_queue() -> list:
    """
    Return all queued flights as a list.

    Returns:
        list: List of all pending flight dictionaries
    """
    return flight_queue.get_all()


def process_next(avl, bst=None) -> dict:
    """
    Process one queued flight, inserting into AVL and optional BST.

    Dequeues one flight and inserts it into both trees. Detects balance conflicts
    if AVL is in stress mode and balance factor exceeds 1.

    Args:
        avl: AVL tree instance (required)
        bst: BST tree instance (optional)

    Returns:
        dict: Processing result with flight data, remaining count, and conflict status
    """
    if flight_queue.is_empty():
        return {
            "processed": None,
            "remaining": 0,
            "message": "No flights in queue"
        }

    flight_data = flight_queue.dequeue()
    codigo = flight_data.get("codigo")

    node_avl = Node(codigo, datos=flight_data)
    avl.insert(node_avl)

    if bst is not None:
        node_bst = Node(codigo, datos=flight_data)
        bst.insert(node_bst)

    balance_conflict = False
    if getattr(avl, "stress_mode", False):
        bf = get_balance_factor(avl.getRoot()) if avl.getRoot() else 0
        balance_conflict = abs(bf) > 1

    return {
        "processed": True,
        "remaining": flight_queue.size(),
        "flight_inserted": flight_data,
        "balance_conflict": balance_conflict
    }


def clear_queue() -> dict:
    """
    Clear the shared queue and return the number of removed items.

    Returns:
        dict: Response with cleared count and confirmation message
    """
    count = flight_queue.size()
    flight_queue.clear()
    return {
        "cleared_count": count,
        "message": f"Queue cleared. Removed {count} pending flights."
    }
