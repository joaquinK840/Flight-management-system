from typing import Optional

from fastapi import APIRouter, Body
from controllers.tree_controller import tree_controller
from core.structures.avl_tree.tree import AVL
from core.structures.bst_tree.tree import BST
from core.structures.node.node import Node
from models.flight import Flight
from services.avl_service import tree_service
from services.serialize_tree import serialize_tree

avl = AVL()
bst = BST()
tree_service.set_trees(avl, bst)

router = APIRouter(prefix="/avl", tags=["AVL Tree"])


def _count_leaves(node):
    if node is None:
        return 0
    if node.getLeftChild() is None and node.getRightChild() is None:
        return 1
    return _count_leaves(node.getLeftChild()) + _count_leaves(node.getRightChild())


def _height(node):
    if node is None:
        return 0
    return 1 + max(_height(node.getLeftChild()), _height(node.getRightChild()))


def _build_avl_from_topology(data):
    if data is None:
        return None

    flight = Flight.from_dict(data)
    node = Node(flight.codigo, flight.to_dict())
    left = _build_avl_from_topology(data.get("izquierdo"))
    right = _build_avl_from_topology(data.get("derecho"))

    if left is not None:
        left.setParent(node)
        node.setLeftChild(left)
    if right is not None:
        right.setParent(node)
        node.setRightChild(right)

    return node


def _inorder_nodes(node, nodes):
    if node is None:
        return
    _inorder_nodes(node.getLeftChild(), nodes)
    nodes.append(node)
    _inorder_nodes(node.getRightChild(), nodes)


def _comparison_payload(tree):
    root = tree.getRoot()
    return {
        "root": root.getValue() if root else None,
        "height": _height(root),
        "leaves": _count_leaves(root),
    }

# -----------------------------
# INSERTAR NODO
# -----------------------------
@router.post("/insert/{value}")
def insert_value(value: int, payload: Optional[dict] = Body(None)):
    if payload:
        flight = Flight.from_dict(payload)
        value = flight.codigo
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
    response = tree_controller.reset_tree()
    global avl, bst
    avl = tree_service.avl
    bst = tree_service.bst
    return response


@router.post("/load-json")
def load_json(payload: dict = Body(...)):
    tree_service.set_trees(AVL(), BST())
    global avl, bst
    avl = tree_service.avl
    bst = tree_service.bst

    if payload.get("tipo") == "INSERCION" or "vuelos" in payload:
        vuelos = payload.get("vuelos", [])
        for flight_data in vuelos:
            flight = Flight.from_dict(flight_data)
            flight.precio_final = flight.precio_base
            node = Node(flight.codigo, flight.to_dict())
            avl.insert(node)
            bst_node = Node(flight.codigo, flight.to_dict())
            bst.insert_node(bst_node)

        load_type = "insertion"
    else:
        avl.root = _build_avl_from_topology(payload)
        nodes = []
        _inorder_nodes(avl.root, nodes)
        for node in nodes:
            flight = Flight.from_dict(node.getDatos() or {})
            bst_node = Node(flight.codigo, flight.to_dict())
            bst.insert_node(bst_node)

        load_type = "topology"

    return {
        "load_type": load_type,
        "trees": {
            "avl": serialize_tree(avl),
            "bst": serialize_tree(bst),
        },
        "comparison": {
            "avl": _comparison_payload(avl),
            "bst": _comparison_payload(bst),
        },
    }


@router.put("/config/depth-limit")
def set_depth_limit(payload: dict = Body(...)):
    limit = payload.get("limit")
    if limit is not None:
        avl.depth_limit = int(limit)
    return {
        "depth_limit": avl.depth_limit,
        "tree": serialize_tree(avl),
    }


@router.get("/config")
def get_config():
    return {
        "depth_limit": avl.depth_limit,
        "stress_mode": avl.stress_mode,
    }
