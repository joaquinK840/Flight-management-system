"""
Flight management API routes.

Provides REST endpoints for flight CRUD operations, profitability analysis,
and tree synchronization.
"""

from typing import Optional

from core.shared_instances import avl as shared_avl
from core.shared_instances import (flight_queue,  # Use shared instances
                                   flight_repository)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.profitability_service import (count_subtree_size,
                                            find_least_profitable)

router = APIRouter(prefix="/flights", tags=["Flights"])


def _sync_shared_avl_from_repo():
    """
    Keep shared AVL in sync with repository tree state.

    Synchronizes the shared AVL instance with the current tree state
    from the flight repository, copying all relevant attributes.
    """
    tree = flight_repository.tree
    if tree is None:
        return
    if hasattr(tree, "getRoot"):
        shared_avl.root = tree.getRoot()
    else:
        shared_avl.root = getattr(tree, "root", None)
    if hasattr(tree, "rotation_counts"):
        shared_avl.rotation_counts = tree.rotation_counts.copy()
    if hasattr(tree, "mass_cancellation_count"):
        shared_avl.mass_cancellation_count = tree.mass_cancellation_count
    if hasattr(tree, "stress_mode"):
        shared_avl.stress_mode = tree.stress_mode
    if hasattr(tree, "depth_limit"):
        shared_avl.depth_limit = tree.depth_limit


# =====================
# MODELOS PYDANTIC
# =====================
class FlightCreate(BaseModel):
    codigo: int
    origen: str
    destino: str
    horaSalida: str
    precioBase: float
    pasajeros: int
    prioridad: int
    promocion: bool = False
    alerta: str = "normal"
    precioFinal: Optional[float] = None


class FlightUpdate(BaseModel):
    origen: Optional[str] = None
    destino: Optional[str] = None
    horaSalida: Optional[str] = None
    precioBase: Optional[float] = None
    pasajeros: Optional[int] = None
    prioridad: Optional[int] = None
    promocion: Optional[bool] = None
    alerta: Optional[str] = None
    precioFinal: Optional[float] = None


# =====================
# ENDPOINTS
# =====================

@router.post("/insert")
def insert_flight(flight: FlightCreate):
    """
    Insert a new flight into the tree.

    If tree.stress_mode == False: Uses AVL with balancing
    If tree.stress_mode == True: Uses BST without balancing

    Args:
        flight: Flight data

    Returns:
        Serialized tree and operation status
    """
    try:
        flight_dict = flight.dict()
        
        # Calcular precioFinal si no viene
        if flight_dict.get("precioFinal") is None:
            precio_base = flight_dict.get("precioBase", 0)
            promocion = flight_dict.get("promocion", False)
            flight_dict["precioFinal"] = precio_base * 0.9 if promocion else precio_base
        
        result = flight_repository.insert_flight(flight_dict)
        _sync_shared_avl_from_repo()
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error insertando vuelo: {str(e)}")


@router.delete("/delete/{codigo}")
def delete_flight(codigo: int):
    """
    Delete a specific flight from the tree.

    The inorder successor replaces the deleted node.

    Args:
        codigo: Code of the flight to delete

    Returns:
        Updated serialized tree
    """
    try:
        result = flight_repository.delete_flight(codigo)
        _sync_shared_avl_from_repo()
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        message = str(e)
        if "No se encontró" in message or "no encontrado" in message:
            raise HTTPException(status_code=404, detail=message)
        raise HTTPException(status_code=500, detail=f"Error eliminando vuelo: {message}")


@router.delete("/cancel/{codigo}")
def cancel_flight_subtree(codigo: int):
    """
    Cancel a flight AND ALL ITS DESCENDANTS.

    Increments the mass cancellation counter.

    Args:
        codigo: Code of the root flight of the subtree to cancel

    Returns:
        Serialized tree, mass cancellation counter
    """
    try:
        result = flight_repository.cancel_flight_subtree(codigo)
        _sync_shared_avl_from_repo()
        _sync_shared_avl_from_repo()
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cancelando vuelo: {str(e)}")


@router.put("/update/{codigo}")
def update_flight(codigo: int, flight_update: FlightUpdate):
    """
    Update flight data without changing its position in the tree.

    Args:
        codigo: Flight code
        flight_update: Data to update (only non-null fields are applied)

    Returns:
        Updated serialized tree
    """
    try:
        # Filtrar solo los campos que vienen (no nulos)
        updated_fields = {k: v for k, v in flight_update.dict().items() if v is not None}
        
        if not updated_fields:
            raise ValueError("Al menos un campo debe ser actualizado")
        
        result = flight_repository.update_flight(codigo, updated_fields)
        _sync_shared_avl_from_repo()
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando vuelo: {str(e)}")


