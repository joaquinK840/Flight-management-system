# Modo Estrés (Stress Mode) - Documentación Completa

**Fecha**: 12 de abril de 2026  
**Versión**: 1.0  
**Estado**: ✅ IMPLEMENTADO

---

## 📋 Resumen

El **Modo Estrés** permite cambiar el comportamiento del árbol AVL para análisis comparativos:

- **Deshabilitado (Default)**: Árbol AVL con balanceo automático en cada inserción/eliminación
- **Habilitado**: Árbol se convierte en BST (Binary Search Tree) sin balanceo automático

---

## 🎯 Casos de Uso

### Caso 1: Comparar Eficiencia (AVL vs BST)
```bash
# 1. Insertar datos en modo normal (AVL)
POST /flights/insert {"codigo": 100, ...}
POST /flights/insert {"codigo": 50, ...}
POST /flights/insert {"codigo": 150, ...}

# 2. Guardar métricas del AVL
GET /flights/metrics/tree
# Resultado: altura 2, 2 rotaciones

# 3. Cambiar a BST
POST /avl/stress-mode/enable

# 4. La estructura se mantiene, pero siguientes operaciones NO rotarán
POST /flights/insert {"codigo": 25, ...}

# 5. Comparar: BST altura vs AVL altura

# 6. Restaurar AVL
POST /avl/stress-mode/disable
POST /avl/rebalance
```

### Caso 2: Auditoría de Integridad
```bash
# Insertar datos en stress_mode
POST /avl/stress-mode/enable
POST /flights/insert {"codigo": 100, ...}
POST /flights/insert {"codigo": 50, ...}
... (muchas operaciones)

# Verificar integridad
GET /avl/audit
# Retorna: valid=true, nodes_checked=1000, ...
```

### Caso 3: Rebalanceo Controlado
```bash
# Recopilar datos en stress_mode
POST /avl/stress-mode/enable
POST /flights/insert {"codigo": 100, ...}  # No rota
POST /flights/insert {"codigo": 50, ...}   # No rota
POST /flights/insert {"codigo": 25, ...}   # No rota
# Resultado: BST degenerado (como lista)

# Decidir rebalancear al final
POST /avl/stress-mode/disable
POST /avl/rebalance
# Resultado: Árbol rebalanceado con altura óptima
```

---

## 🔌 Endpoints

### 1. Habilitar Modo Estrés

```http
POST /avl/stress-mode/enable
```

**Descripción:**
- Activa stress_mode
- El árbol cambia de AVL a BST
- Las inserciones/eliminaciones no harán rotaciones automáticas
- Respeta `check_balance()` que solo actualiza alturas

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Modo estrés activado",
    "stress_mode": true,
    "tree_info": {
        "total_nodes": 7,
        "total_leaves": 3,
        "height": 4,
        "rotation_counts": {
            "LL": 2,
            "RR": 0,
            "LR": 1,
            "RL": 0
        },
        "total_rotations": 3
    }
}
```

---

### 2. Deshabilitar Modo Estrés

```http
POST /avl/stress-mode/disable
```

**Descripción:**
- Desactiva stress_mode
- El árbol vuelve a usar AVL
- NO hace rebalanceo automático aquí
- Usuario debe llamar explícitamente a `POST /avl/rebalance` si necesita

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Modo estrés desactivado. Llama a POST /avl/rebalance si necesitas rebalancear",
    "stress_mode": false
}
```

---

### 3. Rebalancear Árbol

```http
POST /avl/rebalance
```

**Descripción:**
- Rebalancea el árbol completo
- Solo disponible cuando `stress_mode == false`
- Recorre en **postorden** (hojas primero)
- Para cada nodo desbalanceado (|factor| > 1), aplica rotación
- Registra rotaciones en `tree.rotation_counts`

**Validaciones:**
- Si `stress_mode == true`: HTTP 400
  ```json
  {
      "detail": "No se puede rebalancear en stress_mode. Primero llama a POST /avl/stress-mode/disable"
  }
  ```

