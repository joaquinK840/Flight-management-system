"""
Tests for the versioning system.

Run with: pytest test_versions.py -v
"""

import json

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestVersionSave:
    """Tests for saving versions"""

    def setup_method(self):
        """Clean up before each test"""
        # Reset
        client.delete("/flights/reset")
        client.delete("/versions/clear/all")
        
        # Insertar datos de prueba
        flights = [
            {"codigo": 100, "origen": "Madrid", "destino": "Barcelona", "horaSalida": "10:30", "precioBase": 150.00, "pasajeros": 180, "prioridad": 1},
            {"codigo": 50, "origen": "Madrid", "destino": "Valencia", "horaSalida": "08:00", "precioBase": 100.00, "pasajeros": 150, "prioridad": 2},
            {"codigo": 150, "origen": "Madrid", "destino": "Malaga", "horaSalida": "12:00", "precioBase": 120.00, "pasajeros": 200, "prioridad": 1},
        ]
        for flight in flights:
            client.post("/flights/insert", json=flight)

    def test_save_version(self):
        """Should save a version"""
        response = client.post("/versions/save", json={"name": "Test Version"})
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert "Test Version" in response.json()["available_versions"]

    def test_save_duplicate_name(self):
        """Should reject duplicate name"""
        client.post("/versions/save", json={"name": "Version 1"})
        response = client.post("/versions/save", json={"name": "Version 1"})
        assert response.status_code == 400

    def test_save_empty_name(self):
        """Should reject empty name"""
        response = client.post("/versions/save", json={"name": ""})
        assert response.status_code == 400


class TestVersionList:
    """Tests for listing versions"""

    def setup_method(self):
        """Prepare data"""
        client.delete("/flights/reset")
        client.delete("/versions/clear/all")
        
        # Guardar varias versiones
        for i in range(3):
            flight = {"codigo": 100 + i, "origen": "Madrid", "destino": "City", "horaSalida": "10:00", "precioBase": 100.00, "pasajeros": 100, "prioridad": 1}
            client.post("/flights/insert", json=flight)
            client.post("/versions/save", json={"name": f"Version {i+1}"})

    def test_list_versions(self):
        """Should list all versions"""
        response = client.get("/versions/list")
        assert response.status_code == 200
        assert response.json()["total_versions"] == 3
        assert len(response.json()["versions"]) == 3

    def test_list_versions_contains_info(self):
        """Should include information for each version"""
        response = client.get("/versions/list")
        versions = response.json()["versions"]
        for version in versions:
            assert "name" in version
            assert "timestamp" in version
            assert "metrics" in version


class TestVersionRestore:
    """Tests for restoring versions"""

    def setup_method(self):
        """Prepare data"""
        client.delete("/flights/reset")
        client.delete("/versions/clear/all")
        
        # Crear versión 1 con 3 vuelos
        for i in range(3):
            flight = {"codigo": 100 + i, "origen": "Madrid", "destino": f"City{i}", "horaSalida": "10:00", "precioBase": 100.00 + i*10, "pasajeros": 100 + i*10, "prioridad": 1}
            client.post("/flights/insert", json=flight)
        client.post("/versions/save", json={"name": "Version 1"})
        
        # Crear versión 2 con más vuelos
        for i in range(3, 5):
            flight = {"codigo": 100 + i, "origen": "Barcelona", "destino": f"City{i}", "horaSalida": "11:00", "precioBase": 100.00 + i*10, "pasajeros": 100 + i*10, "prioridad": 2}
            client.post("/flights/insert", json=flight)
        client.post("/versions/save", json={"name": "Version 2"})

    def test_restore_version(self):
        """Debe restaurar una versión"""
        # Restaurar Version 1 (3 vuelos)
        response = client.post("/versions/restore/Version%201")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["metrics"]["total_nodes"] == 3

    def test_restore_nonexistent(self):
        """Debe fallar restaurando versión inexistente"""
        response = client.post("/versions/restore/Nonexistent")
        assert response.status_code == 404

    def test_restore_changes_tree(self):
        """Restaurar debe cambiar el árbol actual"""
        # Restaurar Version 1
        client.post("/versions/restore/Version%201")
        
        # Verificar que el árbol tiene 3 nodos
        metrics = client.get("/flights/metrics").json()["metrics"]
        assert metrics["total_nodes"] == 3


class TestVersionDelete:
    """Tests para eliminar versiones"""

    def setup_method(self):
        """Preparar datos"""
        client.delete("/flights/reset")
        client.delete("/versions/clear/all")
        
        client.post("/flights/insert", json={"codigo": 100, "origen": "Madrid", "destino": "Barcelona", "horaSalida": "10:00", "precioBase": 100.00, "pasajeros": 100, "prioridad": 1})
        client.post("/versions/save", json={"name": "To Delete"})
        client.post("/versions/save", json={"name": "To Keep"})

    def test_delete_version(self):
        """Debe eliminar una versión"""
        response = client.delete("/versions/To%20Delete")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert "To Delete" not in response.json()["available_versions"]

    def test_delete_nonexistent(self):
        """Debe fallar eliminando versión inexistente"""
        response = client.delete("/versions/Nonexistent")
        assert response.status_code == 404


class TestVersionInfo:
    """Tests para obtener información de versiones"""

    def setup_method(self):
        """Preparar datos"""
        client.delete("/flights/reset")
        client.delete("/versions/clear/all")
        
        client.post("/flights/insert", json={"codigo": 100, "origen": "Madrid", "destino": "Barcelona", "horaSalida": "10:00", "precioBase": 100.00, "pasajeros": 100, "prioridad": 1})
        client.post("/versions/save", json={"name": "Test"})

    def test_get_version_info(self):
        """Debe obtener información de versión"""
        response = client.get("/versions/Test/info")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        version_info = response.json()["version"]
        assert version_info["name"] == "Test"
        assert "metrics" in version_info
        assert version_info["tree_type"] == "AVL"


class TestVersionCompare:
    """Tests para comparar versiones"""

    def setup_method(self):
        """Preparar datos"""
        client.delete("/flights/reset")
        client.delete("/versions/clear/all")
        
        # Version 1: 1 vuelo
        client.post("/flights/insert", json={"codigo": 100, "origen": "Madrid", "destino": "Barcelona", "horaSalida": "10:00", "precioBase": 100.00, "pasajeros": 100, "prioridad": 1})
        client.post("/versions/save", json={"name": "Version 1"})
        
        # Version 2: 3 vuelos
        client.post("/flights/insert", json={"codigo": 50, "origen": "Madrid", "destino": "Valencia", "horaSalida": "08:00", "precioBase": 100.00, "pasajeros": 100, "prioridad": 1})
        client.post("/flights/insert", json={"codigo": 150, "origen": "Madrid", "destino": "Malaga", "horaSalida": "12:00", "precioBase": 100.00, "pasajeros": 100, "prioridad": 1})
        client.post("/versions/save", json={"name": "Version 2"})

    def test_compare_versions(self):
        """Debe comparar dos versiones"""
        response = client.post("/versions/compare/Version%201/vs/Version%202")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        comparison = response.json()["comparison"]["comparison"]
        assert comparison["nodes_diff"] == 2  # Pasó de 1 a 3 nodos


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