@router.post("/undo")
def undo_operation():
    """
    Revert the last tree operation.

    Returns:
        Serialized tree from the previous state
    """
    try:
        result = flight_repository.undo()
        _sync_shared_avl_from_repo()
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error revirtiendo operación: {str(e)}")


@router.post("/redo")
def redo_operation():
    """
    Redo the last undone operation.

    Returns:
        Serialized tree from the redone state
    """
    try:
        result = flight_repository.redo()
        _sync_shared_avl_from_repo()
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rehaciendo operación: {str(e)}")


@router.get("/metrics")
def get_flight_metrics():
    """
    Return current tree metrics.

    Returns:
        Dict with height, leaves, nodes, rotations, etc.
    """


@router.get("/tree")
def get_tree():
    """
    Return the complete serialized tree.

    Returns:
        Serialized tree with all flight data
    """
    try:
        tree_data = flight_repository._get_serialized_tree()
        return {"status": "success", "tree": tree_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo árbol: {str(e)}")


@router.post("/stress-mode/{enabled}")
def toggle_stress_mode(enabled: bool):
    """
    Enable/disable stress_mode.

    In stress_mode:
    - AVL does not apply rotations (only updates heights)
    - Insertions behave like BST

    Args:
        enabled: True to enable, False to disable

    Returns:
        Updated status
    """
    try:
        if hasattr(flight_repository.tree, 'stress_mode'):
            flight_repository.tree.stress_mode = enabled
            return {
                "status": "success",
                "stress_mode": enabled,
                "message": "Stress mode " + ("activado" if enabled else "desactivado")
            }
        else:
            raise ValueError("Tree no soporta stress_mode")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/reset")
def reset_tree():
    """
    Reset the tree, FIFO queue and clear undo stack.

    Completely cleans the system.

    Returns:
        Reset confirmation
    """
    try:
        # Limpiar el árbol AVL completamente
        flight_repository.tree.root = None
        flight_repository.tree.rotation_counts = {"LL": 0, "RR": 0, "LR": 0, "RL": 0}
        flight_repository.tree.mass_cancellation_count = 0
        flight_repository.tree.stress_mode = False
        flight_repository.tree.depth_limit = 3
        
        # Limpiar la cola FIFO
        flight_queue.clear()
        
        # Limpiar historial de undo/redo
        flight_repository.undo_stack = []
        flight_repository.redo_stack = []
        
        return {
            "status": "success",
            "message": "Sistema reiniciado completamente: Árbol, cola y historial"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/eliminate-least-profitable")
def eliminate_least_profitable():
    """
    Eliminate the node with LEAST profitability from the tree.

    Process:
    1. Traverse the ENTIRE tree calculating profitability of each node
    2. Find the node with least profitability
    3. Tie-breaking criteria:
       a) If tie, take the farthest from root (greater depth)
       b) If still tie, take the one with highest code
    4. Cancel that node (delete + descendants)
    5. Rebalance the tree

    Returns:
        {
            "status": "success",
            "message": "Flight with least profitability eliminated",
            "eliminated_code": int,
            "eliminated_rentability": float,
            "subtree_size_removed": int,
            "tree": serialized tree
        }
    """
    try:
        # Obtener árbol del repositorio
        tree = flight_repository.tree
        
        # Encontrar nodo de menor rentabilidad
        least_profitable_node, rentability, codigo, profundidad = find_least_profitable(tree)
        
        if least_profitable_node is None:
            raise ValueError("No se encontró nodo para eliminar")
        
        # Contar cuántos nodos se van a eliminar (subárbol)
        subtree_size = count_subtree_size(least_profitable_node)
        
        # Cancelar (eliminar nodo + descendientes)
        result = flight_repository.cancel_flight_subtree(codigo)
        _sync_shared_avl_from_repo()
        
        return {
            "status": "success",
            "message": f"Vuelo {codigo} (menor rentabilidad) eliminado con {subtree_size - 1} descendientes",
            "eliminated_code": codigo,
            "eliminated_rentability": round(float(rentability), 2),
            "subtree_size_removed": subtree_size,
            "profundidad": profundidad,
            "tree": result["tree"],
            "mass_cancellations": result.get("mass_cancellations", 0)
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando vuelo: {str(e)}")
