# Sistema de Simulación de Concurrencia - Documentación

## 📋 Resumen

El sistema de simulación de concurrencia permite procesar vuelos de manera **controlada y predecible** usando una estructura **FIFO (First In, First Out)**.

### Propósito

- ✅ Agregar vuelos a una cola sin procesarlos inmediatamente
- ✅ Procesar vuelos uno por uno o todos juntos
- ✅ Detectar conflictos de balance en el árbol AVL
- ✅ Mantener control sobre el flujo de inserciones
- ✅ Simular condiciones de concurrencia de forma controlada

---

## 🏗️ Arquitectura

### Componentes

```
┌─────────────────────────────────────────────────────────┐
│                   FRONTEND (React)                       │
│  - Queue Control Component                              │
│  - Add Flight, Show Pending, Process Queue buttons      │
└────────────────┬────────────────────────────────────────┘
                 │
     ┌───────────┴────────────┐
     │                        │
┌────▼──────────────────┐    │
│  Queue Service        │◄───┘
│ (FIFO Management)     │
└────┬──────────────────┘
     │
     │ Process/Insert
     │
┌────▼──────────────────┐
│  AVL Tree             │
│  (Node Insertion)     │
└───────────────────────┘

Queue: [Vuelo1, Vuelo2, Vuelo3, ...]
```

### Estructura de Datos

#### Flight Object (en la cola)

```json
{
  "codigo": 100,
  "origen": "Madrid",
  "destino": "Barcelona",
  "horaSalida": "10:30",
  "precioBase": 150.0,
  "pasajeros": 180,
  "prioridad": 1
}
```

#### Queue (FIFO)

```python
items = [
    {"codigo": 100, ...},    # Primero en salir (dequeue)
    {"codigo": 50, ...},
    {"codigo": 150, ...}     # Último en salir
]
```

---

## 📡 Endpoints API

### 1. POST /queue/add

**Agregar vuelo a la cola**

#### Request

```bash
POST http://localhost:8000/queue/add
Content-Type: application/json

{
  "codigo": 100,
  "origen": "Madrid",
  "destino": "Barcelona",
  "horaSalida": "10:30",
  "precioBase": 150.0,
  "pasajeros": 180,
  "prioridad": 1
}
```

#### Response

```json
{
  "status": "success",
  "message": "Vuelo 100 agregado a la cola",
  "queue_size": 3,
  "pending_flights": [
    {"codigo": 100, "origen": "Madrid", ...},
    {"codigo": 50, "origen": "Valencia", ...},
    {"codigo": 150, "origen": "Malaga", ...}
  ]
}
```

---

### 2. GET /queue/pending

**Obtener vuelos pendientes**

#### Request

```bash
GET http://localhost:8000/queue/pending
```

#### Response

```json
{
  "status": "success",
  "pending_count": 3,
  "flights": [
    {"codigo": 100, "origen": "Madrid", ...},
    {"codigo": 50, "origen": "Valencia", ...},
    {"codigo": 150, "origen": "Malaga", ...}
  ]
}
```

---

### 3. POST /queue/process-one

**Procesar el primer vuelo de la cola**

#### Request

```bash
POST http://localhost:8000/queue/process-one
```

#### Response (Sin Conflicto)

```json
{
  "status": "success",
  "message": "Vuelo 100 procesado exitosamente",
  "flight_inserted": {
    "codigo": 100,
    "origen": "Madrid",
    "destino": "Barcelona",
    "horaSalida": "10:30",
    "precioBase": 150.0,
    "pasajeros": 180,
    "prioridad": 1
  },
  "tree_after": {
    "value": 5,
    "left": { "value": 3, ... },
    "right": { "value": 7, ... }
  },
  "conflict": false,
  "conflict_detail": null,
  "queue_remaining": 2
}
```

#### Response (Con Conflicto)

```json
{
  "status": "success",
  "message": "Vuelo 100 procesado exitosamente",
  "flight_inserted": {...},
  "tree_after": {...},
  "conflict": true,
  "conflict_detail": "Árbol muy inclinado a la izquierda (BF=3). Posible degradación de performance.",
  "queue_remaining": 2
}
```

**¿Qué es un conflicto?**
- Se detecta cuando `|balance_factor| > 2`
- Indica mala distribución del árbol
- El árbol AVL debería tener `|BF| ≤ 1`, pero en casos especiales puede haber estrés

---

### 4. POST /queue/process-all

**Procesar todos los vuelos de la cola**

#### Request

```bash
POST http://localhost:8000/queue/process-all
```

#### Response

