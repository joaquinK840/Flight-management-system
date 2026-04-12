"""
Tests básicos para endpoints de vuelos.
Ejecutar con: pytest test_flight_endpoints.py -v
"""

import pytest
import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestFlightInsert:
    """Tests para inserción de vuelos"""

    def test_insert_valid_flight(self):
        """Debe insertar un vuelo válido"""
        flight = {
            "codigo": 100,
            "origen": "Madrid",
            "destino": "Barcelona",
            "horaSalida": "10:30",
            "precioBase": 150.00,
            "pasajeros": 180,
            "prioridad": 1,
            "promocion": False,
            "alerta": "normal"
        }
        response = client.post("/flights/insert", json=flight)
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert "tree" in response.json()

    def test_insert_missing_codigo(self):
        """Debe fallar si falta 'codigo'"""
        flight = {
            "origen": "Madrid",
            "destino": "Barcelona",
            "horaSalida": "10:30",
            "precioBase": 150.00,
            "pasajeros": 180,
            "prioridad": 1
        }
        response = client.post("/flights/insert", json=flight)
        assert response.status_code == 400

    def test_insert_multiple_flights(self):
        """Debe insertar múltiples vuelos"""
        # Reset first
        client.delete("/flights/reset")

        flights = [
            {"codigo": 100, "origen": "Madrid", "destino": "Barcelona", "horaSalida": "10:30", "precioBase": 150.00, "pasajeros": 180, "prioridad": 1},
            {"codigo": 50, "origen": "Madrid", "destino": "Valencia", "horaSalida": "08:00", "precioBase": 100.00, "pasajeros": 150, "prioridad": 2},
            {"codigo": 150, "origen": "Madrid", "destino": "Malaga", "horaSalida": "12:00", "precioBase": 120.00, "pasajeros": 200, "prioridad": 1},
        ]

        for flight in flights:
            response = client.post("/flights/insert", json=flight)
            assert response.status_code == 200


class TestFlightDelete:
    """Tests para eliminación de vuelos"""

    def setup_method(self):
        """Setup antes de cada test"""
        client.delete("/flights/reset")
        
        # Insertar vuelos de prueba
        flights = [
            {"codigo": 100, "origen": "Madrid", "destino": "Barcelona", "horaSalida": "10:30", "precioBase": 150.00, "pasajeros": 180, "prioridad": 1},
            {"codigo": 50, "origen": "Madrid", "destino": "Valencia", "horaSalida": "08:00", "precioBase": 100.00, "pasajeros": 150, "prioridad": 2},
            {"codigo": 150, "origen": "Madrid", "destino": "Malaga", "horaSalida": "12:00", "precioBase": 120.00, "pasajeros": 200, "prioridad": 1},
        ]
        for flight in flights:
            client.post("/flights/insert", json=flight)

    def test_delete_existing_flight(self):
        """Debe eliminar un vuelo existente"""
        response = client.delete("/flights/delete/100")
        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_delete_nonexistent_flight(self):
        """Debe fallar al eliminar vuelo inexistente"""
        response = client.delete("/flights/delete/999)
        assert response.status_code == 404


class TestFlightUpdate:
    """Tests para actualización de vuelos"""

    def setup_method(self):
        """Setup antes de cada test"""
        client.delete("/flights/reset")
        
        flight = {
            "codigo": 100,
            "origen": "Madrid",
            "destino": "Barcelona",
            "horaSalida": "10:30",
            "precioBase": 150.00,
            "pasajeros": 180,
            "prioridad": 1
        }
        client.post("/flights/insert", json=flight)

    def test_update_flight_price(self):
        """Debe actualizar el precio de un vuelo"""
        update_data = {"precioBase": 160.00}
        response = client.put("/flights/update/100", json=update_data)
        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_update_nonexistent_flight(self):
        """Debe fallar al actualizar vuelo inexistente"""
        update_data = {"precioBase": 160.00}
        response = client.put("/flights/update/999", json=update_data)
        assert response.status_code == 404


class TestUndo:
    """Tests para funcionalidad de undo"""

    def setup_method(self):
        """Setup antes de cada test"""
        client.delete("/flights/reset")

    def test_undo_insert(self):
        """Debe deshacer una inserción"""
        flight = {
            "codigo": 100,
            "origen": "Madrid",
            "destino": "Barcelona",
            "horaSalida": "10:30",
            "precioBase": 150.00,
            "pasajeros": 180,
            "prioridad": 1
        }
        client.post("/flights/insert", json=flight)
        
        # Undo
        response = client.post("/flights/undo")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["undo_remaining"] >= 0

    def test_undo_empty(self):
        """Debe fallar si no hay operaciones para deshacer"""
        response = client.post("/flights/undo")
        assert response.status_code == 400


class TestMetrics:
    """Tests para métricas"""

    def setup_method(self):
        """Setup antes de cada test"""
        client.delete("/flights/reset")
        
        # Insertar algunos vuelos
        flights = [
            {"codigo": 100, "origen": "Madrid", "destino": "Barcelona", "horaSalida": "10:30", "precioBase": 150.00, "pasajeros": 180, "prioridad": 1},
            {"codigo": 50, "origen": "Madrid", "destino": "Valencia", "horaSalida": "08:00", "precioBase": 100.00, "pasajeros": 150, "prioridad": 2},
        ]
        for flight in flights:
            client.post("/flights/insert", json=flight)

    def test_get_metrics(self):
        """Debe retornar métricas del árbol"""
        response = client.get("/flights/metrics")
        assert response.status_code == 200
        metrics = response.json()["metrics"]
        assert "height" in metrics
        assert "leaves" in metrics
        assert "total_nodes" in metrics
        assert metrics["total_nodes"] == 2


class TestStressMode:
    """Tests para stress mode"""

    def test_enable_stress_mode(self):
        """Debe activar stress mode"""
        response = client.post("/flights/stress-mode/true")
        assert response.status_code == 200
        assert response.json()["stress_mode"] == True

    def test_disable_stress_mode(self):
        """Debe desactivar stress mode"""
        response = client.post("/flights/stress-mode/false")
        assert response.status_code == 200
        assert response.json()["stress_mode"] == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
