from fastapi import APIRouter, UploadFile, HTTPException, File, Depends
from fastapi.responses import FileResponse
import json
import io
from core.structures.avl_tree.tree import AVL
from core.structures.avl_tree import traversal
from core.structures.node.node import Node
from services.metrics import get_metrics
from services.json_manager import load_trees_from_json, export_tree_to_json
from services.serialize_tree import serialize_tree
from services.stress_mode_service import rebalance_tree_postorder, audit_tree
from core.shared_instances import avl, flight_queue  # Usar instancias compartidas

router = APIRouter(prefix="/avl", tags=["AVL Tree"])

# instancias globales para comparación AVL vs BST
bst_global = None
load_type_global = None


# -----------------------------
# SERIALIZADOR DEL ÁRBOL
# -----------------------------
def serialize(node):

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

    node = Node(value)

    avl.insert(node)

    return {
        "message": "Nodo insertado",
        "root": avl.getRoot().getValue(),
        "tree": serialize(avl.getRoot())
    }


# -----------------------------
# OBTENER ÁRBOL COMPLETO
# -----------------------------
@router.get("/tree")
def get_tree():
    """
    Obtiene el árbol serializado con precios calculados según profundidad crítica.
    - Usa tree.depth_limit para determinar qué nodos aplican penalización de 25%
    - Recalcula precios en cada llamada según depth_limit actual
    """
    return serialize_tree(avl)


# ========================================
# PROFUNDIDAD CRÍTICA (DEPTH LIMIT)
# ========================================