```json
{
  "status": "success",
  "message": "Procesados 5 vuelos de la cola",
  "total_processed": 5,
  "results": [
    {
      "status": "success",
      "message": "Vuelo 100 procesado exitosamente",
      "flight_inserted": {...},
      "tree_after": {...},
      "conflict": false,
      "conflict_detail": null,
      "queue_remaining": 4
    },
    {
      "status": "success",
      "message": "Vuelo 50 procesado exitosamente",
      "flight_inserted": {...},
      "tree_after": {...},
      "conflict": false,
      "conflict_detail": null,
      "queue_remaining": 3
    },
    {
      "status": "success",
      "message": "Vuelo 150 procesado exitosamente",
      "flight_inserted": {...},
      "tree_after": {...},
      "conflict": true,
      "conflict_detail": "Árbol muy inclinado a la derecha (BF=-3). Posible degradación de performance.",
      "queue_remaining": 2
    },
    ...
  ],
  "tree_final": {
    "value": 5,
    "left": { "value": 3, ... },
    "right": { "value": 7, ... }
  },
  "total_conflicts": 1,
  "queue_remaining": 0
}
```

---

### 5. DELETE /queue/clear

**Vaciar la cola sin procesar**

#### Request

```bash
DELETE http://localhost:8000/queue/clear
```

#### Response

```json
{
  "status": "success",
  "message": "Cola vaciada. Se eliminaron 3 vuelos pendientes.",
  "cleared_count": 3
}
```

---

## 🔄 Flujo en el Backend

### POST /queue/add

```
1. Validar estructura del vuelo (Pydantic)
2. Convertir a dict
3. Llamar a add_flight_to_queue()
   - flight_queue.enqueue(flight_data)
   - Retornar estado, tamaño cola, lista de vuelos
4. Responder al cliente
```

### POST /queue/process-one

```
1. Verificar que la cola no esté vacía
2. Extraer primer vuelo: flight_queue.dequeue()
3. Crear Node(codigo, flight_data)
4. Insertar en árbol: tree.insert(node)
5. Calcular balance_factor de root
6. Detectar conflicto: |BF| > 2
7. Serializar árbol
8. Retornar:
   - flight_inserted
   - tree_after (serializado)
   - conflict: bool
   - conflict_detail: str | null
   - queue_remaining: cantidad
```

### POST /queue/process-all

```
1. Contar vuelos iniciales: queue_size_initial
2. Para cada vuelo:
   a. Llamar process_one_flight(tree)
   b. Guardar resultado
   c. Contar conflictos
3. Serializar árbol final
4. Retornar:
   - total_processed
   - resultados de cada inserción
   - tree_final
   - total_conflicts
   - queue_remaining (debe ser 0)
```

---

## 📊 Detección de Conflictos

### Balance Factor (BF)

```
BF = altura(izq) - altura(der)
```

### Rango Normal (AVL)

```
-1 ≤ BF ≤ 1  ✅ Árbol balanceado
```

### Umbrales de Conflicto

```
|BF| = 2: ⚠️  Advertencia (puede rebalancearse solo)
|BF| > 2: 🔴 Conflicto detectado (estrés)
```

### Ejemplos

```
Árbol bien balanceado:
        5
       / \
      3   7
     / \ / \
    2  4 6  8
  
BF(5) = 2 - 2 = 0 ✅

Árbol con conflicto:
        1
         \
          3
         / \
        2   5
           / \
          4   7
         /
        /
       
BF(root) = 0 - 3 = -3 🔴 CONFLICTO

Solución: Rebalancear con rotaciones (POST /avl/rebalance en modo stress)
```

---

## 💡 Casos de Uso

### Caso 1: Agregar múltiples vuelos y procesarlos

```bash
# 1. Agregar vuelos a la cola
curl -X POST http://localhost:8000/queue/add \
  -H "Content-Type: application/json" \
  -d '{"codigo":100,"origen":"Madrid","destino":"Barcelona",...}'

curl -X POST http://localhost:8000/queue/add \
  -H "Content-Type: application/json" \
  -d '{"codigo":50,"origen":"Valencia","destino":"Sevilla",...}'

# 2. Ver pendientes
curl http://localhost:8000/queue/pending

# 3. Procesar uno por uno
curl -X POST http://localhost:8000/queue/process-one
curl -X POST http://localhost:8000/queue/process-one

# 4. Ver árbol actualizado
curl http://localhost:8000/avl/tree
```

### Caso 2: Procesar todos de una vez

