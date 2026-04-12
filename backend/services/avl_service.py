from core.structures.avl_tree.tree import AVL
from core.structures.bst_tree.tree import BST
from core.structures.node.node import Node
from services.serialize_tree import serialize_tree

class TreeService:
    def __init__(self, avl=None, bst=None):
        self.avl = avl or AVL()
        self.bst = bst or BST()

    def set_trees(self, avl, bst):
        self.avl = avl
        self.bst = bst

    def insert_node(self, value: int):
        node = Node(value)
        self.avl.insert(node)
        return {
            "message": "Nodo insertado",
            "root": self.avl.getRoot().getValue() if self.avl.getRoot() else None,
            "tree": serialize_tree(self.avl)
        }

    def get_tree(self):
        return {
            "tree": serialize_tree(self.avl)
        }

    def search_value(self, value: int):
        node = self.avl.search(value)
        if node is None:
            return {
                "found": False,
                "value": value
            }
        return {
            "found": True,
            "value": node.getValue()
        }

    def cancel_value(self, value: int):
        self.avl.cancel(value)
        return {
            "canceled": True,
            "value": value,
            "message": "Valor cancelado",
            "tree": serialize_tree(self.avl)
        }

    def delete_value(self, value: int):
        self.avl.delete(value)
        return {
            "deleted": True,
            "value": value,
            "message": "Valor eliminado",
            "tree": serialize_tree(self.avl)
        }

    def reset_tree(self):
        self.avl = AVL()
        self.bst = BST()
        return {
            "message": "Árbol reiniciado"
        }

# Singleton instance to persist tree state across requests if not using a DB
tree_service = TreeService()
