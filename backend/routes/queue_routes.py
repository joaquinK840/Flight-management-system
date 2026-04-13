"""
Queue router for concurrency simulation.

Endpoints to add flights to queue, process them in FIFO order.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
# Import global AVL tree instance
from routes.avl_routes import avl
from services.queue_service import (add_flight_to_queue, clear_queue,
                                    get_pending_flights, process_all_flights,
                                    process_one_flight)

router = APIRouter(prefix="/queue", tags=["Queue - Concurrency"])


# =====================================
# Modelos Pydantic para validación
# =====================================

class FlightQueueRequest(BaseModel):
    """Model for adding flight to queue."""
    codigo: int
    origen: str
    destino: str
    horaSalida: str
    precioBase: float
    pasajeros: int
    prioridad: int


# =====================================
# ENDPOINTS
# =====================================

# Instancia del árbol será pasada como parámetro
# Se importará del módulo avl_routes en main.py

@router.post("/add")
def add_flight(flight: FlightQueueRequest):
    """
    Add a flight to the queue without processing it.

    Body:
        {
            "codigo": 100,
            "origen": "Madrid",
            "destino": "Barcelona",
            "horaSalida": "10:30",
            "precioBase": 150.0,
            "pasajeros": 180,
            "prioridad": 1
        }

    Returns:
        {
            "status": "success",
            "message": "Flight 100 added to queue",
            "queue_size": 3,
            "pending_flights": [...]
        }
    """
    flight_dict = flight.dict()
    result = add_flight_to_queue(flight_dict)
    return result


@router.get("/pending")
def get_pending():
    """
    Get the list of pending flights in the queue.

    Returns:
        {
            "status": "success",
            "pending_count": 3,
            "flights": [
                {"codigo": 100, "origen": "Madrid", ...},
                {"codigo": 50, "origen": "Valencia", ...},
                {"codigo": 150, "origen": "Malaga", ...}
            ]
        }
    """
    return get_pending_flights()


@router.post("/process-one")
def process_one():
    """
    Process the first flight from the queue.

    - Extract from queue
    - Insert into AVL tree
    - Detect conflicts (|balance_factor| > 2)

    Returns:
        {
            "status": "success",
            "message": "Flight 100 processed successfully",
            "flight_inserted": {...},
            "tree_after": {...},
            "conflict": false,
            "conflict_detail": null,
            "queue_remaining": 2
        }
    """
    result = process_one_flight(avl)
    return result


@router.post("/process-all")
def process_all():
    """
    Process all flights from the queue.

    - Extracts all flights in FIFO order
    - Inserts each one into the tree
    - Returns results of each insertion

    Returns:
        {
            "status": "success",
            "message": "Processed 5 flights from queue",
            "total_processed": 5,
            "results": [
                {
                    "status": "success",
                    "flight_inserted": {...},
                    "tree_after": {...},
                    "conflict": false
                },
                ...
            ],
            "tree_final": {...},
            "total_conflicts": 0,
            "queue_remaining": 0
        }
    """
    result = process_all_flights(avl)
    return result


@router.delete("/clear")
def clear():
    """
    Clear the queue without processing anything.

    Returns:
        {
            "status": "success",
            "message": "Queue cleared. 3 pending flights removed.",
            "cleared_count": 3
        }
    """
    result = clear_queue()
    return result
