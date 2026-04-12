# Endpoints de Versionado (Versions)

## Descripción General

El sistema de versionado permite guardar, restaurar y gestionar diferentes estados del árbol AVL.

**Punto clave**: Se guarda la **estructura jerárquica completa** del árbol (no solo la lista de vuelos), preservando:
- Topología (relaciones padre-hijo)
- Valores y datos de cada nodo
- Alturas calculadas
- Factores de balance

Esto permite restaurar un árbol funcionalmente equivalente al original.

---

## Estructura de una Versión Guardada

```json
{
  "name": "Simulacion Alta Demanda",
  "timestamp": "2026-04-12 10:30:45",
  "metrics": {
    "height": 4,
    "total_nodes": 7,
    "total_leaves": 3,
    "total_rotations": 2,
    "rotation_counts": {
      "LL": 1,
      "RR": 0,
      "LR": 1,
      "RL": 0
    }
  },
  "tree_data": {
    "value": 100,
    "height": 4,
    "datos": { /* datos del vuelo */ },
    "left": { /* subárbol */ },
    "right": { /* subárbol */ }
  }
}
```

---

## Endpoints

### 1. POST /versions/save
**Guarda el estado actual del árbol.**

```bash
curl -X POST "http://localhost:8000/versions/save" \
  -H "Content-Type: application/json" \
  -d '{"name": "Simulacion Alta Demanda"}'
```

**Respuesta (200):**
```json
{
  "status": "success",
  "message": "Versión 'Simulacion Alta Demanda' guardada",
  "timestamp": "2026-04-12 10:30:45",
  "versions_count": 1,
  "available_versions": ["Simulacion Alta Demanda"]
}
```

**Errores:**
- 400: Nombre vacío o versión ya existe
- 500: Error interno

---

### 2. GET /versions/list
**Lista todas las versiones guardadas.**

```bash
curl "http://localhost:8000/versions/list"
```

**Respuesta (200):**
```json
{
  "status": "success",
  "total_versions": 2,
  "versions": [
    {
      "name": "Simulacion Alta Demanda",
      "timestamp": "2026-04-12 10:30:45",
      "metrics": {
        "height": 4,
        "total_nodes": 7,
        "total_leaves": 3
      },
      "tree_type": "AVL",
      "has_data": true
    },
    {
      "name": "Estado Inicial",
      "timestamp": "2026-04-12 10:00:00",
      "metrics": {
        "height": 2,
        "total_nodes": 3,
        "total_leaves": 2
      },
      "tree_type": "AVL",
      "has_data": true
    }
  ]
}
```

---

### 3. POST /versions/restore/{name}
**Restaura el árbol desde una versión guardada.**

Reconstruye exactamente la topología original con las mismas alturas.

```bash
curl -X POST "http://localhost:8000/versions/restore/Simulacion%20Alta%20Demanda"
```

**Respuesta (200):**
```json
{
  "status": "success",
  "message": "Versión 'Simulacion Alta Demanda' restaurada",
  "restored_from": "2026-04-12 10:30:45",
  "metrics": {
    "height": 4,
    "total_nodes": 7,
    "total_leaves": 3,
    "total_rotations": 2
  },
  "tree": {
    "value": 100,
    "codigo": 100,
    "height": 4,
    "datos": { /* datos */ },
    "left": { /* subárbol */ },
    "right": { /* subárbol */ }
  }
}
```

**Errores:**
- 404: Versión no existe

---

### 4. DELETE /versions/{name}
**Elimina una versión guardada.**

```bash
curl -X DELETE "http://localhost:8000/versions/Simulacion%20Alta%20Demanda"
```

**Respuesta (200):**
```json
{
  "status": "success",
  "message": "Versión 'Simulacion Alta Demanda' eliminada",
  "versions_remaining": 1,
  "available_versions": ["Estado Inicial"]
}
```

**Errores:**
- 404: Versión no existe

---

## Endpoints Adicionales

### GET /versions/{name}/info
**Obtiene información detallada de una versión.**

```bash
curl "http://localhost:8000/versions/Estado%20Inicial/info"
```

**Respuesta:**
```json
{
  "status": "success",
  "version": {
    "name": "Estado Inicial",
    "timestamp": "2026-04-12 10:00:00",
    "metrics": { /* métricas */ },
    "tree_type": "AVL",
    "has_data": true
  }
}
```

---

### POST /versions/{name}/overwrite
**Sobrescribe una versión existente con el árbol actual.**

Útil para actualizar un checkpoint sin crear una nueva versión.

```bash
curl -X POST "http://localhost:8000/versions/Estado%20Inicial/overwrite"
```

**Respuesta:**
```json
{
  "status": "success",
  "message": "Versión 'Estado Inicial' actualizada",
  "new_timestamp": "2026-04-12 11:00:00"
}
```

---

### POST /versions/compare/{version1}/vs/{version2}
**Compara dos versiones.**

Muestra las diferencias en métricas entre dos versiones.

```bash
curl -X POST "http://localhost:8000/versions/compare/Estado%20Inicial/vs/Simulacion%20Alta%20Demanda"
```

**Respuesta:**
```json
{
  "status": "success",
  "comparison": {
    "version1": "Estado Inicial",
    "version2": "Simulacion Alta Demanda",
    "comparison": {
      "height_diff": 2,
      "nodes_diff": 4,
      "leaves_diff": 1,
      "rotations_diff": 2
    }
  }
}
```

**Interpretación:**
- `height_diff: 2` - V2 es 2 leveles más profunda
- `nodes_diff: 4` - V2 tiene 4 nodos más
- `leaves_diff: 1` - V2 tiene 1 hoja más
- `rotations_diff: 2` - Se realizaron 2 más rotaciones en V2

