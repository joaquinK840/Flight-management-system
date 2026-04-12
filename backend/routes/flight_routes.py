from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from services.tree_repository import TreeRepository
from services.profitability_service import find_least_profitable, count_subtree_size
from core.structures.avl_tree.tree import AVL
from core.shared_instances import flight_repository, flight_queue  # Usar instancias compartidas

router = APIRouter(prefix="/flights", tags=["Flights"])


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
    Inserta un nuevo vuelo en el árbol.
    
    Si tree.stress_mode == False: Usa AVL con balanceo
    Si tree.stress_mode == True: Usa BST sin balanceo
    
    Args:
        flight: Datos del vuelo
        
    Returns:
        Árbol serializado y estado de la operación
    """
    try:
        flight_dict = flight.dict()
        
        # Calcular precioFinal si no viene
        if flight_dict.get("precioFinal") is None:
            precio_base = flight_dict.get("precioBase", 0)
            promocion = flight_dict.get("promocion", False)
            flight_dict["precioFinal"] = precio_base * 0.9 if promocion else precio_base
        
        result = flight_repository.insert_flight(flight_dict)
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error insertando vuelo: {str(e)}")


@router.delete("/delete/{codigo}")
def delete_flight(codigo: int):
    """
    Elimina un vuelo específico del árbol.
    El sucesor inorder reemplaza al nodo eliminado.
    
    Args:
        codigo: Código del vuelo a eliminar
        
    Returns:
        Árbol serializado actualizado
    """
    try:
        result = flight_repository.delete_flight(codigo)
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando vuelo: {str(e)}")


@router.delete("/cancel/{codigo}")
def cancel_flight_subtree(codigo: int):
    """
    Cancela un vuelo Y TODOS SUS DESCENDIENTES.
    Incrementa el contador de cancelaciones masivas.
    
    Args:
        codigo: Código del vuelo raíz del subárbol a cancelar
        
    Returns:
        Árbol serializado, contador de cancelaciones masivas
    """
    try:
        result = flight_repository.cancel_flight_subtree(codigo)
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cancelando vuelo: {str(e)}")


@router.put("/update/{codigo}")
def update_flight(codigo: int, flight_update: FlightUpdate):
    """
    Actualiza los datos de un vuelo sin cambiar su posición en el árbol.
    
    Args:
        codigo: Código del vuelo
        flight_update: Datos a actualizar (solo campos no nulos se aplican)
        
    Returns:
        Árbol serializado actualizado
    """
    try:
        # Filtrar solo los campos que vienen (no nulos)
        updated_fields = {k: v for k, v in flight_update.dict().items() if v is not None}
        
        if not updated_fields:
            raise ValueError("Al menos un campo debe ser actualizado")
        
        result = flight_repository.update_flight(codigo, updated_fields)
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando vuelo: {str(e)}")


@router.post("/undo")
def undo_operation():
    """
    Revierte la última operación del árbol.
    
    Returns:
        Árbol serializado del estado anterior
    """
    try:
        result = flight_repository.undo()
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error revirtiendo operación: {str(e)}")


@router.post("/redo")
def redo_operation():
    """
    Rehace la última operación desecha.
    
    Returns:
        Árbol serializado del estado rehecho
    """
    try:
        result = flight_repository.redo()
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rehaciendo operación: {str(e)}")


@router.get("/metrics")
def get_flight_metrics():
    """
    Retorna métricas del árbol actual.
    
    Returns:
        Dict con altura, hojas, nodos, rotaciones, etc.
    """
    try:
        metrics = flight_repository.get_tree_metrics()
        return {"status": "success", "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo métricas: {str(e)}")


@router.get("/tree")
def get_tree():
    """
    Retorna el árbol serializado completo.
    
    Returns:
        Árbol serializado con todos los datos de vuelos
    """
    try:
        tree_data = flight_repository._get_serialized_tree()
        return {"status": "success", "tree": tree_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo árbol: {str(e)}")


@router.post("/stress-mode/{enabled}")
def toggle_stress_mode(enabled: bool):
    """
    Activa/desactiva stress_mode.
    
    En stress_mode:
    - AVL no aplica rotaciones (solo actualiza alturas)
    - Inserciones se comportan como BST
    
    Args:
        enabled: True para activar, False para desactivar
        
    Returns:
        Estado actualizado
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
    Reinicia el árbol, la cola FIFO y limpia la pila de undo.
    Limpia completamente el sistema.
    
    Returns:
        Confirmación de reinicio
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
    Elimina el nodo con MENOR rentabilidad del árbol.
    
    Proceso:
    1. Recorrer TODO el árbol calculando rentabilidad de cada nodo
    2. Encontrar el nodo de menor rentabilidad
    3. Criterios de desempate:
       a) Si hay empate, tomar el más lejano a raíz (mayor profundidad)
       b) Si sigue empate, tomar el de código más grande
    4. Cancelar ese nodo (eliminar + descendientes)
    5. Rebalancear el árbol
    
    Returns:
        {
            "status": "success",
            "message": "Vuelo de menor rentabilidad eliminado",
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
