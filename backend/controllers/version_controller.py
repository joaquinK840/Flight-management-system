"""
Version controller for tree versioning operations.

This module orchestrates tree versioning operations including save, restore,
delete, and duplicate functionality.
"""

from services.version_service import VersionService


class VersionController:
    """
    Controller for tree versioning operations.

    Orchestrates the logic for saving, restoring, and managing tree versions.
    """

    def __init__(self):
        """Initialize the controller with the version service."""
        self.version_service = VersionService()

    def save_version(self, tree, version_name: str, queue=None) -> dict:
        """
        Save the current tree AND queue state as a new version.

        Args:
            tree: AVL/BST tree to save
            version_name (str): Name for the version
            queue: Optional FIFO queue to save

        Returns:
            dict: Confirmation with timestamp and version list

        Raises:
            ValueError: If name is empty or already exists
        """
        # Validation
        if not version_name or not version_name.strip():
            raise ValueError("Version name cannot be empty")

        if version_name in self.version_service.versions:
            raise ValueError(f"Version '{version_name}' already exists")

        # Delegate to service
        result = self.version_service.save_version(tree, version_name, queue)
        return result

    def list_versions(self) -> dict:
        """
        Return list of all saved versions with detailed information.

        Returns:
            dict: Status, total count, and list of versions with metadata
        """
        versions_info = []
        for name, data in self.version_service.versions.items():
            versions_info.append({
                "name": name,
                "created_at": data.get("timestamp", ""),
                "total_nodes": data.get("metrics", {}).get("total_nodes", 0),
                "height": data.get("metrics", {}).get("height", 0)
            })

        return {"versions": versions_info, "count": len(versions_info)}

    def restore_version(self, tree, version_name: str, queue=None) -> dict:
        """
        Restore tree AND queue from a saved version.

        Args:
            tree: AVL/BST tree to restore
            version_name (str): Name of version to restore
            queue: Optional FIFO queue to restore

        Returns:
            dict: Restored serialized tree and metrics

        Raises:
            ValueError: If version does not exist
        """
        # Validation
        if version_name not in self.version_service.versions:
            raise ValueError(f"Version '{version_name}' not found")

        # Delegate to service
        result = self.version_service.restore_version(tree, version_name, queue)
        return result

    def delete_version(self, version_name: str) -> dict:
        """
        Delete a saved version.

        Args:
            version_name (str): Name of version to delete

        Returns:
            dict: Deletion confirmation

        Raises:
            ValueError: If version does not exist
        """
        # Validation
        if version_name not in self.version_service.versions:
            raise ValueError(f"Version '{version_name}' not found")

        # Delegate to service
        del self.version_service.versions[version_name]

        return {
            "status": "success",
            "message": f"Version '{version_name}' deleted",
            "versions_count": len(self.version_service.versions),
            "available_versions": self.version_service.get_version_list()
        }

    def duplicate_version(self, source_name: str, dest_name: str) -> dict:
        """
        Create a copy of an existing version with a new name.

        Args:
            source_name (str): Source version to copy
            dest_name (str): Name for the new copy

        Returns:
            dict: Duplication confirmation

        Raises:
            ValueError: If source doesn't exist or destination already exists
        """
        # Validation
        if source_name not in self.version_service.versions:
            raise ValueError(f"Version '{source_name}' does not exist")

        if dest_name in self.version_service.versions:
            raise ValueError(f"Version '{dest_name}' already exists")

        # Copy version
        source_version = self.version_service.versions[source_name]
        self.version_service.versions[dest_name] = {
            "timestamp": f"{source_version['timestamp']} (copy)",
            "tree_data": source_version["tree_data"],
            "metrics": source_version["metrics"].copy(),
            "tree_type": source_version.get("tree_type", "Unknown")
        }

        return {
            "status": "success",
            "message": f"Version '{source_name}' copied as '{dest_name}'",
            "versions_count": len(self.version_service.versions),
            "available_versions": self.version_service.get_version_list()
        }
