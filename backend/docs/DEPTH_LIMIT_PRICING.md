# Cálculo de Precios por Profundidad Crítica

**Fecha**: 12 de abril de 2026  
**Estado**: ✅ IMPLEMENTADO

---

## 📋 Resumen

El sistema de precios ahora se calcula automáticamente basándose en la **profundidad crítica** del árbol:

- **Nodos <= depth_limit**: Precio normal (sin cambios)
- **Nodos > depth_limit**: Precio con penalización exacta del **25%**

Cuando el usuario cambia `depth_limit` en cualquier momento, **TODOS los precios se recalculan automáticamente**.

---

## 🎯 Reglas de Precios

```
Regla 1: Profundidad Normal (depth <= depth_limit)
├─ nodoCritico = False
├─ precioFinal = precioBase
└─ Ejemplo: precioBase=100 → precioFinal=100

Regla 2: Profundidad Crítica (depth > depth_limit)
├─ nodoCritico = True
├─ precioFinal = precioBase * 1.25 (exactamente 25%)
└─ Ejemplo: precioBase=100 → precioFinal=125
```

---

## 🔌 Endpoints

### GET /avl/tree

```http
GET /avl/tree
```

**Descripción:**
- Obtiene el árbol serializado con precios calculados
- Usa `tree.depth_limit` actual
- Recalcula precios en cada llamada

**Response (200 OK):**
```json
{
    "root": {
        "value": 100,
        "codigo": 100,
        "profundidad": 0,
        "nodoCritico": false,
        "precioBase": 150.0,
        "precioFinal": 150.0,
        "datos": {...},
        "left": {
            "value": 50,
            "codigo": 50,
            "profundidad": 1,
            "nodoCritico": false,
            "precioBase": 100.0,
            "precioFinal": 100.0,
            ...
        },
        "right": {
            "value": 150,
            "codigo": 150,
            "profundidad": 1,
            "nodoCritico": false,
            "precioBase": 120.0,
            "precioFinal": 120.0,
            ...
        }
    },
    "depth_limit": 3,
    "rotations": {"LL": 0, "RR": 0, "LR": 0, "RL": 0},
    "metrics": {
        "total_nodes": 3,
        "height": 2
    }
}
```

---

### PUT /avl/depth-limit

```http
PUT /avl/depth-limit
Content-Type: application/json

{
    "limit": 4
}
```

**Descripción:**
- Actualiza el límite crítico de profundidad
- Todos los precios se recalculan automáticamente
- Retorna árbol completo con precios recalculados

**Request Body:**
```json
{
    "limit": 4  // Profundidad >= la cual se aplica penalización
}
```

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Límite de profundidad actualizado a 4",
    "depth_limit": 4,
    "tree": {
        "value": 100,
        "codigo": 100,
        "profundidad": 0,
        "nodoCritico": false,
        "precioBase": 150.0,
        "precioFinal": 150.0,
        "left": null,
        "right": {
            "value": 150,
            "profundidad": 1,
            "nodoCritico": false,
            "precioFinal": 120.0,
            "left": null,
            "right": {
                "value": 175,
                "profundidad": 2,
                "nodoCritico": false,
                "precioFinal": 140.0,
                ...
            }
        }
    },
    "metrics": {
        "total_nodes": 7,
        "height": 4
    }
}
```

**Error (400 Bad Request):**
```json
{
    "detail": "'limit' debe ser un entero no negativo"
}
```

---

## 💾 Servicios Internos

### price_calculator.py (Nueva)

**Archivo**: `backend/services/price_calculator.py`

**Responsabilidad**: Calcular precios (SRP - Single Responsibility Principle)

**Función Pura:**
```python
def calculate_final_price(
    precio_base: float, 
    depth: int, 
    limit: int
) -> tuple
```

**Parámetros:**
- `precio_base`: Precio base del vuelo
- `depth`: Profundidad actual en el árbol (0 = raíz)
- `limit`: Límite crítico de profundidad

**Returns:**
- `tuple`: `(precio_final: float, nodoCritico: bool)`

**Ejemplos:**
```python
# Profundidad normal
calculate_final_price(100.0, 2, 3)  # depth <= limit
→ (100.0, False)

# Profundidad crítica
calculate_final_price(100.0, 5, 3)  # depth > limit
→ (125.0, True)

# Sin límite
calculate_final_price(100.0, 10, None)
→ (100.0, False)
```

---

### serialize_tree.py (Actualizado)

**Cambios:**
- Importa `calculate_final_price` de price_calculator
- Usa regla exacta: 25% de penalización
- Recalcula precios en cada llamada
- Incluye métricas en la respuesta

**Función Principal:**
```python
def serialize_tree(tree, depth_limit=None) -> dict
```

**Lógica:**
1. Obtiene `depth_limit` de parámetro o `tree.depth_limit`
2. Recorre árbol en postorden
3. Para cada nodo, calcula precio basado en profundidad
4. Retorna árbol serializado con precios recalculados

---

## 📊 Ejemplo Completo

### Árbol Inicial
```
tree.depth_limit = 2

        100 (depth=0)
       /   \
      50    150  (depth=1)
     /        \
    25        175  (depth=2)
   /
  10  (depth=3)
