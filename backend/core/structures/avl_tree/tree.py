from core.structures.node.node import Node

from .insert import insert_node
from .search import search_node
from .balance import check_balance
from .delete import delete


class AVL:

    def __init__(self):
        self.root = None


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