from core.structures.node.node import Node

from .insert import insert_node
from .search import search_node
from .balance import check_balance
from .cancel import cancel
from .delete import delete



class AVL:

    def __init__(self):
        self.root = None
        self.rotate_right = 0
        self.rotate_left_right = 0
        self.rotate_left = 0
        self.rotate_right_left = 0
        
    
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


    def cancel(self, value):
        cancel(self, value)

    def delete(self, value):
        delete(self, value)

    def get_rotation_by_type(self):
        return {
            "LL": self.rotate_right,
            "LR": self.rotate_left_right,
            "RR": self.rotate_left,
            "RL": self.rotate_right_left
        }
    