---

### DELETE /versions/clear/all
**Elimina TODAS las versiones guardadas.**

⚠️ **OPERACIÓN IRREVERSIBLE**

```bash
curl -X DELETE "http://localhost:8000/versions/clear/all"
```

**Respuesta:**
```json
{
  "status": "success",
  "message": "Se eliminaron 5 versiones",
  "versions_remaining": 0
}
```

---

### GET /versions/{name}/export
**Exporta una versión completa como JSON.**

Útil para compartir o guardar en archivo.

```bash
curl "http://localhost:8000/versions/Simulacion%20Alta%20Demanda/export"
```

**Respuesta:**
```json
{
  "status": "success",
  "version_name": "Simulacion Alta Demanda",
  "json": {
    "name": "Simulacion Alta Demanda",
    "timestamp": "2026-04-12 10:30:45",
    "metrics": { /* métricas */ },
    "tree_data": { /* árbol completo */ }
  }
}
```

---

### POST /versions/duplicate/{source_name}/{dest_name}
**Crea una copia de una versión con nuevo nombre.**

```bash
curl -X POST "http://localhost:8000/versions/duplicate/Estado%20Inicial/Copia%20Backup"
```

**Respuesta:**
```json
{
  "status": "success",
  "message": "Versión 'Estado Inicial' copiada como 'Copia Backup'",
  "versions_count": 2,
  "available_versions": ["Estado Inicial", "Copia Backup"]
}
```

---

## Casos de Uso

### 1. Guardar Snapshot Antes de Cambios Importantes

```bash
# Guardar estado actual
curl -X POST "http://localhost:8000/versions/save" \
  -d '{"name": "Antes de Actualizacion Masiva"}'

# Realizar cambios...
curl -X POST "http://localhost:8000/flights/insert" -d '{...}'
curl -X POST "http://localhost:8000/flights/insert" -d '{...}'

# Si algo sale mal, restaurar
curl -X POST "http://localhost:8000/versions/restore/Antes%20de%20Actualizacion%20Masiva"
```

---

### 2. Comparar Eficiencia de Algoritmos

```bash
# Modo AVL
curl -X POST "http://localhost:8000/flights/stress-mode/false"
curl -X POST "http://localhost:8000/versions/save" -d '{"name": "Con Balanceo AVL"}'

# Modo Stress (sin balanceo)
curl -X POST "http://localhost:8000/flights/stress-mode/true"
curl -X POST "http://localhost:8000/versions/save" -d '{"name": "Sin Balanceo"}'

# Comparar
curl -X POST "http://localhost:8000/versions/compare/Con%20Balanceo%20AVL/vs/Sin%20Balanceo"
```

**Resultado esperado:**
- Con balanceo: altura ~log n
- Sin balanceo: altura puede ser O(n)

---

### 3. Auditoría de Cambios

```bash
# Listar todas las versiones
curl "http://localhost:8000/versions/list"

# Ver información de una versión específica
curl "http://localhost:8000/versions/Simulacion%20Alta%20Demanda/info"

# Exportar para análisis externo
curl "http://localhost:8000/versions/Simulacion%20Alta%20Demanda/export" > version.json
```

---

## Restricciones y Ventajas

### ✅ Ventajas de Esta Implementación

1. **Estructura Real**: Guarda la topología completa del árbol, no solo datos
2. **Restauración Exacta**: El árbol restaurado es funcionalmente equivalente
3. **Métricas Preservadas**: Alturas, factores de balance, rotaciones
4. **Sin Pérdida**: Todos los datos de vuelo se preservan
5. **Comparación**: Permite análisis de cambios entre versiones

### ⚠️ Restricciones

1. **No es Lista de Vuelos**: Si intentaras guardar solo `{"vuelos": [...]}`, no podrías reconstruir el árbol con las mismas alturas
2. **Topología Importa**: El orden de inserción no se guarda, solo la estructura final
3. **Espacio**: Guarda la estructura completa (más que solo la lista)

### 🏛️ Principio LSP (Liskov Substitution)

Las versiones guardadas son **funcionalmente equivalentes** al original:
- Búsqueda opera igual
- Balanceo está preservado
- Métrica de profundidad es idéntica

---

## Modelo de Datos: Nodo Serializado

```json
{
  "value": 100,
  "height": 4,
  "datos": {
    "codigo": 100,
    "origen": "Madrid",
    "destino": "Barcelona",
    "horaSalida": "10:30",
    "precioBase": 150.0,
    "precioFinal": 150.0,
    "pasajeros": 180,
    "promocion": false,
    "alerta": "normal",
    "prioridad": 1
  },
  "left": {
    "value": 50,
    "height": 2,
    "datos": { /* ... */ },
    "left": null,
    "right": null
  },
  "right": {
    "value": 150,
    "height": 3,
    "datos": { /* ... */ },
    "left": null,
    "right": null
  }
}
```

---

## Códigos de Error

| Código | Mensaje | Causa |
|--------|---------|-------|
| 400 | `"El nombre de la versión no puede estar vacío"` | Nombre vacío |
| 400 | `"La versión '{name}' ya existe"` | Intento de duplicar nombre |
| 404 | `"La versión '{name}' no existe"` | Versión no encontrada |
| 500 | `"Error interno del servidor"` | Error inesperado |

---

## Tips Pro

1. **Backup Automático**: Guarda versión antes de cada operación crítica
2. **Comparación**: Usa compare para medir impacto de cambios
3. **Exportar**: Usa export para análisis externo con Python, Excel, etc.
4. **Duplicar**: Crea copia para hacer experimentos sin perder original
5. **Auditoría**: Usa list y info para rastrear cambios en el tiempo

---

**Última actualización**: 12 de abril de 2026
