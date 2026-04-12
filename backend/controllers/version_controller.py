"""
Version Controller - Controlador de Versionado
Orquesta las operaciones de versionado del árbol.
Arquitectura: Controller → Service → Data
"""

from services.version_service import VersionService


class VersionController:
    """
    Controlador de versionado.
    Orquesta la lógica de guardado, restauración y eliminación de versiones.
    """

    def __init__(self):
        """Inicializa el controlador con el servicio de versiones."""
        self.version_service = VersionService()

    def save_version(self, tree, version_name: str, queue=None) -> dict:
        """
        Guarda el estado actual del árbol Y COLA como una nueva versión.

        Args:
            tree: Árbol AVL/BST a guardar
            version_name: Nombre de la versión
            queue: Cola FIFO opcional a guardar

        Returns:
            Dict con confirmación, timestamp, y lista de versiones

        Raises:
            ValueError: Si el nombre está vacío o ya existe
        """
        # Validación
        if not version_name or not version_name.strip():
            raise ValueError("El nombre de la versión no puede estar vacío")

        if version_name in self.version_service.versions:
            raise ValueError(f"La versión '{version_name}' ya existe")

        # Delegamos al servicio
        result = self.version_service.save_version(tree, version_name, queue)
        return result

    def list_versions(self) -> dict:
        """
        Retorna lista de todas las versiones guardadas con información detallada.

        Returns:
            Dict con estado, cantidad total, y lista de versiones
        """
        versions = self.version_service.get_version_list()

        # Obtener información detallada de cada versión
        versions_info = []
        for version_name in versions:
            info = self.version_service.get_version_info(version_name)
            versions_info.append(info)

        return {
            "status": "success",
            "total_versions": len(versions_info),
            "versions": versions_info
        }

    def restore_version(self, tree, version_name: str, queue=None) -> dict:
        """
        Restaura el árbol Y COLA desde una versión guardada.

        Args:
            tree: Árbol AVL/BST a restaurar
            version_name: Nombre de la versión a restaurar
            queue: Cola FIFO opcional a restaurar

        Returns:
            Dict con árbol serializado restaurado y métricas

        Raises:
            ValueError: Si la versión no existe
        """
        # Validación
        if version_name not in self.version_service.versions:
            raise ValueError(f"Versión '{version_name}' no encontrada")

        # Delegamos al servicio
        result = self.version_service.restore_version(tree, version_name, queue)
        return result

    def delete_version(self, version_name: str) -> dict:
        """
        Elimina una versión guardada.

        Args:
            version_name: Nombre de la versión a eliminar

        Returns:
            Dict con confirmación de eliminación

        Raises:
            ValueError: Si la versión no existe
        """
        # Validación
        if version_name not in self.version_service.versions:
            raise ValueError(f"Versión '{version_name}' no encontrada")

        # Delegamos al servicio
        del self.version_service.versions[version_name]

        return {
            "status": "success",
            "message": f"Versión '{version_name}' eliminada",
            "versions_count": len(self.version_service.versions),
            "available_versions": self.version_service.get_version_list()
        }

    def duplicate_version(self, source_name: str, dest_name: str) -> dict:
        """
        Crea una copia de una versión existente con un nuevo nombre.

        Args:
            source_name: Versión origen a copiar
            dest_name: Nombre para la nueva copia

        Returns:
            Dict con confirmación de duplicación

        Raises:
            ValueError: Si la versión origen no existe o destino ya existe
        """
        # Validación
        if source_name not in self.version_service.versions:
            raise ValueError(f"La versión '{source_name}' no existe")

        if dest_name in self.version_service.versions:
            raise ValueError(f"La versión '{dest_name}' ya existe")

        # Copiar versión
        source_version = self.version_service.versions[source_name]
        self.version_service.versions[dest_name] = {
            "timestamp": f"{source_version['timestamp']} (copia)",
            "tree_data": source_version["tree_data"],
            "metrics": source_version["metrics"].copy(),
            "tree_type": source_version.get("tree_type", "Unknown")
        }

        return {
            "status": "success",
            "message": f"Versión '{source_name}' copiada como '{dest_name}'",
            "versions_count": len(self.version_service.versions),
            "available_versions": self.version_service.get_version_list()
        }
