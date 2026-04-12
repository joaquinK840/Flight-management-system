"""
Router de Cola para simulación de concurrencia.
Endpoints para agregar vuelos a la cola, procesarlos por orden FIFO.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.queue_service import (
    add_flight_to_queue,
    get_pending_flights,
    process_one_flight,
    process_all_flights,
    clear_queue
)

# Importar instancia global del árbol AVL
from routes.avl_routes import avl

router = APIRouter(prefix="/queue", tags=["Queue - Concurrencia"])


# =====================================
# Modelos Pydantic para validación
# =====================================

class FlightQueueRequest(BaseModel):
    """Modelo para agregar vuelo a la cola."""
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
    Agregar un vuelo a la cola sin procesarlo.
    
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
            "message": "Vuelo 100 agregado a la cola",
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
    Obtener la lista de vuelos pendientes en la cola.
    
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
    Procesar el primer vuelo de la cola.
    - Extraer de la cola
    - Insertar en el árbol AVL
    - Detectar conflictos (|balance_factor| > 2)
    
    Returns:
        {
            "status": "success",
            "message": "Vuelo 100 procesado exitosamente",
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
    Procesar todos los vuelos de la cola.
    - Extrae todos los vuelos en orden FIFO
    - Inserta cada uno en el árbol
    - Retorna resultados de cada inserción
    
    Returns:
        {
            "status": "success",
            "message": "Procesados 5 vuelos de la cola",
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
    Vaciar la cola sin procesar nada.
    
    Returns:
        {
            "status": "success",
            "message": "Cola vaciada. Se eliminaron 3 vuelos pendientes.",
            "cleared_count": 3
        }
    """
    result = clear_queue()
    return result
