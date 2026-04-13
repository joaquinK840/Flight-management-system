"""
Binary Search Tree implementation without self-balancing.

This module provides a standard BST for comparison with AVL trees,
using the same data but without rotation-based balancing.
"""

from core.structures.node.node import Node


class BST:
    """
    Binary Search Tree without automatic balancing.

    Used for comparison against AVL trees with identical data.
    Maintains BST property but allows arbitrary imbalance.

    Attributes:
        root: Root node of the tree
    """

    def __init__(self):
        """Initialize an empty BST."""
        self.root = None

    def getRoot(self):
        """
        Get the root node of the tree.

        Returns:
            Node or None: The root node
        """
        return self.root

    def insert(self, node):
        """
        Insert a node into the BST maintaining BST property.

        No rotations are performed (unlike AVL).

        Args:
            node (Node): Node with value and optional flight data
        """
        if self.root is None:
            self.root = node
        else:
            self._insert_recursive(self.root, node)

    def _insert_recursive(self, current, node):
        """
        Recursively insert node while maintaining BST ordering.

        Args:
            current (Node): Current position in traversal
            node (Node): Node to insert
        """
        if node.getValue() == current.getValue():
            # Duplicate - do not insert
            return

        if node.getValue() > current.getValue():
            # Go right
            if current.getRightChild() is None:
                current.setRightChild(node)
                node.setParent(current)
                self._update_height_branch(current)
            else:
                self._insert_recursive(current.getRightChild(), node)
        else:
            # Go left
            if current.getLeftChild() is None:
                current.setLeftChild(node)
                node.setParent(current)
                self._update_height_branch(current)
            else:
                self._insert_recursive(current.getLeftChild(), node)

    def _update_height_branch(self, node):
        """
        Update heights from node up to root (no rotations).

        Args:
            node (Node): Starting node for height update
        """
        while node is not None:
            left_height = node.getLeftChild().getHeight() if node.getLeftChild() is not None else 0
            right_height = node.getRightChild().getHeight() if node.getRightChild() is not None else 0
            node.setHeight(1 + max(left_height, right_height))
            node = node.getParent()

    def search(self, value):
        """
        Search for a node by value in O(log n) average time.

        Args:
            value (int): Value to search for

        Returns:
            Node or None: Found node or None
        """
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        """
        Recursive binary search implementation.

        Args:
            node (Node): Current node in search
            value (int): Value to find

        Returns:
            Node or None: Found node or None
        """
        if node is None:
            return None

        if value == node.getValue():
            return node
        elif value > node.getValue():
            return self._search_recursive(node.getRightChild(), value)
        else:
            return self._search_recursive(node.getLeftChild(), value)

    def contar_hojas(self):
        """
        Count the number of leaf nodes in the tree.

        Returns:
            int: Number of leaf nodes
        """
        return self._contar_hojas_recursivo(self.root)

    def _contar_hojas_recursivo(self, node):
        """
        Recursively count leaf nodes.

        Args:
            node (Node): Current node in traversal

        Returns:
            int: Number of leaf nodes in subtree
        """
        if node is None:
            return 0
        if node.getLeftChild() is None and node.getRightChild() is None:
            return 1
        return (
            self._contar_hojas_recursivo(node.getLeftChild()) +
            self._contar_hojas_recursivo(node.getRightChild())
        )

    def contar_nodos(self):
        """
        Count the total number of nodes in the tree.

        Returns:
            int: Total number of nodes
        """
        return self._contar_nodos_recursivo(self.root)

    def _contar_nodos_recursivo(self, node):
        """
        Recursively count total nodes.

        Args:
            node (Node): Current node in traversal

        Returns:
            int: Number of nodes in subtree
        """
        if node is None:
            return 0
        return 1 + self._contar_nodos_recursivo(node.getLeftChild()) + self._contar_nodos_recursivo(node.getRightChild())

    def obtener_profundidad(self):
        """
        Get the maximum depth of the tree.

        Returns:
            int: Maximum depth (height - 1)
        """
        return self._obtener_profundidad_recursiva(self.root) - 1

    def _obtener_profundidad_recursiva(self, node):
        """
        Recursively calculate tree depth.

        Args:
            node (Node): Current node in traversal

        Returns:
            int: Depth of subtree
        """
        if node is None:
            return 0
        return 1 + max(
            self._obtener_profundidad_recursiva(node.getLeftChild()),
            self._obtener_profundidad_recursiva(node.getRightChild())
        )
