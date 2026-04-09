from core.structures.bst_tree.delete import _delete_node
from core.structures.bst_tree.insert import _insert_node
from core.structures.bst_tree.search import _search_node
from core.structures.node.node import Node


class BST:
    """
    This class represents a Binary Search Tree (BST) data structure.
    It provides methods for inserting, searching, and deleting nodes in the tree.
    """

    def __init__(self):
        self.root: Node | None = None

    def getRoot(self):
        return self.root

    def search(self, value: int) -> Node | None:
        if self.root is None:
            raise ValueError("The tree is empty.")

        return _search_node(self.root, value)

    def insert(self, value: int):
        new_node = Node(value)
        if self.root is None:
            self.root = new_node
        else:
            _insert_node(self.root, new_node)

    def delete(self, value: int):
        if self.root is None:
            raise ValueError("Cannot delete from an empty tree.")

        _delete_node(self.root, value)
