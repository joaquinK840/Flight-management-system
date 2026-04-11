from core.structures.avl_tree.tree import AVL
from core.structures.node.node import Node
from services.serialize_tree import serialize_tree


class AVLService:
    def __init__(self):
        self._avl = AVL()

    def _find_node(self, value: int):
        root = self._avl.getRoot()
        if root is None:
            return None
        return self._avl.search(value)

    def insert_value(self, value: int) -> dict:
        if self._find_node(value) is not None:
            return {
                "inserted": False,
                "value": value,
                "message": f"El valor {value} ya existe",
                "tree": serialize_tree(self._avl),
            }

        self._avl.insert(Node(value))

        return {
            "inserted": True,
            "value": value,
            "message": "Nodo insertado",
            "root": self._avl.getRoot().getValue() if self._avl.getRoot() else None,
            "tree": serialize_tree(self._avl),
        }

    def get_tree(self) -> dict:
        return {
            "tree": serialize_tree(self._avl)
        }

    def search_value(self, value: int) -> dict:
        node = self._find_node(value)
        if node is None:
            return {
                "found": False,
                "value": value,
            }

        return {
            "found": True,
            "value": node.getValue(),
        }

    def cancel_value(self, value: int) -> dict:
        if self._find_node(value) is None:
            raise ValueError(f"No se encontró el valor {value} en el árbol")

        self._avl.cancel(value)
        return {
            "canceled": True,
            "value": value,
            "message": "Valor cancelado",
            "tree": serialize_tree(self._avl),
        }

    def delete_value(self, value: int) -> dict:
        if self._find_node(value) is None:
            raise ValueError(f"No se encontró el valor {value} en el árbol")

        self._avl.delete(value)
        return {
            "deleted": True,
            "value": value,
            "message": "Valor eliminado",
            "tree": serialize_tree(self._avl),
        }

    def reset_tree(self) -> dict:
        self._avl = AVL()
        return {
            "message": "Árbol reiniciado"
        }
