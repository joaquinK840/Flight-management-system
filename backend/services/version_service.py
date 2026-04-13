"""
Tree versioning service.

Allows saving, restoring, and managing complete versions of the AVL tree.
"""

from datetime import datetime
from typing import Dict, Optional, List
from core.structures.node.node import Node
from core.structures.avl_tree.balance import update_height


class VersionService:
    """
    Versioning service for trees.

    Maintains a dictionary of saved versions of the complete tree.
    """

    def __init__(self):
        """
        Initialize the versioning service.

        Structure:
        {
            "version_name": {
                "timestamp": "2026-04-12 10:30:45",
                "tree_data": { serialized node },
                "metrics": { height, nodes, leaves, etc }
            }
        }
        """
        self.versions: Dict[str, dict] = {}

    def save_version(self, tree, version_name: str, queue=None) -> dict:
        """
        Save the current state of the tree AND THE QUEUE as a new version.

        Serializes the complete hierarchical structure of the tree.

        Args:
            tree: AVL/BST tree to save
            version_name (str): Name of the version
            queue: Optional FIFO queue to save

        Returns:
            dict: Dictionary with confirmation, timestamp, and list of versions

        Raises:
            ValueError: If name already exists or is empty, or if tree is empty
        """
        if not version_name or not version_name.strip():
            raise ValueError("El nombre de la versión no puede estar vacío")
        
        if version_name in self.versions:
            raise ValueError(f"La versión '{version_name}' ya existe")
        
        # Validar que el árbol no esté vacío
        root = tree.getRoot()
        if root is None:
            raise ValueError("No se puede guardar una versión del árbol vacío. Primero carga o crea vuelos.")
        
        # Serializar el árbol completo (estructura jerárquica)
        tree_data = self._serialize_tree_complete(root)
        
        # Calcular métricas
        metrics = self._calculate_metrics(tree)
        
        # Guardar cola FIFO si existe
        queue_data = None
        queue_size = 0
        if queue is not None:
            queue_data = queue.get_all()  # Obtener todos los vuelos en la cola
            queue_size = queue.size()
        
        # Guardar versión
        self.versions[version_name] = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tree_data": tree_data,
            "metrics": metrics,
            "queue_data": queue_data,
            "queue_size": queue_size,
            "tree_type": "AVL" if hasattr(tree, 'rotation_counts') else "BST",
            "stress_mode": bool(getattr(tree, "stress_mode", False))
        }
        
        return {
            "status": "success",
            "message": f"Versión '{version_name}' guardada (incluyendo cola FIFO)",
            "timestamp": self.versions[version_name]["timestamp"],
            "versions_count": len(self.versions),
            "available_versions": self.get_version_list(),
            "tree_stats": {
                "total_nodes": metrics.get("total_nodes", 0),
                "total_leaves": metrics.get("total_leaves", 0),
                "height": metrics.get("height", 0),
                "queue_size": queue_size
            }
        }

    def _serialize_tree_complete(self, node):
        """
        Serialize a complete tree preserving the hierarchical structure.

        Important: Saves value, data, height, left, right for exact reconstruction.

        Args:
            node: Root node of the tree

        Returns:
            dict: Dictionary with complete tree structure
        """
        if node is None:
            return None
        
        return {
            "value": node.getValue(),
            "height": node.getHeight(),
            "datos": node.getDatos().copy() if node.getDatos() else None,
            "left": self._serialize_tree_complete(node.getLeftChild()),
            "right": self._serialize_tree_complete(node.getRightChild())
        }

    def _calculate_metrics(self, tree) -> dict:
        """
        Calculate tree metrics to save in the version.

        Args:
            tree: Tree to measure

        Returns:
            dict: Dictionary with metrics
        """
        root = tree.getRoot()
        
        metrics = {
            "height": root.getHeight() if root else 0,
            "total_nodes": self._count_nodes(root),
            "total_leaves": self._count_leaves(root),
        }
        
        # Agregar métricas específicas de AVL
        if hasattr(tree, 'rotation_counts'):
            metrics["rotation_counts"] = tree.rotation_counts.copy()
            metrics["total_rotations"] = sum(tree.rotation_counts.values())
        
        if hasattr(tree, 'mass_cancellation_count'):
            metrics["mass_cancellations"] = tree.mass_cancellation_count
        
        return metrics

    def get_version_list(self) -> List[str]:
        """
        Return list of saved version names.

        Returns:
            List[str]: List of version names
        """
        return list(self.versions.keys())

    def get_version_info(self, version_name: str) -> dict:
        """
        Get detailed information about a version.

        Args:
            version_name (str): Name of the version

        Returns:
            dict: Dictionary with version information

        Raises:
            ValueError: If the version does not exist
        """
        if version_name not in self.versions:
            raise ValueError(f"La versión '{version_name}' no existe")
        
        version = self.versions[version_name]
        return {
            "name": version_name,
            "timestamp": version["timestamp"],
            "metrics": version["metrics"],
            "tree_type": version.get("tree_type", "Unknown"),
            "has_data": version["tree_data"] is not None
        }

    def restore_version(self, tree, version_name: str, queue=None) -> dict:
        """
        Restore a tree AND THE QUEUE from a saved version.

        Reconstructs exactly the original topology with the same heights.

        Args:
            tree: Target tree (will be cleared and filled)
            version_name (str): Name of the version to restore
            queue: Optional FIFO queue to restore

        Returns:
            dict: Dictionary with confirmation and serialized restored tree

        Raises:
            ValueError: If the version does not exist or is empty
        """
        
        if version_name not in self.versions:
            raise ValueError(f"La versión '{version_name}' no existe")
        
        version_data = self.versions[version_name]
        tree_data = version_data["tree_data"]
        
        # Validar que tenemos datos para restaurar
        if tree_data is None:
            raise ValueError(f"La versión '{version_name}' está vacía y no se puede restaurar")
        
        # Reconstruir el árbol desde el estado serializado
        new_root = self._deserialize_tree_complete(tree_data)
        
        # Validar que la deserialización tuvo éxito
        if new_root is None and tree_data is not None:
            raise ValueError(f"Error al deserializar la versión '{version_name}'")
        
        # Limpiar completamente el árbol actual
        tree.root = None
        tree.rotation_counts = {"LL": 0, "RR": 0, "LR": 0, "RL": 0}
        if hasattr(tree, 'mass_cancellation_count'):
            tree.mass_cancellation_count = 0
        
        # Asignar nueva raíz al árbol
        tree.root = new_root
        
        # Restaurar contador de cancelaciones si aplica
        if hasattr(tree, 'mass_cancellation_count'):
            tree.mass_cancellation_count = version_data["metrics"].get("mass_cancellations", 0)

        # Restaurar stress_mode si aplica
        if hasattr(tree, 'stress_mode'):
            tree.stress_mode = bool(version_data.get("stress_mode", False))
        
        # Restaurar conteos de rotaciones si aplica
        if hasattr(tree, 'rotation_counts'):
            saved_rotations = version_data["metrics"].get("rotation_counts", {
                "LL": 0, "RR": 0, "LR": 0, "RL": 0
            })
            tree.rotation_counts = {
                "LL": saved_rotations.get("LL", 0),
                "RR": saved_rotations.get("RR", 0),
                "LR": saved_rotations.get("LR", 0),
                "RL": saved_rotations.get("RL", 0)
            }
        
        # RESTAURAR COLA FIFO
        restored_queue_size = 0
        if queue is not None:
            # Limpiar la cola actual
            while not queue.is_empty():
                queue.dequeue()
            
            # Restaurar los vuelos guardados en la versión
            queue_data = version_data.get("queue_data", [])
            if queue_data:
                for flight in queue_data:
                    queue.enqueue(flight)
                restored_queue_size = len(queue_data)
        
        # Serializar el árbol restaurado para devolver
        restored_tree_data = self._serialize_tree_complete(new_root)
        
        # Verificar que el árbol restaurado no está vacío
        if restored_tree_data is None and new_root is not None:
            return {
                "status": "error",
                "message": f"El árbol se restauró pero no se puede serializar correctamente",
                "root": None
            }
        
        return {
            "status": "success",
            "message": f"Versión '{version_name}' restaurada correctamente (árbol + cola FIFO)",
            "restored_from": version_data["timestamp"],
            "metrics": version_data["metrics"],
            "root": restored_tree_data,
            "depth_limit": tree.depth_limit if hasattr(tree, 'depth_limit') else 3,
            "rotations": tree.rotation_counts if hasattr(tree, 'rotation_counts') else {},
            "queue_restored": restored_queue_size > 0,
            "queue_size": restored_queue_size
        }

    def _deserialize_tree_complete(self, tree_data):
        """
        Reconstruct a tree from serialized data.

        Maintains the original hierarchical structure.

        Args:
            tree_data: Dictionary with tree structure

        Returns:
            Root node of the reconstructed tree
        """
        if tree_data is None:
            return None
        
        try:
            # Crear nodo con valor, datos y altura
            node = Node(tree_data["value"], datos=tree_data.get("datos"))
            node.setHeight(tree_data.get("height", 1))
            
            # Validar que el nodo fue creado correctamente
            if node is None:
                return None
            
            # Reconstruir subárboles
            left_data = tree_data.get("left")
            right_data = tree_data.get("right")
            
            left_child = self._deserialize_tree_complete(left_data) if left_data else None
            right_child = self._deserialize_tree_complete(right_data) if right_data else None
            
            # Conectar subárboles de forma explícita
            if left_child is not None:
                node.setLeftChild(left_child)
                left_child.setParent(node)
            
            if right_child is not None:
                node.setRightChild(right_child)
                right_child.setParent(node)
            
            return node
        
        except Exception as e:
            print(f"Error en deserialización: {str(e)}")
            return None

    def delete_version(self, version_name: str) -> dict:
        """
        Delete a saved version.

        Args:
            version_name (str): Name of the version to delete

        Returns:
            dict: Dictionary with confirmation

        Raises:
            ValueError: If the version does not exist
        """
        if version_name not in self.versions:
            raise ValueError(f"La versión '{version_name}' no existe")
        
        del self.versions[version_name]
        
        return {
            "status": "success",
            "message": f"Versión '{version_name}' eliminada",
            "versions_remaining": len(self.versions),
            "available_versions": self.get_version_list()
        }

    def clear_all_versions(self) -> dict:
        """
        Delete all saved versions.

        Returns:
            dict: Dictionary with confirmation
        """
        count = len(self.versions)
        self.versions.clear()
        
        return {
            "status": "success",
            "message": f"Se eliminaron {count} versiones",
            "versions_remaining": 0
        }

    def overwrite_version(self, tree, version_name: str) -> dict:
        """
        Overwrite an existing version with the current tree state.

        Args:
            tree: Current tree
            version_name (str): Name of the version to overwrite

        Returns:
            dict: Dictionary with confirmation

        Raises:
            ValueError: If the version does not exist
        """
        if version_name not in self.versions:
            raise ValueError(f"La versión '{version_name}' no existe")
        
        # Serializar árbol actual
        tree_data = self._serialize_tree_complete(tree.getRoot())
        metrics = self._calculate_metrics(tree)
        
        # Sobrescribir versión
        self.versions[version_name] = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tree_data": tree_data,
            "metrics": metrics,
            "tree_type": "AVL" if hasattr(tree, 'rotation_counts') else "BST"
        }
        
        return {
            "status": "success",
            "message": f"Versión '{version_name}' actualizada",
            "new_timestamp": self.versions[version_name]["timestamp"]
        }

    def _count_nodes(self, node) -> int:
        """
        Count nodes recursively.

        Args:
            node: Root node of the subtree to count

        Returns:
            int: Number of nodes in the subtree
        """
        if node is None:
            return 0
        return 1 + self._count_nodes(node.getLeftChild()) + self._count_nodes(node.getRightChild())

    def _count_leaves(self, node) -> int:
        """
        Count leaves recursively.

        Args:
            node: Root node of the subtree to count

        Returns:
            int: Number of leaf nodes in the subtree
        """
        if node is None:
            return 0
        if node.getLeftChild() is None and node.getRightChild() is None:
            return 1
        return self._count_leaves(node.getLeftChild()) + self._count_leaves(node.getRightChild())

    def export_version_as_json(self, version_name: str) -> str:
        """
        Export a version as JSON string.

        Args:
            version_name (str): Name of the version

        Returns:
            str: JSON string with the version data
        """
        import json
        if version_name not in self.versions:
            raise ValueError(f"La versión '{version_name}' no existe")
        
        version = self.versions[version_name]
        return json.dumps({
            "name": version_name,
            "timestamp": version["timestamp"],
            "metrics": version["metrics"],
            "tree_data": version["tree_data"]
        }, indent=2, ensure_ascii=False)

    def compare_versions(self, version1: str, version2: str) -> dict:
        """
        Compare two versions and return their differences.

        Args:
            version1 (str): Name of the first version
            version2 (str): Name of the second version

        Returns:
            dict: Dictionary with metrics comparison
        """
        if version1 not in self.versions:
            raise ValueError(f"La versión '{version1}' no existe")
        if version2 not in self.versions:
            raise ValueError(f"La versión '{version2}' no existe")
        
        v1 = self.versions[version1]
        v2 = self.versions[version2]
        
        m1 = v1["metrics"]
        m2 = v2["metrics"]
        
        return {
            "version1": version1,
            "version2": version2,
            "comparison": {
                "height_diff": m2["height"] - m1["height"],
                "nodes_diff": m2["total_nodes"] - m1["total_nodes"],
                "leaves_diff": m2["total_leaves"] - m1["total_leaves"],
                "rotations_diff": m2.get("total_rotations", 0) - m1.get("total_rotations", 0)
            }
        }