**Response (200 OK):**
```json
{
    "status": "success",
    "total_rotations": 5,
    "rotation_counts": {
        "LL": 2,
        "RR": 1,
        "LR": 1,
        "RL": 1
    },
    "nodes_rebalanced": 4,
    "imbalanced_before": [
        {
            "codigo": 100,
            "balance_factor": 2,
            "height": 3
        },
        {
            "codigo": 50,
            "balance_factor": -2,
            "height": 2
        }
    ],
    "current_tree_metrics": {
        "height": 3,
        "total_nodes": 7
    }
}
```

**Postorden (Recorrido):**
```
        100
       /   \
      50   150
     / \   /  \
    25 75 125 175

Postorden: 25 → 75 → 50 → 125 → 175 → 150 → 100
(Las hojas primero, luego sus padres, subiendo hasta raíz)
```

---

### 4. Auditar Integridad del Árbol

```http
GET /avl/audit
```

**Descripción:**
- Verifica integridad del árbol
- Únicamente disponible cuando `stress_mode == true`
- Usa **Dependency Injection** de FastAPI para verificación

**Verificaciones:**
1. Factor de balance ∈ {-1, 0, 1} para cada nodo
2. Altura correcta: `altura = 1 + max(left_h, right_h)`
3. Estructura general del árbol

**Validaciones:**
- Si `stress_mode == false`: HTTP 403
  ```json
  {
      "detail": "Este endpoint solo está disponible cuando stress_mode está habilitado (POST /avl/stress-mode/enable)"
  }
  ```

**Response (200 OK) - Árbol Válido:**
```json
{
    "status": "success",
    "valid": true,
    "nodes_checked": 15,
    "inconsistent_nodes": []
}
```

**Response (200 OK) - Árbol Invalido:**
```json
{
    "status": "success",
    "valid": false,
    "nodes_checked": 15,
    "inconsistent_nodes": [
        {
            "codigo": 50,
            "balance_factor": 2,
            "expected_balance": false,
            "expected_height": 3,
            "actual_height": 4
        },
        {
            "codigo": 100,
            "balance_factor": -3,
            "expected_balance": false,
            "expected_height": 5,
            "actual_height": 5
        }
    ]
}
```

---

## 🔐 Dependency Injection (DI / ISP)

El endpoint `GET /avl/audit` utiliza **Dependency Injection** de FastAPI:

```python
def verify_stress_mode_enabled():
    """Dependency: Verifica que stress_mode esté habilitado."""
    if not avl.stress_mode:
        raise HTTPException(status_code=403, detail="...")
    return True

@router.get("/audit", dependencies=[Depends(verify_stress_mode_enabled)])
def audit_tree_integrity():
    ...
```

**Ventajas:**
- ✅ Separación de responsabilidades (ISP)
- ✅ Reutilizable para otros endpoints
- ✅ Validación declarativa
- ✅ Documentación automática en Swagger

---

## 📊 Flujo Completo

```
┌─────────────────────────────────────────────────────────┐
│ 1. Estado Inicial (AVL Balanceado)                      │
│    Inserción automática + rotación = O(log n)          │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
        POST /avl/stress-mode/enable
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Modo Estrés Activo (BST Sin Balanceo)               │
│    Inserción SIN rotación = sin garantía de O(log n)   │
│    HEIGHT puede crecer (peor caso O(n))                │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
        POST /avl/stress-mode/disable
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Modo Estrés Deshabilitado (Listo para Rebalance)    │
│    Árbol probablemente desbalanceado                    │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
        POST /avl/rebalance
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Árbol Rebalanceado (AVL Óptimo)                     │
│    HEIGHT mínimo alcanzado                             │
│    Rotaciones registradas en tree.rotation_counts      │
└─────────────────────────────────────────────────────────┘
```

---

## 🧪 Ejemplo Con Curl

### Script Completo