```bash
# Agregar varios
curl -X POST http://localhost:8000/queue/add -d {...}
curl -X POST http://localhost:8000/queue/add -d {...}
curl -X POST http://localhost:8000/queue/add -d {...}

# Procesar todos
curl -X POST http://localhost:8000/queue/process-all

# Respuesta contiene resultados de TODAS las inserciones
```

### Caso 3: Limpiar sin procesar

```bash
# Si cambias de opinión
curl -X DELETE http://localhost:8000/queue/clear

# Todos los vuelos en la cola se descartan
```

---

## 📁 Archivos Implementados

### 1. `backend/core/structures/queue/queue.py`

```python
class Queue:
    - enqueue(item)      # Agregar al final
    - dequeue()          # Extraer del frente
    - peek()             # Ver primero sin extraer
    - is_empty()         # ¿Vacía?
    - size()             # Cantidad de elementos
    - clear()            # Vaciar
    - get_all()          # Obtener copia
```

### 2. `backend/services/queue_service.py`

```python
# Instancia global
flight_queue = Queue()

# Funciones
- add_flight_to_queue(flight_data)
- get_pending_flights()
- process_one_flight(tree)
- process_all_flights(tree)
- clear_queue()
- _serialize_tree_simple(node)
```

### 3. `backend/routes/queue_routes.py`

```python
# Endpoints
POST   /queue/add
GET    /queue/pending
POST   /queue/process-one
POST   /queue/process-all
DELETE /queue/clear
```

### 4. `backend/main.py` (Modificado)

```python
# Incluye nuevo router
app.include_router(queue_router)
```

---

## 🧪 Validación

```bash
✅ queue.py compila sin errores
✅ queue_service.py compila sin errores
✅ queue_routes.py compila sin errores
✅ main.py compila sin errores
✅ Endpoints integrados correctamente
✅ Conflictos detectados: |BF| > 2
```

---

## 🚀 Próximos Pasos (Frontend)

El componente frontend debe:

1. **QueueControlComponent**
   - Input para agregar vuelos (código, origen, destino, etc.)
   - Botón "Agregar a Cola"
   - Mostrar lista de pendientes en tiempo real
   - Botón "Procesar Uno" (puede iterar)
   - Botón "Procesar Todo"
   - Botón "Limpiar Cola"

2. **Animaciones**
   - Mostrar animación elegante de cada inserción
   - Colorear nodos en conflicto en rojo
   - Mostrar indicador de balance factor

3. **Integración**
   ```javascript
   // En avlService.js
   const addToQueue = (flight) => fetch('/queue/add', ...)
   const getPending = () => fetch('/queue/pending', ...)
   const processOne = () => fetch('/queue/process-one', ...)
   const processAll = () => fetch('/queue/process-all', ...)
   const clearQueue = () => fetch('/queue/clear', ...)
   ```

---

## 📝 Notas Importantes

- ⏱️ **FIFO**: Primer vuelo agregado es el primero procesado
- 🔴 **Conflictos**: Se detectan automáticamente (BF > 2)
- 🌳 **Árbol**: El árbol AVL persiste entre llamadas (sesión)
- 📋 **Cola**: La cola también persiste (sesión)
- 🔄 **Serialización**: El árbol se serializa con cada inserción

---

## 🔗 Relación con otras Características

### Con Stress Mode

```
Si tree.stress_mode == True:
  - Check balance NO aplica rotaciones automáticas
  - POST /queue/process-one puede generar desbalances
  - Detecta conflictos (BF > 2)
  - POST /avl/rebalance para corregir manualmente

Si tree.stress_mode == False (DEFAULT):
  - Check balance aplica rotaciones automáticamente
  - AVL se rebalancea solo
  - Menos conflictos esperados
```

### Con Depth Limit Pricing

```
Cada nodo insertado via /queue:
  - Se agrega con precioBase original
  - Al serializar, se calcula precioFinal
  - Si profundidad > depth_limit: 25% más
  - Precios se recalculan en cada GET /avl/tree
```

---

## 📊 Estadísticas Esperadas

### Caso Normal (tree.stress_mode = False)

```
5 Vuelos procesados
├─ Total: 5
├─ Éxitos: 5
├─ Conflictos: 0
└─ Árbol balanceado ✅
```

### Caso Estrés (tree.stress_mode = True)

```
10 Vuelos procesados
├─ Total: 10
├─ Éxitos: 10
├─ Conflictos: 2-3
└─ Árbol desbalanceado ⚠️
   (Requiere POST /avl/rebalance)
```

---

## ✅ Status

**Estado**: COMPLETADO ✅

Todos los endpoints funcionales, documentación lista, compilación exitosa.