```

### GET /avl/tree (con depth_limit=2)

```json
{
    "root": {
        "value": 100,
        "profundidad": 0,
        "nodoCritico": false,
        "precioBase": 200.0,
        "precioFinal": 200.0,
        "left": {
            "value": 50,
            "profundidad": 1,
            "nodoCritico": false,
            "precioBase": 150.0,
            "precioFinal": 150.0,
            "left": {
                "value": 25,
                "profundidad": 2,
                "nodoCritico": false,
                "precioBase": 100.0,
                "precioFinal": 100.0,
                "left": {
                    "value": 10,
                    "profundidad": 3,
                    "nodoCritico": true,          ← CRÍTICO
                    "precioBase": 80.0,
                    "precioFinal": 100.0           ← 80 * 1.25 = 100
                }
            }
        },
        "right": {
            "value": 150,
            "profundidad": 1,
            "nodoCritico": false,
            "precioBase": 120.0,
            "precioFinal": 120.0,
            "right": {
                "value": 175,
                "profundidad": 2,
                "nodoCritico": false,
                "precioBase": 140.0,
                "precioFinal": 140.0
            }
        }
    },
    "depth_limit": 2,
    "metrics": {
        "total_nodes": 5,
        "height": 4
    }
}
```

### Cambiar depth_limit

```bash
curl -X PUT "http://localhost:8000/avl/depth-limit" \
  -H "Content-Type: application/json" \
  -d '{"limit": 3}'
```

### Resultado: Todos los precios recalculados

```json
{
    "status": "success",
    "message": "Límite de profundidad actualizado a 3",
    "tree": {
        "value": 100,
        "profundidad": 0,
        "nodoCritico": false,
        "precioBase": 200.0,
        "precioFinal": 200.0,
        "left": {
            "value": 50,
            "profundidad": 1,
            "nodoCritico": false,
            "precioFinal": 150.0,
            "left": {
                "value": 25,
                "profundidad": 2,
                "nodoCritico": false,
                "precioFinal": 100.0,
                "left": {
                    "value": 10,
                    "profundidad": 3,
                    "nodoCritico": false,        ← YA NO CRÍTICO
                    "precioFinal": 80.0          ← Precio normal nuevamente (100 * 0.8 = 80)
                }
            }
        }
    }
}
```

---

## 🔐 Validaciones

### Input Validation (PUT /avl/depth-limit)

| Validación | Tipo | Error |
|-----------|------|-------|
| `limit` presente | Required | 400: "'limit' es requerido" |
| `limit` es int | Type | 400: "'limit' debe ser un entero no negativo" |
| `limit` >= 0 | Range | 400: "'limit' debe ser un entero no negativo" |

---

## 📈 Cambios de Comportamiento

### Antes (Incorrecto)
- Penalización: 5% * (depth - limit) por cada nivel
- Penalización progresiva: depth=4, limit=2 → 10% (5% * 2 niveles)
- No recalculaba precios al cambiar depth_limit

### Después (Correcto)
- Penalización: Exactamente 25% si depth > limit
- Penalización binaria: 0% si depth <= limit, 25% si depth > limit
- Recalcula todos los precios cuando cambia depth_limit

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────┐
│  GET /avl/tree                   │
│  PUT /avl/depth-limit (nuevo)   │
├─────────────────────────────────┤
│  avl_routes.py                   │
├─────────────────────────────────┤
│  serialize_tree(tree)            │
├─────────────────────────────────┤
│  calculate_final_price()         │
│  (Nueva función pura)            │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│     AVL Tree Instance            │
│  └─ tree.depth_limit             │
│  └─ tree.rotation_counts         │
└─────────────────────────────────┘
```

---

## 🎓 Principios Implementados

### SRP (Single Responsibility Principle)
- `price_calculator.py`: Solo calcula precios
- `serialize_tree.py`: Solo serializa con precios
- `avl_routes.py`: Solo maneja HTTP

### DRY (Don't Repeat Yourself)
- `calculate_final_price()` es reutilizable
- Un solo lugar de lógica de precios
- Cambios futuros en regla de precio: un solo cambio

### Funciones Puras
- `calculate_final_price()` no tiene efectos secundarios
- Testeable en forma aislada
- Predecible: mismas entradas = mismas salidas

---

## ✅ Validaciones Completadas

✓ Compilación sin errores  
✓ Función `calculate_final_price()` pura  
✓ `serialize_tree()` usa nueva función  
✓ `GET /avl/tree` retorna con precios recalculados  
✓ `PUT /avl/depth-limit` crea y actualiza  
✓ Validaciones de input correctas  
✓ Documentación completa  

---

## 🚀 Próximas Mejoras (Opcional)

- [ ] Histórico de cambios de depth_limit
- [ ] Validación de profundidad máxima del árbol
- [ ] Alert cuando muchos nodos son críticos
- [ ] Reporte de impacto de precio por cambio depth_limit
- [ ] Tests unitarios para calculate_final_price

---

**Última actualización**: 12 de abril de 2026