```bash
#!/bin/bash

API="http://localhost:8000"

echo "=== 1. Insertar datos en AVL normal ==="
curl -X POST "$API/flights/insert" -d '{"codigo": 100, "origen": "Madrid", "destino": "Barcelona", "horaSalida": "10:00", "precioBase": 100.0, "pasajeros": 100, "prioridad": 1}' -H "Content-Type: application/json"

echo -e "\n=== 2. Habilitar stress_mode ==="
curl -X POST "$API/avl/stress-mode/enable" -H "Content-Type: application/json"

echo -e "\n=== 3. Insertar m\u00e1s datos (sin rotaci\u00f3n) ==="
curl -X POST "$API/flights/insert" -d '{"codigo": 50, "origen": "Madrid", "destino": "Valencia", "horaSalida": "08:00", "precioBase": 80.0, "pasajeros": 80, "prioridad": 2}' -H "Content-Type: application/json"

echo -e "\n=== 4. Auditar integridad ==="
curl "$API/avl/audit"

echo -e "\n=== 5. Deshabilitar stress_mode ==="
curl -X POST "$API/avl/stress-mode/disable" -H "Content-Type: application/json"

echo -e "\n=== 6. Rebalancear \u00e1rbol ==="
curl -X POST "$API/avl/rebalance" -H "Content-Type: application/json"

echo -e "\n=== 7. Ver m\u00e9tricas finales ==="
curl "$API/flights/metrics"

echo -e "\n=== 8. Intentar auditar fuera de stress_mode (debe fallar) ==="
curl "$API/avl/audit"
```

---

## 📈 Métricas Importantes

### Rotaciones Registradas

Después de `POST /avl/rebalance`:

```json
{
    "rotation_counts": {
        "LL": 2,    // LL rotations applied
        "RR": 1,    // RR rotations applied
        "LR": 1,    // LR rotations applied
        "RL": 0     // RL rotations applied
    },
    "total_rotations": 4
}
```

### Nodos Desbalanceados Encontrados

```json
{
    "imbalanced_before": [
        {
            "codigo": 50,
            "balance_factor": 2,   // left-heavy
            "height": 3
        },
        {
            "codigo": 100,
            "balance_factor": -3,  // right-heavy (peor)
            "height": 4
        }
    ],
    "nodes_rebalanced": 2
}
```

---

## 🚨 Códigos de Error

| Status | Error | Significado |
|--------|-------|-------------|
| **200** | ✅ OK | Operación exitosa |
| **400** | Can't rebalance in stress_mode | Intentó rebalancear con stress_mode=true |
| **403** | Audit only in stress_mode | Intentó auditar con stress_mode=false |
| **500** | Internal Server Error | Error inesperado |

---

## 🔄 Algoritmo de Rebalanceo (Postorden)

```python
def rebalance_postorder(node):
    if node is None:
        return
    
    # 1. Procesar subárbol izquierdo (POSTORDEN)
    rebalance_postorder(node.left)
    
    # 2. Procesar subárbol derecho (POSTORDEN)
    rebalance_postorder(node.right)
    
    # 3. Procesar nodo actual
    actualizar_altura(node)
    bf = factor_balance(node)
    
    if |bf| > 1:
        # Aplicar rotación necesaria
        registrar_rotación(bf)
        aplicar_rotación(node)
        actualizar_altura(node)
```

**Complejidad:**
- **Tiempo**: O(n) - todos los nodos se visitan
- **Espacio**: O(h) - altura de la pila de recursión

---

## 📚 Principios Aplicados

### ISP (Interface Segregation Principle)
- Cada endpoint tiene una responsabilidad clara
- Dependency Injection para checks de autorización

### Single Responsibility
- `enable_stress_mode()`: Activa stress_mode
- `disable_stress_mode()`: Desactiva stress_mode
- `rebalance_tree()`: Rebalancea
- `audit_tree_integrity()`: Audita

### Liskov Substitution Principle
- En stress_mode, el árbol sigue siendo AVL en estructura
- Solo cambia su comportamiento (no es un subtipo diferente)

---

## ✅ Validaciones Completadas

✓ Compilación sin errores  
✓ Todos los endpoints definidos  
✓ Dependency Injection implementada  
✓ Recorrido postorden verificado  
✓ Rotaciones registradas correctamente  
✓ Auditoría implementada  

---

## 🎯 Conclusión

El Modo Estrés permite:

1. **Análisis Comparativos**: AVL vs BST
2. **Auditoría de Integridad**: Verificar árbol en stress_mode
3. **Rebalanceo Controlado**: Decidir cuándo aplicar rotaciones
4. **Testing**: Simular inserción sin balanceo

**Status**: 🟢 **PRODUCTION READY**

---

**Última actualización**: 12 de abril de 2026
