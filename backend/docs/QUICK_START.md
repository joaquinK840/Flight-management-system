# Guía de Inicio Rápido - Router de Vuelos

Comienza en 5 minutos con los nuevos endpoints.

## 1️⃣ Iniciar Servidor

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

El servidor estará en: `http://localhost:8000`

---

## 2️⃣ Usar Swagger UI (Visual)

Abre: `http://localhost:8000/docs`

- Verás todos los endpoints
- Puedes probar directamente desde el navegador
- Documentación auto-generada

---

## 3️⃣ Primeras Operaciones con curl

### Insertar un vuelo
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

### Insertar otro vuelo
```bash
curl -X POST "http://localhost:8000/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": 50,
    "origen": "Madrid",
    "destino": "Valencia",
    "horaSalida": "08:00",
    "precioBase": 100.00,
    "pasajeros": 150,
    "prioridad": 2
  }'
```

### Ver el árbol
```bash
curl "http://localhost:8000/flights/tree"
```

### Ver métricas
```bash
curl "http://localhost:8000/flights/metrics"
```

### Actualizar vuelo
```bash
curl -X PUT "http://localhost:8000/flights/update/100" \
  -H "Content-Type: application/json" \
  -d '{"precioBase": 160.00}'
```

### Deshacer última operación
```bash
curl -X POST "http://localhost:8000/flights/undo"
```

### Cancelar vuelo y subárbol
```bash
curl -X DELETE "http://localhost:8000/flights/cancel/50"
```

### Eliminar solo vuelo
```bash
curl -X DELETE "http://localhost:8000/flights/delete/100"
```

### Reiniciar
```bash
curl -X DELETE "http://localhost:8000/flights/reset"
```

---

## 4️⃣ Flujo Completo de Ejemplo

```bash
# Reset
curl -X DELETE "http://localhost:8000/flights/reset"

# Insertar 100
curl -X POST "http://localhost:8000/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{"codigo": 100, "origen": "Madrid", "destino": "Barcelona", "horaSalida": "10:30", "precioBase": 150.00, "pasajeros": 180, "prioridad": 1}'

# Insertar 50
curl -X POST "http://localhost:8000/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{"codigo": 50, "origen": "Madrid", "destino": "Valencia", "horaSalida": "08:00", "precioBase": 100.00, "pasajeros": 150, "prioridad": 2}'

# Insertar 150
curl -X POST "http://localhost:8000/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{"codigo": 150, "origen": "Madrid", "destino": "Malaga", "horaSalida": "12:00", "precioBase": 120.00, "pasajeros": 200, "prioridad": 1}'

# Ver árbol (debería ser balanceado)
curl "http://localhost:8000/flights/tree" | python -m json.tool

# Ver métricas
curl "http://localhost:8000/flights/metrics" | python -m json.tool

# Actualizar precio de vuelo 100
curl -X PUT "http://localhost:8000/flights/update/100" \
  -H "Content-Type: application/json" \
  -d '{"precioBase": 160.00, "promocion": true}'

# Deshacer (vuelve al precio anterior)
curl -X POST "http://localhost:8000/flights/undo"

# Rehacer (vuelve al precio actualizado)
curl -X POST "http://localhost:8000/flights/redo"
```

---

## 5️⃣ Entender el Resultado del Árbol

Cuando haces GET `/flights/tree`, recibes:

```json
{
  "status": "success",
  "tree": {
    "root": {
      "value": 100,
      "codigo": 100,
      "profundidad": 0,
      "nodoCritico": false,
      "precioFinal": 160.00,
      "datos": {
        "codigo": 100,
        "origen": "Madrid",
        "destino": "Barcelona",
        "horaSalida": "10:30",
        "precioBase": 160.00,
        "pasajeros": 180,
        "prioridad": 1,
        "promocion": true
      },
      "left": {
        "value": 50,
        "codigo": 50,
        ...
      },
      "right": {
        "value": 150,
        "codigo": 150,
        ...
      }
    }
  }
}
```

