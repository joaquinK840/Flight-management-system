from fastapi import APIRouter, UploadFile, HTTPException, File, Depends
from fastapi.responses import FileResponse, JSONResponse
import json
import io
from core.structures.node.node import Node
from core.shared_instances import avl
from services.metrics import get_metrics
from services.json_manager import load_trees_from_json, export_tree_to_json
from services.serialize_tree import serialize_tree
from services.stress_mode_service import rebalance_tree_postorder, audit_tree

router = APIRouter(prefix="/avl", tags=["AVL Tree"])

# instancias globales para comparacion AVL vs BST
bst_global = None
load_type_global = None


# -----------------------------
# TREE SERIALIZER (BASIC)
# -----------------------------
def serialize(node):
    """Serialize a node with its children using basic AVL structure."""

    if node is None:
        return None

    return {
        "value": node.getValue(),
        "left": serialize(node.getLeftChild()),
        "right": serialize(node.getRightChild())
    }


# -----------------------------
# INSERTAR NODO
# -----------------------------
@router.post("/insert/{value}")
def insert_value(value: int):
    """Insert a flight node into the AVL tree and return the updated tree."""

    node = Node(value)

    avl.insert(node)

    result = serialize_tree(avl, depth=0, depth_limit=avl.depth_limit)

    return {
        "message": "Nodo insertado",
        "root": avl.getRoot().getValue(),
        "tree": result["root"],
        "metrics": result.get("metrics"),
        "rotations": result.get("rotations"),
        "depth_limit": result.get("depth_limit")
    }


# -----------------------------
# OBTENER ARBOL COMPLETO
# -----------------------------
@router.get("/tree")
def get_tree():
    """Return the AVL tree serialized with depth-based pricing applied."""
    return serialize_tree(avl, depth=0, depth_limit=avl.depth_limit)


# ========================================
# PROFUNDIDAD CRITICA (DEPTH LIMIT)
# ========================================

