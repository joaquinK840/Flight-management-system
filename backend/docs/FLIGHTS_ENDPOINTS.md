# Endpoints de Vuelos (Flights)

## Resumen de Arquitectura

El sistema implementa el **patrón Repository** para encapsular la lógica del árbol y la gestión de undo:

```
┌─────────────────────────────────────┐
│   flight_routes.py (Controlador)    │  Endpoints REST
├─────────────────────────────────────┤
│   TreeRepository (Servicio)         │  Patrón Repository
│   - Maneja pila de undo (Stack)     │
│   - Serializa/deserializa estados   │
├─────────────────────────────────────┤
│   AVL / BST (Modelos)               │  Árboles
│   Node (Estructura)                 │
└─────────────────────────────────────┘
```

---

## Endpoints

### 1. POST /flights/insert
**Inserta un nuevo vuelo en el árbol.**

```bash
curl -X POST "http://localhost:8000/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": 100,
    "origen": "Madrid",
    "destino": "Barcelona",
    "horaSalida": "10:30",
    "precioBase": 150.00,
    "pasajeros": 180,
    "prioridad": 1,
    "promocion": false,
    "alerta": "normal"
  }'
```

**Comportamiento según stress_mode:**
- `stress_mode = False`: Inserta en AVL con balanceo automático
- `stress_mode = True`: Inserta sin balanceo (como BST)

**Respuesta (200):**
```json
{
  "status": "success",
  "message": "Vuelo 100 insertado",
  "tree": { /* árbol serializado */ }
}
```

---

### 2. DELETE /flights/delete/{codigo}
**Elimina un vuelo específico.**

Solo elimina el nodo; el sucesor inorder lo reemplaza.

```bash
curl -X DELETE "http://localhost:8000/flights/delete/100"
```

**Respuesta (200):**
```json
{
  "status": "success",
  "message": "Vuelo 100 eliminado",
  "tree": { /* árbol serializado */ }
}
```

---

### 3. DELETE /flights/cancel/{codigo}
**Cancela un vuelo Y TODO SU SUBÁRBOL.**

Elimina el nodo especificado y todos sus descendientes. Incrementa `mass_cancellation_count`.

```bash
curl -X DELETE "http://localhost:8000/flights/cancel/50"
```

**Respuesta (200):**
```json
{
  "status": "success",
  "message": "Vuelo 50 y subárbol cancelados",
  "tree": { /* árbol serializado */ },
  "mass_cancellations": 1
}
```

---

### 4. PUT /flights/update/{codigo}
**Actualiza datos de un vuelo sin cambiar su posición.**

Solo los campos especificados se actualizan.

```bash
curl -X PUT "http://localhost:8000/flights/update/100" \
  -H "Content-Type: application/json" \
  -d '{
    "precioBase": 160.00,
    "pasajeros": 200,
    "promocion": true
  }'
```

**Respuesta (200):**
```json
{
  "status": "success",
  "message": "Vuelo 100 actualizado",
  "tree": { /* árbol serializado */ }
}
```

---

### 5. POST /flights/undo
**Revierte la última operación.**

```bash
curl -X POST "http://localhost:8000/flights/undo"
```

**Respuesta (200):**
```json
{
  "status": "success",
  "message": "Operación deshecha",
  "tree": { /* árbol anterior */ },
  "undo_remaining": 3
}
```

---

### 6. POST /flights/redo
**Rehace la última operación deshecha.**

```bash
curl -X POST "http://localhost:8000/flights/redo"
```

**Respuesta (200):**
```json
{
  "status": "success",
  "message": "Operación rehecha",
  "tree": { /* árbol rehecho */ }
}
```

---

### 7. GET /flights/metrics
**Obtiene métricas del árbol actual.**

```bash
curl -X GET "http://localhost:8000/flights/metrics"
```

**Respuesta (200):**
```json
{
  "status": "success",
  "metrics": {
    "height": 4,
    "leaves": 3,
    "total_nodes": 7,
    "rotation_counts": {
      "LL": 1,
      "RR": 0,
      "LR": 1,
      "RL": 0
    },
    "total_rotations": 2,
    "mass_cancellations": 0,
    "undo_states_available": 5,
    "tree_type": "AVL"
  }
}
```

