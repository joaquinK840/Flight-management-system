from core.structures.node.node import Node

from .insert import insert_node
from .search import search_node
from .balance import check_balance
from .delete import delete


class AVL:

    def __init__(self):
        self.root = None
        self.rotation_counts = {"LL": 0, "RR": 0, "LR": 0, "RL": 0}
        self.mass_cancellation_count = 0
        self.stress_mode = False
        self.depth_limit = 3


    def getRoot(self):
        return self.root


    def insert(self, node):

        if self.root is None:
            self.root = node
        else:
            insert_node(self, self.root, node)


    def search(self, value):

        if self.root is None:
            raise Exception("El árbol no tiene raíz")

        return search_node(self.root, value)


    def delete(self, value):
        delete(self, value)

    def contar_hojas(self):
        """Count leaf nodes in the tree."""
        return self._contar_hojas_recursivo(self.root)

    def _contar_hojas_recursivo(self, node):
        if node is None:
            return 0
        if node.getLeftChild() is None and node.getRightChild() is None:
            return 1
        return self._contar_hojas_recursivo(node.getLeftChild()) + self._contar_hojas_recursivo(node.getRightChild())

    def contar_nodos(self):
        """Count total nodes in the tree."""
        return self._contar_nodos_recursivo(self.root)

    def _contar_nodos_recursivo(self, node):
        if node is None:
            return 0
        return 1 + self._contar_nodos_recursivo(node.getLeftChild()) + self._contar_nodos_recursivo(node.getRightChild())

    def cancelar_vuelo(self, value):
        """Cancel a flight and increment the mass cancellation counter."""
        self.mass_cancellation_count += 1
        self.delete(value)