@router.put("/config/depth-limit")
def update_depth_limit(request: dict):
    """Update depth limit and return a fully re-serialized tree."""
    try:
        new_limit = request.get("limit")

        if new_limit is None:
            raise HTTPException(status_code=400, detail="'limit' es requerido")

        if not isinstance(new_limit, int) or new_limit < 0:
            raise HTTPException(status_code=400, detail="'limit' debe ser un entero no negativo")

        # Actualizar el limite de profundidad
        avl.depth_limit = new_limit

        # Serializar con el nuevo limite (recalcula todos los precios)
        result = serialize_tree(avl, depth=0, depth_limit=new_limit)

        return {
            "status": "success",
            "message": f"Limite de profundidad actualizado a {new_limit}",
            "depth_limit": avl.depth_limit,
            "tree": result["root"],
            "metrics": result["metrics"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# -----------------------------
# BUSCAR VALOR
# -----------------------------
@router.get("/search/{value}")
def search_value(value: int):
    """Search for a node by value and report if found."""

    node = avl.search(value)

    if node is None:
        return {
            "found": False,
            "value": value
        }

    return {
        "found": True,
        "value": node.getValue()
    }


# -----------------------------
# REINICIAR ARBOL
# -----------------------------
@router.delete("/reset")
def reset_tree():
    """Reset the AVL tree state while preserving depth limit configuration."""

    current_depth_limit = avl.depth_limit
    avl.root = None
    avl.depth_limit = current_depth_limit
    avl.stress_mode = False
    avl.rotation_counts = {"LL": 0, "RR": 0, "LR": 0, "RL": 0}
    avl.mass_cancellation_count = 0

    return {
        "message": "Arbol reiniciado"
    }


# -----------------------------
# CARGAR ARBOLES DESDE JSON
# -----------------------------
@router.post("/load-file")
async def load_file(file: UploadFile = File(...)):
    """
    Load trees from a JSON file.

    Supports two modes:
    1. topology: rebuilds the exact JSON structure without balancing
    2. insertion: inserts flights one by one (AVL balanced, BST unbalanced)

    Returns:
        Dict with serialized trees, load type, and metrics for both
    """
    global avl, bst_global, load_type_global

    try:
        # Leer contenido del archivo
        content = await file.read()
        json_content = content.decode("utf-8")

        # Cargar arboles desde JSON
        loaded_avl, bst_global, load_type_global = load_trees_from_json(json_content)

        # Sincronizar la instancia compartida de AVL
        avl.root = loaded_avl.getRoot()
        avl.rotation_counts = loaded_avl.rotation_counts
        avl.mass_cancellation_count = loaded_avl.mass_cancellation_count
        avl.stress_mode = loaded_avl.stress_mode
        avl.depth_limit = loaded_avl.depth_limit

        # Serializar arboles
        avl_serialized = serialize_tree(avl, depth=0, depth_limit=avl.depth_limit)

        # Serializar BST manualmente (no tiene rotation_counts)
        def serialize_node(node):
            if node is None:
                return None
            return {
                "value": node.getValue(),
                "codigo": node.getValue(),
                "profundidad": 0,
                "datos": node.getDatos() if node.getDatos() else {},
                "left": serialize_node(node.getLeftChild()),
                "right": serialize_node(node.getRightChild())
            }

        bst_serialized = {
            "root": serialize_node(bst_global.getRoot()),
            "rotations": {}
        }

        # Calcular metricas
        def calculate_tree_metrics(tree):
            root = tree.getRoot()
            return {
                "height": root.getHeight() if root else 0,
                "leaves": tree.contar_hojas(),
                "total_nodes": tree.contar_nodos()
            }

        avl_metrics = calculate_tree_metrics(avl)
        bst_metrics = calculate_tree_metrics(bst_global)

        # Agregar rotaciones del AVL
        avl_metrics["rotations"] = avl.rotation_counts
        avl_metrics["total_rotations"] = sum(avl.rotation_counts.values())

        return {
            "status": "success",
            "load_type": load_type_global,
            "avl": {
                "tree": avl_serialized["root"],
                "metrics": avl_metrics
            },
            "bst": {
                "tree": bst_serialized["root"],
                "metrics": bst_metrics
            },
            "comparison": {
                "avl_height": avl_metrics["height"],
                "bst_height": bst_metrics["height"],
                "avl_rotations": avl_metrics["total_rotations"],
                "avl_optimized": True if avl_metrics["height"] <= bst_metrics["height"] else False
            }
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error en JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando archivo: {str(e)}")


# -----------------------------
# OBTENER METRICAS
# -----------------------------
@router.get("/metrics")
def get_tree_metrics():
    """Return real-time analytics for the AVL tree."""
    return get_metrics(avl)


# -----------------------------
# RECORRIDOS
# -----------------------------
@router.get("/traversal/{mode}")
def get_traversal(mode: str):
    """Return tree traversal in the specified order: pre, in, post, bfs."""
    from core.structures.avl_tree.traversal import (
        pre_order,
        in_order,
        post_order,
        breadth_first_traversal
    )

    root = avl.getRoot()
    traversal_map = {
        "pre": lambda: pre_order(root),
        "in": lambda: in_order(root),
        "post": lambda: post_order(root),
        "bfs": lambda: breadth_first_traversal(root)
    }

    if mode not in traversal_map:
        raise HTTPException(status_code=400, detail=f"Modo inválido: {mode}. Usar: pre, in, post, bfs")

    result = traversal_map[mode]()
    return {"mode": mode, "result": result, "count": len(result)}


# ========================================
# MODO ESTRES (STRESS MODE)
# ========================================


def verify_stress_mode_enabled():
    """Dependency guard that enforces stress mode being enabled."""
    if not avl.stress_mode:
        raise HTTPException(
            status_code=403,
            detail="Este endpoint solo esta disponible cuando stress_mode esta habilitado (POST /avl/stress-mode/enable)"
        )
    return True


@router.post("/stress-mode/enable")
def enable_stress_mode():
    """Enable stress mode to stop automatic AVL rebalancing."""
    avl.stress_mode = True

    return {
        "status": "success",
        "message": "Modo estres activado",
        "stress_mode": avl.stress_mode,
        "tree_info": {
            "total_nodes": avl.contar_nodos(),
            "total_leaves": avl.contar_hojas(),
            "height": avl.getRoot().getHeight() if avl.getRoot() else 0,
            "rotation_counts": avl.rotation_counts,
            "total_rotations": sum(avl.rotation_counts.values())
        }
    }


@router.post("/stress-mode/disable")
def disable_stress_mode():
    """Disable stress mode and keep the tree as-is until rebalance is triggered."""
    avl.stress_mode = False

    return {
        "status": "success",
        "message": "Modo estres desactivado. Llama a POST /avl/rebalance si necesitas rebalancear",
        "stress_mode": avl.stress_mode
    }


@router.post("/rebalance")
def rebalance_tree():
    """Rebalance the entire AVL tree in postorder when stress mode is off."""
    if avl.stress_mode:
        raise HTTPException(
            status_code=400,
            detail="No se puede rebalancear en stress_mode. Primero llama a POST /avl/stress-mode/disable"
        )

    if avl.getRoot() is None:
        return {
            "status": "success",
            "message": "Arbol vacio, no hay nada que rebalancear",
            "total_rotations": 0,
            "rotation_counts": {"LL": 0, "RR": 0, "LR": 0, "RL": 0},
            "nodes_rebalanced": 0,
            "imbalanced_before": []
        }

    result = rebalance_tree_postorder(avl)
    result["status"] = "success"
    return result


@router.get("/audit", dependencies=[Depends(verify_stress_mode_enabled)])
def audit_tree_integrity():
    """Audit AVL invariants while stress mode is enabled."""
    result = audit_tree(avl)
    result["status"] = "success"
    return result


# ========================================
# EXPORTAR ARBOL A JSON
# ========================================
@router.get("/export")
def export_tree_endpoint():
    """Export the AVL tree as a JSON file using the topology format."""
    try:
        # Verificar que el arbol no este vacio
        if avl.getRoot() is None:
            raise HTTPException(status_code=400, detail="El arbol esta vacio, no se puede exportar")

        # Exportar arbol a estructura JSON
        export_data = export_tree_to_json(avl)

        # Convertir a JSON string
        json_str = json.dumps(export_data, indent=2, ensure_ascii=False)

        # Crear BytesIO para simular archivo
        json_bytes = json_str.encode("utf-8")

        # Retornar como FileResponse para descarga
        return FileResponse(
            io.BytesIO(json_bytes),
            media_type="application/json",
            headers={
                "Content-Disposition": "attachment; filename=skybalance_avl.json"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exportando arbol: {str(e)}")


@router.get("/export-json")
def export_tree_json():
    """Export the full tree structure with all computed fields for reimport."""
    try:
        if avl.getRoot() is None:
            raise HTTPException(status_code=400, detail="El arbol esta vacio, no se puede exportar")

        export_data = export_tree_to_json(avl)

        return JSONResponse(
            content=export_data,
            headers={"Content-Disposition": "attachment; filename=avl_tree.json"}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exportando arbol: {str(e)}")
