from core.structures.node.node import Node


class BST:
    """
    Binary Search Tree implementation for comparison with AVL tree.
    """

    def __init__(self):
        self.root = None

    def getRoot(self):
        return self.root

    def insert(self, node):
        """
        Insert a node into the BST.
        """
        if self.root is None:
            self.root = node
        else:
            self._insert_recursive(self.root, node)

    def _insert_recursive(self, current, node):
        """
        Recursive helper for insertion.
        """
        if node.getValue() < current.getValue():
            if current.getLeftChild() is None:
                current.setLeftChild(node)
                node.setParent(current)
            else:
                self._insert_recursive(current.getLeftChild(), node)
        else:
            if current.getRightChild() is None:
                current.setRightChild(node)
                node.setParent(current)
            else:
                self._insert_recursive(current.getRightChild(), node)

    def insertar(self, clave, datos):
        """
        Insert a new node with key and data.
        """
        nuevo_nodo = Node(clave)
        nuevo_nodo.setDatos(datos)
        self.insert(nuevo_nodo)

    def search(self, value):
        """
        Search for a node with the given value.
        """
        return self._search_recursive(self.root, value)

    def _search_recursive(self, current, value):
        """
        Recursive helper for search.
        """
        if current is None or current.getValue() == value:
            return current

        if value < current.getValue():
            return self._search_recursive(current.getLeftChild(), value)
        else:
            return self._search_recursive(current.getRightChild(), value)

    def delete(self, value):
        """
        Delete a node with the given value.
        """
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, current, value):
        """
        Recursive helper for deletion.
        """
        if current is None:
            return current

        if value < current.getValue():
            current.setLeftChild(self._delete_recursive(current.getLeftChild(), value))
        elif value > current.getValue():
            current.setRightChild(self._delete_recursive(current.getRightChild(), value))
        else:
            # Node with only one child or no child
            if current.getLeftChild() is None:
                return current.getRightChild()
            elif current.getRightChild() is None:
                return current.getLeftChild()

            # Node with two children: Get the inorder successor
            temp = self._min_value_node(current.getRightChild())
            current.value = temp.getValue()
            current.setDatos(temp.getDatos())
            current.setRightChild(self._delete_recursive(current.getRightChild(), temp.getValue()))

        return current

    def _min_value_node(self, node):
        """
        Find the node with minimum value in a subtree.
        """
        current = node
        while current.getLeftChild() is not None:
            current = current.getLeftChild()
        return current

    def get_height(self, node=None):
        """
        Get the height of the tree or a specific node.
        """
        if node is None:
            node = self.root
        if node is None:
            return -1

        left_height = self.get_height(node.getLeftChild())
        right_height = self.get_height(node.getRightChild())

        return max(left_height, right_height) + 1

    def count_leaves(self, node=None):
        """
        Count the number of leaf nodes in the tree.
        """
        if node is None:
            node = self.root
        if node is None:
            return 0

        if node.getLeftChild() is None and node.getRightChild() is None:
            return 1

        return self.count_leaves(node.getLeftChild()) + self.count_leaves(node.getRightChild())

    def in_order_traversal(self):
        """
        Return in-order traversal as a list.
        """
        result = []
        self._in_order_recursive(self.root, result)
        return result

    def _in_order_recursive(self, node, result):
        """
        Recursive helper for in-order traversal.
        """
        if node is not None:
            self._in_order_recursive(node.getLeftChild(), result)
            result.append(node.getValue())
            self._in_order_recursive(node.getRightChild(), result)

    def serialize(self, node=None):
        """
        Serialize the tree to a dictionary structure.
        """
        if node is None:
            node = self.root

        if node is None:
            return None

        return {
            "value": node.getValue(),
            "data": node.getDatos(),
            "left": self.serialize(node.getLeftChild()),
            "right": self.serialize(node.getRightChild())
        }