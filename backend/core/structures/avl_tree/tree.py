"""
AVL tree implementation with self-balancing capabilities.

This module provides the main AVL class that manages self-balancing binary search trees
with support for stress mode (no rebalancing) and mass cancellation tracking.
"""

from core.structures.node.node import Node

from .balance import check_balance
from .delete import delete
from .insert import insert_node
from .search import search_node


class AVL:
    """
    Self-balancing AVL binary search tree.

    Manages flight data with automatic rebalancing unless stress_mode is enabled.
    Tracks rotation counts and mass cancellations for analytics.

    Attributes:
        root: Root node of the tree
        rotation_counts: Dict counting LL, RR, LR, RL rotations
        mass_cancellation_count: Counter for subtree cancellations
        stress_mode: If True, acts as BST (no rebalancing)
        depth_limit: Depth threshold for pricing penalties
    """

    def __init__(self):
        """Initialize an empty AVL tree with default settings."""
        self.root = None
        self.rotation_counts = {"LL": 0, "RR": 0, "LR": 0, "RL": 0}
        self.mass_cancellation_count = 0
        self.stress_mode = False
        self.depth_limit = 3

    def getRoot(self):
        """
        Get the root node of the tree.

        Returns:
            Node or None: The root node
        """
        return self.root

    def insert(self, node):
        """
        Insert a node into the AVL tree.

        If tree is empty, sets as root. Otherwise inserts and rebalances
        unless stress_mode is enabled.

        Args:
            node (Node): Node to insert
        """
        if self.root is None:
            self.root = node
        else:
            insert_node(self, self.root, node)

    def search(self, value):
        """
        Search for a node by value.

        Args:
            value (int): Value to search for

        Returns:
            Node or None: Found node or None

        Raises:
            Exception: If tree has no root
        """
        if self.root is None:
            raise Exception("Tree has no root")

        return search_node(self.root, value)

    def delete(self, value):
        """
        Delete a node by value.

        Args:
            value (int): Value to delete

        Raises:
            Exception: If value not found
        """
        delete(self, value)

    def contar_hojas(self):
        """
        Count leaf nodes in the tree.

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
        return self._contar_hojas_recursivo(node.getLeftChild()) + self._contar_hojas_recursivo(node.getRightChild())

    def contar_nodos(self):
        """
        Count total nodes in the tree.

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

    def cancelar_vuelo(self, value):
        """
        Cancel a flight and increment the mass cancellation counter.

        Increments mass_cancellation_count and deletes the node.

        Args:
            value (int): Flight code to cancel
        """
        self.mass_cancellation_count += 1
        self.delete(value)