**Campos importantes:**
- `value`: Código del vuelo (clave de búsqueda)
- `datos`: Información completa del vuelo
- `profundidad`: Nivel en el árbol
- `left`/`right`: Subárboles
- `precioFinal`: Precio final calculado

---

## 6️⃣ Entender las Métricas

```json
{
  "status": "success",
  "metrics": {
    "height": 2,
    "leaves": 2,
    "total_nodes": 3,
    "rotation_counts": {
      "LL": 0,
      "RR": 0,
      "LR": 0,
      "RL": 0
    },
    "total_rotations": 2,
    "mass_cancellations": 0,
    "undo_states_available": 5,
    "tree_type": "AVL"
  }
}
```

**¿Qué significa?**
- `height`: Altura del árbol (objetivo: log n)
- `leaves`: Vuelos sin descendientes
- `total_nodes`: Total de vuelos
- `rotation_counts`: Rotaciones por tipo
- `total_rotations`: Total de balanceos
- `undo_states_available`: Operaciones que puedes deshacer
- `tree_type`: AVL (con balanceo) o BST (sin balanceo)

---

## 7️⃣ Modos de Operación

### Modo Normal (Recomendado)
✓ Árboles balanceados
✓ Búsqueda O(log n)
✓ Altura optimizada

```bash
curl -X POST "http://localhost:8000/flights/stress-mode/false"
```

### Modo Stress (Testing)
- Sin balanceo
- Búsqueda O(n) en peor caso
- Útil para comparar

```bash
curl -X POST "http://localhost:8000/flights/stress-mode/true"
```

---

## 8️⃣ Diferencia: delete vs cancel

### delete (Solo el nodo)
```bash
# Árbol antes:
#        50
#       /  \
#      25  75

curl -X DELETE "http://localhost:8000/flights/delete/50"

# Árbol después:
#        75     ← Sucesor lo reemplaza
#       /
#      25
```

### cancel (Nodo + subárbol)
```bash
# Árbol antes:
#        50
#       /  \
#      25  75
#         / \
#        60 80

curl -X DELETE "http://localhost:8000/flights/cancel/75"

# Árbol después:
#        50
#       /
#      25      ← 75 y todos sus descendientes eliminados
```

---

## 9️⃣ Estructura del Proyecto

```
backend/
├── routes/flight_routes.py    ← Los 10 endpoints
├── services/tree_repository.py ← La lógica (patrón Repository)
├── core/structures/
│   ├── avl_tree/
│   ├── bst_tree/
│   ├── node/
│   └── stack/                  ← Para undo
├── main.py                     ← Punto de entrada
└── docs/                       ← Documentación
```

---

## 🔟 Errores Comunes

| Error | Solución |
|-------|----------|
| `"El vuelo debe tener 'codigo'"` | Agrega `"codigo": XXX` al JSON |
| `"Vuelo XXX no encontrado"` | El código no existe en el árbol |
| `"No hay acciones para deshacer"` | Ya deshiciste todo, no hay más |
| `Connection refused` | ¿Corriste `uvicorn main:app`? |
| Port 8000 en uso | Cambia a otro: `--port 8001` |

---

## 📚 Documentación Completa

- **Endpoints detallados**: Ver `docs/FLIGHTS_ENDPOINTS.md`
- **Todo el proyecto**: Ver `docs/README.md`
- **Resumen de implementación**: Ver `docs/IMPLEMENTATION_SUMMARY.md`

---

## 💡 Tips Pro

1. **Postman**: Importa los ejemplos como colección
2. **jq**: Formatea JSON en terminal: `curl ... | jq`
3. **Debug**: Usa `/flights/metrics` para ver estado
4. **Pruebas**: Usa `/flights/reset` antes de cada prueba
5. **Undo**: Ilimitado - puedes deshacer cuanto quieras

---

**¡Listo para empezar! 🚀**

Abre `http://localhost:8000/docs` y comienza a explorar.
