"""
Version management API routes.

Provides REST endpoints for saving, restoring, and managing
tree and queue versions.
"""

import json
from typing import Optional

from controllers.version_controller import VersionController
from core.shared_instances import avl, flight_queue  # Use shared instances
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/versions", tags=["Versions"])

# Global instance of version controller
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
    Save the current state of the tree AND QUEUE as a new version.

    Serializes the complete hierarchical structure of the tree.

    Args:
        request: { "name": "Version name" }

    Returns:
        Confirmation, timestamp, and list of available versions
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
    Return list of all saved versions.

    Returns:
        List of version names with information
    """
    try:
        result = version_controller.list_versions()
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando versiones: {str(e)}")


@router.post("/restore/{name}")
def restore_version(name: str):
    """
    Restore the tree AND QUEUE from a saved version.

    Reconstructs exactly the original topology with the same heights.

    Args:
        name: Name of the version to restore

    Returns:
        Restored serialized tree with metrics and queue status
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
    Delete a saved version.

    Args:
        name: Name of the version to delete

    Returns:
        Confirmation and list of remaining versions
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
    Get detailed information about a specific version.

    Args:
        name: Version name

    Returns:
        Information: timestamp, metrics, tree type
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
    Overwrite an existing version with the current tree state.

    Args:
        name: Name of the version to overwrite

    Returns:
        Confirmation and new timestamp
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
    Compare two versions and return their differences.

    Args:
        version1: First version
        version2: Second version

    Returns:
        Comparison of metrics (height, nodes, leaves, rotations)
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
    Delete ALL saved versions.

    ⚠️ IRREVERSIBLE OPERATION

    Returns:
        Deletion confirmation
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