@router.put("/depth-limit")
def update_depth_limit(request: dict):
    """
    Actualiza el límite de profundidad crítica del árbol.
    - Todos los precios se recalculan automáticamente
    - Nodos en profundidad > limit tienen penalización del 25%
    - Nodos en profundidad <= limit carecen de penalización
    
    Body:
        { "limit": 4 }
        
    Returns:
        Árbol completo serializado con precios recalculados según nuevo limite
    """
    try:
        new_limit = request.get("limit")
        
        if new_limit is None:
            raise HTTPException(status_code=400, detail="'limit' es requerido")
        
        if not isinstance(new_limit, int) or new_limit < 0:
            raise HTTPException(status_code=400, detail="'limit' debe ser un entero no negativo")
        
        # Actualizar el límite de profundidad
        avl.depth_limit = new_limit
        
        # Serializar con el nuevo límite (recalcula todos los precios)
        result = serialize_tree(avl, depth_limit=new_limit)
        
        return {
            "status": "success",
            "message": f"Límite de profundidad actualizado a {new_limit}",
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


@router.delete("/reset")
def reset_tree():
    """
    Reinicia el árbol AVL Y la cola FIFO al estado inicial.
    Limpia completamente el sistema como si fuera nuevo.
    """
    # Limpiar el árbol AVL
    avl.root = None
    avl.rotation_counts = {"LL": 0, "RR": 0, "LR": 0, "RL": 0}
    avl.mass_cancellation_count = 0
    avl.stress_mode = False
    avl.depth_limit = 3
    
    # Limpiar la cola FIFO
    flight_queue.clear()

    return {
        "message": "Árbol y cola reiniciados completamente",
        "status": "success"
    }


# -----------------------------
# CARGAR ÁRBOLES DESDE JSON
# -----------------------------
@router.post("/load-file")
async def load_file(file: UploadFile = File(...)):
    """
    Carga árboles desde archivo JSON.
    
    Soporta dos modos:
    1. topology: Reconstruye exactamente la estructura del JSON sin balanceo
    2. insertion: Inserta vuelos uno a uno (AVL con balanceo, BST sin balanceo)
    
    Returns:
        Dict con árboles serializados, tipo de carga, y métricas de ambos
    """
    global avl, bst_global, load_type_global

    try:
        # Leer contenido del archivo
        content = await file.read()
        json_content = content.decode("utf-8")

        # Cargar árboles desde JSON
        avl, bst_global, load_type_global = load_trees_from_json(json_content)

        # Serializar árboles
        avl_serialized = serialize_tree(avl)
        
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

        # Calcular métricas
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


# -----------------------------
# OBTENER MÉTRICAS
# -----------------------------
@router.get("/metrics")
def get_tree_metrics():
    """Get real-time analytics for the AVL tree."""
    return get_metrics(avl)


# ========================================
# MODO ESTRÉS (STRESS MODE)  
# ========================================

def verify_stress_mode_enabled():
    """
    Dependency: Verifica que stress_mode esté habilitado.
    Lanza HTTPException 403 si no lo está.
    """
    if not avl.stress_mode:
        raise HTTPException(
            status_code=403,
            detail="Este endpoint solo está disponible cuando stress_mode está habilitado (POST /avl/stress-mode/enable)"
        )
    return True


@router.post("/stress-mode/enable")
def enable_stress_mode():
    """
    Activa el modo estrés.
    - Establece tree.stress_mode = True
    - El árbol usa BST (sin balanceo automático durante inserciones/eliminaciones)
    - Respeta check_balance() que solo actualiza alturas pero no rota
    
    Returns:
        dict con confirmación y estado actual del árbol
    """
    avl.stress_mode = True
    
    return {
        "status": "success",
        "message": "Modo estrés activado",
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
    """
    Desactiva el modo estrés.
    - Establece tree.stress_mode = False
    - El árbol vuelve a usar AVL (balanceo automático en inserciones/eliminaciones)
    - NO hace rebalanceo automático aquí (el usuario debe llamar a POST /avl/rebalance)
    
    Returns:
        dict con confirmación
    """
    avl.stress_mode = False
    
    return {
        "status": "success",
        "message": "Modo estrés desactivado. Llama a POST /avl/rebalance si necesitas rebalancear",
        "stress_mode": avl.stress_mode
    }


@router.post("/rebalance")
def rebalance_tree():
    """
    Rebalancea el árbol completo en postorden.
    - Solo disponible cuando stress_mode == False
    - Recorre todos los nodos en postorden (hojas primero)
    - Para cada nodo desbalanceado (|factor| > 1), aplica rotación necesaria
    - Registra rotaciones en tree.rotation_counts
    
    Returns:
        dict con:
        - total_rotations: rotaciones aplicadas en esta operación
        - rotation_counts: desglose por tipo (LL, RR, LR, RL)
        - nodes_rebalanced: cantidad de nodos que estaban desbalanceados
        - imbalanced_before: lista de nodos desbalanceados encontrados
        - current_tree_metrics: altura y nodos después del rebalanceo
    """
    if avl.stress_mode:
        raise HTTPException(
            status_code=400,
            detail="No se puede rebalancear en stress_mode. Primero llama a POST /avl/stress-mode/disable"
        )
    
    if avl.getRoot() is None:
        return {
            "status": "success",
            "message": "Árbol vacío, no hay nada que rebalancear",
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
    """
    Audita la integridad del árbol AVL (SOLO EN STRESS_MODE).
    - Verifica factor de balance ∈ {-1, 0, 1} para todos los nodos
    - Verifica altura correcta según fórmula: 1 + max(left_h, right_h)
    - Disponible SOLO cuando stress_mode == True (Dependency Injection)
    
    Returns:
        dict con:
        - valid: bool indicando si el árbol tiene integridad
        - nodes_checked: cantidad de nodos verificados
        - inconsistent_nodes: lista de nodos con problemas (sin problemas si valid==True)
    
    HTTP 403:
        Si stress_mode == False
    """
    result = audit_tree(avl)
    result["status"] = "success"
    return result


# ========================================
# EXPORTAR ÁRBOL A JSON
# ========================================
@router.get("/export")
def export_tree_endpoint():
    """
    Exporta el árbol AVL completo a un archivo JSON.
    
    Guarda la estructura real del árbol (no solo lista de vuelos).
    El JSON exportado puede ser recargado exactamente con POST /avl/load-file
    (idempotencia: exportar + reimportar produce el mismo árbol).
    
    Returns:
        FileResponse (JSON file):
            filename="skybalance_avl.json"
            
            Contenido:
            {
              "type": "topology",
              "depth_limit": 3,
              "rotation_counts": {"LL": 2, "RR": 1, "LR": 0, "RL": 0},
              "mass_cancellation_count": 0,
              "root": {
                "codigo": 100,
                "height": 3,
                "balance_factor": 0,
                "profundidad": 0,
                "datos": {...},
                "left": {...},
                "right": {...}
              }
            }
            
    HTTP 400:
        Si el árbol está vacío
    HTTP 500:
        Si hay error exportando
    """
    try:
        # Verificar que el árbol no esté vacío
        if avl.getRoot() is None:
            raise HTTPException(status_code=400, detail="El árbol está vacío, no se puede exportar")
        
        # Exportar árbol a estructura JSON
        export_data = export_tree_to_json(avl)
        
        # Convertir a JSON string
        json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
        
        # Crear BytesIO para simular archivo
        json_bytes = json_str.encode('utf-8')
        
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
        raise HTTPException(status_code=500, detail=f"Error exportando árbol: {str(e)}")


# ========================================
# RECORRIDOS DEL ÁRBOL
# ========================================
@router.get("/traversal/{mode}")
def traversal_endpoint(mode: str):
    """
    Realiza un recorrido del árbol AVL según el modo especificado.
    
    Args:
        mode (str): Tipo de recorrido
            - 'pre': preorden (raíz, izq, der)
            - 'in': inorden (izq, raíz, der)
            - 'post': postorden (izq, der, raíz)
            - 'level': por niveles (BFS)
    
    Returns:
        dict: { "mode": mode, "result": [lista de valores] }
    
    HTTP 400:
        Si el árbol está vacío o modo inválido
    HTTP 500:
        Si hay error durante el recorrido
    """
    try:
        if avl.getRoot() is None:
            raise HTTPException(status_code=400, detail="El árbol está vacío")
        
        mode_lower = mode.lower().strip()
        
        if mode_lower == 'pre':
            result = traversal.pre_order(avl.getRoot())
        elif mode_lower == 'in':
            result = traversal.in_order(avl.getRoot())
        elif mode_lower == 'post':
            result = traversal.post_order(avl.getRoot())
        elif mode_lower == 'level':
            result = traversal.breadth_first_traversal(avl.getRoot())
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Modo inválido '{mode}'. Usa: 'pre', 'in', 'post', 'level'"
            )
        
        return {"mode": mode_lower, "result": result}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en recorrido: {str(e)}")