from fastapi import APIRouter
from core.structures.avl_tree.tree import AVL
from core.structures.node.node import Node

router = APIRouter(prefix="/avl", tags=["AVL Tree"])

# instancia global del árbol
avl = AVL()


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
# CANCELAR VALOR
# -----------------------------
@router.delete("/cancel/{value}")
def cancel_value(value: int):
    avl.cancel(value)

    return {
        "canceled": True,
        "value": value,
        "message": "Valor cancelado",
        "tree": serialize(avl.getRoot())
    }

# -----------------------------
# ELIMINAR VALOR
# -----------------------------
@router.delete("/delete/{value}")
def delete_value(value: int):
    avl.delete(value)

    return {
        "deleted": True,
        "value": value,
        "message": "Valor eliminado",
        "tree": serialize(avl.getRoot())
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