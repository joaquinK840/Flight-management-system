from fastapi import APIRouter, UploadFile, HTTPException, File, Depends
from core.structures.avl_tree.tree import AVL
from core.structures.node.node import Node
from services.metrics import get_metrics
from services.json_manager import load_trees_from_json
from services.serialize_tree import serialize_tree
from services.stress_mode_service import rebalance_tree_postorder, audit_tree

router = APIRouter(prefix="/avl", tags=["AVL Tree"])

# instancia global del árbol
avl = AVL()

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

    root = avl.getRoot()

    return {
        "tree": serialize(root)
    }


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


# -----------------------------
# REINICIAR ÁRBOL
# -----------------------------
@router.delete("/reset")
def reset_tree():

    global avl
    avl = AVL()

    return {
        "message": "Árbol reiniciado"
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