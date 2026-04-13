"""
Queue simulation controller used by /avl/queue endpoints.
Provides minimal wrappers around the shared queue and tree insertion.
"""

from core.shared_instances import flight_queue
from core.structures.node.node import Node
from core.structures.avl_tree.balance import get_balance_factor


def enqueue_flight(flight: dict) -> dict:
	"""Add a flight to the shared queue without inserting into the tree."""
	flight_queue.enqueue(flight)
	return {
		"message": f"Vuelo {flight.get('codigo')} agregado a la cola",
		"queue_size": flight_queue.size(),
		"pending_flights": flight_queue.get_all()
	}


def list_queue() -> list:
	"""Return all queued flights as a list."""
	return flight_queue.get_all()


def process_next(avl, bst=None) -> dict:
	"""Process one queued flight, inserting into AVL and optional BST."""
	if flight_queue.is_empty():
		return {
			"processed": None,
			"remaining": 0,
			"message": "No hay vuelos en la cola"
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
	"""Clear the shared queue and return the number of removed items."""
	count = flight_queue.size()
	flight_queue.clear()
	return {
		"cleared_count": count,
		"message": f"Cola vaciada. Se eliminaron {count} vuelos pendientes."
	}