---

### 8. GET /flights/tree
**Retorna el árbol serializado completo.**

```bash
curl -X GET "http://localhost:8000/flights/tree"
```

**Respuesta (200):**
```json
{
  "status": "success",
  "tree": {
    "root": {
      "value": 100,
      "codigo": 100,
      "profundidad": 0,
      "datos": {
        "codigo": 100,
        "origen": "Madrid",
        "destino": "Barcelona",
        ...
      },
      "left": { /* subárbol */ },
      "right": { /* subárbol */ }
    }
  }
}
```

---

### 9. POST /flights/stress-mode/{enabled}
**Activa/desactiva stress_mode.**

```bash
# Activar
curl -X POST "http://localhost:8000/flights/stress-mode/true"

# Desactivar
curl -X POST "http://localhost:8000/flights/stress-mode/false"
```

**Comportamiento en stress_mode:**
- AVL no aplica rotaciones (solo actualiza alturas)
- Inserciones se comportan como BST sin balanceo
- Útil para testear comportamiento sin optimización

**Respuesta (200):**
```json
{
  "status": "success",
  "stress_mode": true,
  "message": "Stress mode activado"
}
```

---

### 10. DELETE /flights/reset
**Reinicia el árbol y limpia la pila de undo.**

```bash
curl -X DELETE "http://localhost:8000/flights/reset"
```

**Respuesta (200):**
```json
{
  "status": "success",
  "message": "Árbol reiniciado"
}
```

---

## Ejemplos de Flujo Completo

### Escenario: Insertar, actualizar, deshacer

```bash
# 1. Insertar vuelo 100
POST /flights/insert
{
  "codigo": 100,
  "origen": "Madrid",
  "destino": "Barcelona",
  "horaSalida": "10:30",
  "precioBase": 150.00,
  "pasajeros": 180,
  "prioridad": 1,
  "promocion": false,
  "alerta": "normal"
}

# 2. Insertar vuelo 50
POST /flights/insert
{
  "codigo": 50,
  "origen": "Madrid",
  "destino": "Valencia",
  "horaSalida": "08:00",
  "precioBase": 100.00,
  "pasajeros": 150,
  "prioridad": 2,
  "promocion": true,
  "alerta": "normal"
}

# 3. Actualizar vuelo 100
PUT /flights/update/100
{ "precioBase": 160.00 }

# 4. Ver árbol actual
GET /flights/tree

# 5. Deshacer última operación (update)
POST /flights/undo

# 6. Ver métricas
GET /flights/metrics
```

---

## Códigos de Error

| Código | Mensaje | Causa |
|--------|---------|-------|
| 400 | `"El vuelo debe tener 'codigo'"` | Falta el código en la inserción |
| 400 | `"Al menos un campo debe ser actualizado"` | PUT sin campos en update |
| 400 | `"No hay acciones para deshacer"` | UNDO en stack vacío |
| 404 | `"Vuelo {codigo} no encontrado"` | Código inexistente en delete/cancel/update |
| 500 | `"Error interno del servidor"` | Error inesperado |

---

## Notas Importantes

1. **Pila de Undo**: Cada operación (insert, delete, update, cancel) guarda el estado anterior
2. **Stress Mode**: Alternancia entre AVL (optimizado) y BST (sin balanceo)
3. **Cancelación Masiva**: `cancel` elimina todo el subárbol, no solo el nodo
4. **Serialización**: Todos los datos del vuelo se preservan en cada nodo
5. **Single Responsibility**: TreeRepository maneja lógica, flight_routes maneja HTTP

---

## Stack en Detail

```python
# Uso interno en TreeRepository

# Guardar estado
self._save_state()  # Copia estado en undo_stack

# Restaurar
if not self.undo_stack.is_empty():
    state = self.undo_stack.pop()
    self._restore_tree_from_state(state)

# Verificar disponibilidad
undo_remaining = self.undo_stack.size()
```
