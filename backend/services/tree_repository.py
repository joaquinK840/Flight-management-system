"""
Tree repository implementing repository pattern.

This module encapsulates tree operations and manages undo/redo functionality
for flight data management in AVL/BST structures.
"""

import copy
import json

from core.structures.avl_tree.balance import update_height
from core.structures.avl_tree.tree import AVL
from core.structures.bst_tree.bst import BST
from core.structures.node.node import Node
from core.structures.stack.stack import Stack
from services.serialize_tree import serialize_tree


class TreeRepository:
    """
    Repository pattern implementation for tree operations.

    Encapsulates CRUD operations on flights in the tree and manages undo/redo stacks.
    """

    def __init__(self, use_bst=False):
        """
        Initialize repository with a tree (AVL or BST).

        Args:
            use_bst (bool): If True, use BST; if False, use AVL
        """
        self.tree = BST() if use_bst else AVL()
        self.use_bst = use_bst
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def _save_state(self):
        """
        Save current tree state to undo stack.

        Serializes complete tree for later restoration.
        """
        state = self._serialize_full_tree()
        self.undo_stack.push(state)
        # Clear redo stack when taking new action
        self.redo_stack.clear()

    def _serialize_full_tree(self):
        """
        Serialize complete tree for undo storage.

        Returns:
            dict: Complete tree information
        """
        return {
            "root": self._serialize_node(self.tree.getRoot()),
            "rotation_counts": self.tree.rotation_counts.copy() if hasattr(self.tree, 'rotation_counts') else {},
            "mass_cancellation_count": self.tree.mass_cancellation_count if hasattr(self.tree, 'mass_cancellation_count') else 0,
            "stress_mode": self.tree.stress_mode if hasattr(self.tree, 'stress_mode') else False
        }

    def _serialize_node(self, node):
        """
        Recursively serialize a node for undo.

        Args:
            node (Node): Node to serialize

        Returns:
            dict: Serialized node data
        """
        if node is None:
            return None
        return {
            "value": node.getValue(),
            "height": node.getHeight(),
            "datos": node.getDatos().copy() if node.getDatos() else None,
            "left": self._serialize_node(node.getLeftChild()),
            "right": self._serialize_node(node.getRightChild())
        }

    def _restore_tree_from_state(self, state):
        """
        Restore tree from saved state.

        Args:
            state (dict): Tree state dictionary
        """
        # Reconstruct tree from state
        new_tree = BST() if self.use_bst else AVL()
        new_tree.root = self._deserialize_node(state["root"])
        if hasattr(new_tree, 'rotation_counts'):
            new_tree.rotation_counts = state.get("rotation_counts", {}).copy()
        if hasattr(new_tree, 'mass_cancellation_count'):
            new_tree.mass_cancellation_count = state.get("mass_cancellation_count", 0)
        if hasattr(new_tree, 'stress_mode'):
            new_tree.stress_mode = state.get("stress_mode", False)

        self.tree = new_tree

    def _deserialize_node(self, node_data):
        """
        Recursively deserialize a node.

        Args:
            node_data (dict): Serialized node data

        Returns:
            Node: Deserialized node
        """
        if node_data is None:
            return None

        node = Node(node_data["value"], datos=node_data.get("datos"))
        node.setHeight(node_data.get("height", 1))

        left_child = self._deserialize_node(node_data.get("left"))
        right_child = self._deserialize_node(node_data.get("right"))

        if left_child:
            node.setLeftChild(left_child)
            left_child.setParent(node)

        if right_child:
            node.setRightChild(right_child)
            right_child.setParent(node)

        return node

    def insert_flight(self, flight_data: dict) -> dict:
        """
        Insert a flight into the tree.

        Args:
            flight_data (dict): Flight data dictionary (codigo, origen, etc.)

        Returns:
            dict: Serialized tree and operation status

        Raises:
            ValueError: If flight lacks 'codigo'
        """
        if "codigo" not in flight_data:
            raise ValueError("Flight must have 'codigo'")

        # Save previous state
        self._save_state()

        try:
            value = flight_data["codigo"]
            node = Node(value, datos=flight_data.copy())

            # Insert according to stress_mode
            if self.tree.stress_mode and not self.use_bst:
                # In stress_mode with AVL, insert as BST (no balancing)
                self._insert_as_bst(node)
            else:
                # Insert normally
                self.tree.insert(node)

            return {
                "status": "success",
                "message": f"Flight {value} inserted",
                "tree": self._get_serialized_tree()
            }
        except Exception as e:
            # Restore previous state on error
            self.undo_stack.pop()
            raise e

    def _insert_as_bst(self, node):
        """
        Insert node as BST without balancing (for stress_mode).

        Args:
            node (Node): Node to insert
        """
        if self.tree.root is None:
            self.tree.root = node
        else:
            self._insert_bst_recursive(self.tree.root, node)
        # Update heights
        self._update_all_heights(self.tree.root)

    def _insert_bst_recursive(self, current, node):
        """
        Insert recursively without balancing.

        Args:
            current (Node): Current position
            node (Node): Node to insert
        """
        if node.getValue() == current.getValue():
            return

        if node.getValue() > current.getValue():
            if current.getRightChild() is None:
                current.setRightChild(node)
                node.setParent(current)
            else:
                self._insert_bst_recursive(current.getRightChild(), node)
        else:
            if current.getLeftChild() is None:
                current.setLeftChild(node)
                node.setParent(current)
            else:
                self._insert_bst_recursive(current.getLeftChild(), node)

    def _update_all_heights(self, node):
        """
        Update heights throughout the tree.

        Args:
            node (Node): Starting node
        """
        if node is None:
            return
        self._update_all_heights(node.getLeftChild())
        self._update_all_heights(node.getRightChild())
        update_height(node)

    def delete_flight(self, codigo: int) -> dict:
        """
        Delete a specific flight from the tree.

        Uses successor replacement for deletion.

        Args:
            codigo (int): Flight code to delete

        Returns:
            dict: Serialized tree

        Raises:
            ValueError: If flight not found
        """
        if self.tree.getRoot() is None:
            raise ValueError(f"Flight {codigo} not found")

        self._save_state()

        try:
            self.tree.delete(codigo)
            return {
                "status": "success",
                "message": f"Flight {codigo} deleted",
                "tree": self._get_serialized_tree()
            }
        except Exception as e:
            self.undo_stack.pop()
            raise e

    def cancel_flight_subtree(self, codigo: int) -> dict:
        """
        Delete a flight AND its entire subtree.

        Increments mass_cancellation_count.

        Args:
            codigo (int): Flight code of subtree root to cancel

        Returns:
            dict: Serialized tree

        Raises:
            ValueError: If flight not found
        """
        self._save_state()

        try:
            # Find the node
            node = self._find_node(self.tree.getRoot(), codigo)
            if node is None:
                raise ValueError(f"Flight {codigo} not found")

            # Increment counter
            if hasattr(self.tree, 'mass_cancellation_count'):
                self.tree.mass_cancellation_count += 1

            # Get parent
            parent = node.getParent()

            # Disconnect subtree by removing parent's reference
            if parent is None:
                # Is root: replace with left or right child
                if node.getLeftChild() is not None:
                    self.tree.root = node.getLeftChild()
                    self.tree.root.setParent(None)
                elif node.getRightChild() is not None:
                    self.tree.root = node.getRightChild()
                    self.tree.root.setParent(None)
                else:
                    self.tree.root = None
            else:
                if parent.getLeftChild() == node:
                    parent.setLeftChild(None)
                else:
                    parent.setRightChild(None)

                # Recalculate heights from parent
                from core.structures.avl_tree.balance import check_balance
                if hasattr(self.tree, 'rotation_counts'):  # Is AVL
                    check_balance(self.tree, parent)

            return {
                "status": "success",
                "message": f"Flight {codigo} and subtree cancelled",
                "tree": self._get_serialized_tree(),
                "mass_cancellations": self.tree.mass_cancellation_count if hasattr(self.tree, 'mass_cancellation_count') else 0
            }
        except Exception as e:
            self.undo_stack.pop()
            raise e

    def update_flight(self, codigo: int, updated_data: dict) -> dict:
        """
        Update flight data without changing tree position.

        Args:
            codigo (int): Flight code
            updated_data (dict): Updated data dictionary

        Returns:
            dict: Serialized tree

        Raises:
            ValueError: If flight not found
        """
        self._save_state()

        try:
            node = self._find_node(self.tree.getRoot(), codigo)
            if node is None:
                raise ValueError(f"Flight {codigo} not found")

            # Update data
            if node.getDatos() is None:
                node.setDatos({})

            current_datos = node.getDatos()
            current_datos.update(updated_data)
            node.setDatos(current_datos)

            return {
                "status": "success",
                "message": f"Flight {codigo} updated",
                "tree": self._get_serialized_tree()
            }
        except Exception as e:
            self.undo_stack.pop()
            raise e

    def undo(self) -> dict:
        """
        Restore previous tree state.

        Returns:
            dict: Serialized tree from previous state

        Raises:
            ValueError: If no actions to undo
        """
        if self.undo_stack.is_empty():
            raise ValueError("No actions to undo")

        # Save current state to redo
        self.redo_stack.push(self._serialize_full_tree())

        # Restore previous state
        previous_state = self.undo_stack.pop()
        self._restore_tree_from_state(previous_state)

        return {
            "status": "success",
            "message": "Operation undone",
            "tree": self._get_serialized_tree(),
            "undo_remaining": self.undo_stack.size()
        }

    def redo(self) -> dict:
        """
        Restore undone tree state.

        Returns:
            dict: Serialized tree from restored state

        Raises:
            ValueError: If no actions to redo
        """
        if self.redo_stack.is_empty():
            raise ValueError("No actions to redo")

        # Save current state to undo
        self.undo_stack.push(self._serialize_full_tree())

        # Restore redo state
        next_state = self.redo_stack.pop()
        self._restore_tree_from_state(next_state)

        return {
            "status": "success",
            "message": "Operation redone",
            "tree": self._get_serialized_tree()
        }

    def _find_node(self, node, codigo):
        """
        Recursively search for node by code.

        Args:
            node (Node): Current node
            codigo (int): Code to find

        Returns:
            Node or None: Found node or None
        """
        if node is None:
            return None

        if node.getValue() == codigo:
            return node
        elif codigo > node.getValue():
            return self._find_node(node.getRightChild(), codigo)
        else:
            return self._find_node(node.getLeftChild(), codigo)

    def _get_serialized_tree(self) -> dict:
        """
        Serialize current tree for API responses.

        Returns:
            dict: Serialized tree data
        """
        return serialize_tree(self.tree, depth=0, depth_limit=self.tree.depth_limit)

    def get_tree_metrics(self) -> dict:
        """
        Return current tree metrics.

        Returns:
            dict: Comprehensive tree metrics
        """
        root = self.tree.getRoot()
        return {
            "height": root.getHeight() if root else 0,
            "leaves": self.tree.contar_hojas(),
            "total_nodes": self.tree.contar_nodos(),
            "rotation_counts": self.tree.rotation_counts.copy() if hasattr(self.tree, 'rotation_counts') else {},
            "total_rotations": sum(self.tree.rotation_counts.values()) if hasattr(self.tree, 'rotation_counts') else 0,
            "mass_cancellations": self.tree.mass_cancellation_count if hasattr(self.tree, 'mass_cancellation_count') else 0,
            "undo_states_available": self.undo_stack.size(),
            "tree_type": "BST" if self.use_bst else "AVL"
        }
