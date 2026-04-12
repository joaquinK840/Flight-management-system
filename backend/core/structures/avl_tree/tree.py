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
            raise Exception("El arbol no tiene raiz")

        return search_node(self.root, value)

    def delete(self, value):
        delete(self, value)

    def contar_hojas(self):
        """Contar el numero de hojas en el arbol."""
        return self._contar_hojas_recursivo(self.root)

    def _contar_hojas_recursivo(self, node):
        if node is None:
            return 0
        if node.getLeftChild() is None and node.getRightChild() is None:
            return 1
        return self._contar_hojas_recursivo(node.getLeftChild()) + self._contar_hojas_recursivo(node.getRightChild())

    def contar_nodos(self):
        """Contar el numero total de nodos en el arbol."""
        return self._contar_nodos_recursivo(self.root)

    def _contar_nodos_recursivo(self, node):
        if node is None:
            return 0
        return 1 + self._contar_nodos_recursivo(node.getLeftChild()) + self._contar_nodos_recursivo(node.getRightChild())

    def cancelar_vuelo(self, value):
        """Cancelar un vuelo (incrementar contador de cancelaciones masivas)."""
        self.mass_cancellation_count += 1
        self.delete(value)
