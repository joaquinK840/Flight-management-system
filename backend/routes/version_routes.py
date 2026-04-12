from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
from controllers.version_controller import VersionController
from core.shared_instances import avl, flight_queue  # Usar instancias compartidas

router = APIRouter(prefix="/versions", tags=["Versions"])

# Instancia global del controlador de versiones
version_controller = VersionController()


# =====================
# MODELOS PYDANTIC
# =====================
class VersionSaveRequest(BaseModel):
    name: str


class VersionRestoreRequest(BaseModel):
    pass


# =====================
# ENDPOINTS
# =====================

@router.post("/save")
def save_version(request: VersionSaveRequest):
    """
    Guarda el estado actual del árbol Y COLA como una nueva versión.
    Serializa la estructura jerárquica completa del árbol.
    
    Args:
        request: { "name": "Nombre de la versión" }
        
    Returns:
        Confirmación, timestamp, y lista de versiones disponibles
    """
    try:
        result = version_controller.save_version(avl, request.name, flight_queue)
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando versión: {str(e)}")


@router.get("/list")
def list_versions():
    """
    Retorna lista de todas las versiones guardadas.
    
    Returns:
        Lista de nombres de versiones con información
    """
    try:
        result = version_controller.list_versions()
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando versiones: {str(e)}")


@router.post("/restore/{name}")
def restore_version(name: str):
    """
    Restaura el árbol Y COLA desde una versión guardada.
    Reconstruye exactamente la topología original con las mismas alturas.
    
    Args:
        name: Nombre de la versión a restaurar
        
    Returns:
        Árbol serializado restaurado con métricas y estado de cola
    """
    try:
        result = version_controller.restore_version(avl, name, flight_queue)
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error restaurando versión: {str(e)}")


@router.delete("/{name}")
def delete_version(name: str):
    """
    Elimina una versión guardada.
    
    Args:
        name: Nombre de la versión a eliminar
        
    Returns:
        Confirmación y lista de versiones restantes
    """
    try:
        result = version_controller.delete_version(name)
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando versión: {str(e)}")


@router.get("/{name}/info")
def get_version_info(name: str):
    """
    Obtiene información detallada de una versión específica.
    
    Args:
        name: Nombre de la versión
        
    Returns:
        Información: timestamp, métricas, tipo de árbol
    """
    try:
        info = version_controller.version_service.get_version_info(name)
        return {
            "status": "success",
            "version": info
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo info: {str(e)}")


@router.post("/{name}/overwrite")
def overwrite_version(name: str):
    """
    Sobrescribe una versión existente con el estado actual del árbol.
    
    Args:
        name: Nombre de la versión a sobrescribir
        
    Returns:
        Confirmación y nuevo timestamp
    """
    try:
        result = version_controller.version_service.overwrite_version(avl, name)
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sobrescribiendo versión: {str(e)}")


@router.post("/compare/{version1}/vs/{version2}")
def compare_versions(version1: str, version2: str):
    """
    Compara dos versiones y retorna sus diferencias.
    
    Args:
        version1: Primera versión
        version2: Segunda versión
        
    Returns:
        Comparación de métricas (altura, nodos, hojas, rotaciones)
    """
    try:
        result = version_controller.version_service.compare_versions(version1, version2)
        return {
            "status": "success",
            "comparison": result
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparando versiones: {str(e)}")


@router.delete("/clear/all")
def clear_all_versions():
    """
    Elimina TODAS las versiones guardadas.
    ⚠️ OPERACIÓN IRREVERSIBLE
    
    Returns:
        Confirmación de eliminación
    """
    try:
        result = version_controller.version_service.clear_all_versions()
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error limpiando versiones: {str(e)}")


@router.get("/{name}/export")
def export_version_as_json(name: str):
    """
    Exporta una versión como JSON completo.
    Útil para compartir o guardar en archivo.
    
    Args:
        name: Nombre de la versión
        
    Returns:
        JSON con toda la información de la versión
    """
    try:
        json_data = version_controller.version_service.export_version_as_json(name)
        return {
            "status": "success",
            "version_name": name,
            "json": json.loads(json_data)
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exportando versión: {str(e)}")


@router.post("/duplicate/{source_name}/{dest_name}")
def duplicate_version(source_name: str, dest_name: str):
    """
    Crea una copia de una versión existente con un nuevo nombre.
    
    Args:
        source_name: Versión origen a copiar
        dest_name: Nombre para la nueva copia
        
    Returns:
        Confirmación de duplicación
    """
    try:
        result = version_controller.duplicate_version(source_name, dest_name)
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error duplicando versión: {str(e)}")
