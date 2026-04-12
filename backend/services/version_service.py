"""
Servicio de Versionado de Árboles
Permite guardar, restaurar y gestionar versiones completas del árbol AVL.
"""

from datetime import datetime
from typing import Dict, Optional, List
from core.structures.node.node import Node
from core.structures.avl_tree.balance import update_height


class VersionService:
    """
    Servicio de versionado para árboles.
    Mantiene un diccionario de versiones guardadas del árbol completo.
    """

    def __init__(self):
        """
        Inicializa el servicio de versionado.
        
        Estructura:
        {
            "nombre_version": {
                "timestamp": "2026-04-12 10:30:45",
                "tree_data": { nodo serializado },
                "metrics": { altura, nodos, hojas, etc }
            }
        }
        """
        self.versions: Dict[str, dict] = {}

    def save_version(self, tree, version_name: str) -> dict:
        """
        Guarda el estado actual del árbol como una nueva versión.
        Serializa la estructura jerárquica completa del árbol.
        
        Args:
            tree: Árbol AVL/BST a guardar
            version_name: Nombre de la versión
            
        Returns:
            Dict con confirmación, timestamp, y lista de versiones
            
        Raises:
            ValueError: Si el nombre ya existe o está vacío
        """
        if not version_name or not version_name.strip():
            raise ValueError("El nombre de la versión no puede estar vacío")
        
        if version_name in self.versions:
            raise ValueError(f"La versión '{version_name}' ya existe")
        
        # Serializar el árbol completo (estructura jerárquica)
        tree_data = self._serialize_tree_complete(tree.getRoot())
        
        # Calcular métricas
        metrics = self._calculate_metrics(tree)
        
        # Guardar versión
        self.versions[version_name] = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tree_data": tree_data,
            "metrics": metrics,
            "tree_type": "AVL" if hasattr(tree, 'rotation_counts') else "BST"
        }
        
        return {
            "status": "success",
            "message": f"Versión '{version_name}' guardada",
            "timestamp": self.versions[version_name]["timestamp"],
            "versions_count": len(self.versions),
            "available_versions": self.get_version_list()
        }

    def _serialize_tree_complete(self, node):
        """
        Serializa un árbol completo preservando la estructura jerárquica.
        Importante: Guarda value, datos, height, left, right para reconstrucción exacta.
        
        Args:
            node: Nodo raíz del árbol
            
        Returns:
            Dict con estructura completa del árbol
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
        Calcula métricas del árbol para guardar en la versión.
        
        Args:
            tree: Árbol a medir
            
        Returns:
            Dict con métricas
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
        Retorna lista de nombres de versiones guardadas.
        
        Returns:
            Lista de nombres de versiones
        """
        return list(self.versions.keys())

    def get_version_info(self, version_name: str) -> dict:
        """
        Obtiene información detallada de una versión.
        
        Args:
            version_name: Nombre de la versión
            
        Returns:
            Dict con información de la versión
            
        Raises:
            ValueError: Si la versión no existe
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

    def restore_version(self, tree, version_name: str) -> dict:
        """
        Restaura un árbol desde una versión guardada.
        Reconstruye exactamente la topología original con las mismas alturas.
        
        Args:
            tree: Árbol destino (se limpiará y llenará)
            version_name: Nombre de la versión a restaurar
            
        Returns:
            Dict con confirmación y árbol restaurado serializado
            
        Raises:
            ValueError: Si la versión no existe
        """
        if version_name not in self.versions:
            raise ValueError(f"La versión '{version_name}' no existe")
        
        version_data = self.versions[version_name]
        tree_data = version_data["tree_data"]
        
        # Reconstruir el árbol desde el estado serializado
        new_root = self._deserialize_tree_complete(tree_data)
        
        # Asignar nueva raíz al árbol
        tree.root = new_root
        
        # Restaurar contador de cancelaciones si aplica
        if hasattr(tree, 'mass_cancellation_count'):
            tree.mass_cancellation_count = version_data["metrics"].get("mass_cancellations", 0)
        
        # Restaurar conteos de rotaciones si aplica
        if hasattr(tree, 'rotation_counts'):
            tree.rotation_counts = version_data["metrics"].get("rotation_counts", {}).copy()
        
        return {
            "status": "success",
            "message": f"Versión '{version_name}' restaurada",
            "restored_from": version_data["timestamp"],
            "metrics": version_data["metrics"],
            "tree": self._serialize_tree_complete(new_root)
        }

    def _deserialize_tree_complete(self, tree_data):
        """
        Reconstruye un árbol desde datos serializados.
        Mantiene la estructura jerárquica original.
        
        Args:
            tree_data: Dict con estructura del árbol
            
        Returns:
            Nodo raíz del árbol reconstruido
        """
        if tree_data is None:
            return None
        
        # Crear nodo con valor, datos y altura
        node = Node(tree_data["value"], datos=tree_data.get("datos"))
        node.setHeight(tree_data.get("height", 1))
        
        # Reconstruir subárboles
        left_child = self._deserialize_tree_complete(tree_data.get("left"))
        right_child = self._deserialize_tree_complete(tree_data.get("right"))
        
        # Conectar subárboles
        if left_child:
            node.setLeftChild(left_child)
            left_child.setParent(node)
        
        if right_child:
            node.setRightChild(right_child)
            right_child.setParent(node)
        
        return node

    def delete_version(self, version_name: str) -> dict:
        """
        Elimina una versión guardada.
        
        Args:
            version_name: Nombre de la versión a eliminar
            
        Returns:
            Dict con confirmación
            
        Raises:
            ValueError: Si la versión no existe
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
        Elimina todas las versiones guardadas.
        
        Returns:
            Dict con confirmación
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
        Sobrescribe una versión existente con el estado actual del árbol.
        
        Args:
            tree: Árbol actual
            version_name: Nombre de la versión a sobrescribir
            
        Returns:
            Dict con confirmación
            
        Raises:
            ValueError: Si la versión no existe
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
        """Cuenta nodos recursivamente."""
        if node is None:
            return 0
        return 1 + self._count_nodes(node.getLeftChild()) + self._count_nodes(node.getRightChild())

    def _count_leaves(self, node) -> int:
        """Cuenta hojas recursivamente."""
        if node is None:
            return 0
        if node.getLeftChild() is None and node.getRightChild() is None:
            return 1
        return self._count_leaves(node.getLeftChild()) + self._count_leaves(node.getRightChild())

    def export_version_as_json(self, version_name: str) -> str:
        """
        Exporta una versión como string JSON.
        
        Args:
            version_name: Nombre de la versión
            
        Returns:
            String JSON con la versión
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
        Compara dos versiones y retorna sus diferencias.
        
        Args:
            version1: Nombre de la primera versión
            version2: Nombre de la segunda versión
            
        Returns:
            Dict con comparación de métricas
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
