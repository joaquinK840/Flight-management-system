from fastapi import APIRouter

from controllers.tree_controller import tree_controller

router = APIRouter(prefix="/avl", tags=["AVL Tree"])

# -----------------------------
# INSERTAR NODO
# -----------------------------
@router.post("/insert/{value}")
def insert_value(value: int):
    return tree_controller.insert_value(value)


# -----------------------------
# OBTENER ÁRBOL COMPLETO
# -----------------------------
@router.get("/tree")
def get_tree():
    return tree_controller.get_tree()


# -----------------------------
# BUSCAR VALOR
# -----------------------------
@router.get("/search/{value}")
def search_value(value: int):
    return tree_controller.search_value(value)

# -----------------------------
# CANCELAR VALOR
# -----------------------------
@router.delete("/cancel/{value}")
def cancel_value(value: int):
    return tree_controller.cancel_value(value)

# -----------------------------
# ELIMINAR VALOR
# -----------------------------
@router.delete("/delete/{value}")
def delete_value(value: int):
    return tree_controller.delete_value(value)

# -----------------------------
# REINICIAR ÁRBOL
# -----------------------------
@router.delete("/reset")
def reset_tree():
    return tree_controller.reset_tree()