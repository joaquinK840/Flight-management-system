# Endpoint POST /avl/load-file

## Descripción
Carga árboles AVL y BST desde archivos JSON. Soporta dos modos de carga distintos.

## Uso

### Modo 1: Topología (Reconstrucción exacta)
Carga el árbol respetando exactamente la estructura especificada en el JSON sin aplicar balanceo.

**Formato JSON:**
```json
{
  "type": "topology",
  "root": {
    "codigo": 100,
    "origen": "Madrid",
    "destino": "Barcelona",
    "horaSalida": "10:30",
    "precioBase": 150.00,
    "precioFinal": 150.00,
    "pasajeros": 180,
    "promocion": false,
    "alerta": "normal",
    "prioridad": 1,
    "left": { /* nodo izquierdo */ },
    "right": { /* nodo derecho */ }
  }
}
```

**Características:**
- NO se aplica balanceo
- Se recalculan alturas correctamente
- Mismo árbol en AVL y BST

---

### Modo 2: Inserción (Comparación AVL vs BST)
Inserta vuelos uno a uno. El AVL se balancea automáticamente, el BST queda sin balancear.

**Formato JSON:**
```json
{
  "type": "insertion",
  "flights": [
    {
      "codigo": 100,
      "origen": "Madrid",
      "destino": "Barcelona",
      "horaSalida": "10:30",
      "precioBase": 150.00,
      "precioFinal": 150.00,
      "pasajeros": 180,
      "promocion": false,
      "alerta": "normal",
      "prioridad": 1
    },
    { /* más vuelos */ }
  ]
}
```

**Características:**
- AVL: Inserte y balancee automáticamente → altura optimizada
- BST: Inserte sin balanceo → posible altura subóptima
- Mismo conjunto de vuelos en ambos árboles
- Permite comparar eficiencia de balanceo

---

## Respuesta

### Status 200 (Éxito)
```json
{
  "status": "success",
  "load_type": "insertion",
  "avl": {
    "tree": { /* árbol serializado */ },
    "metrics": {
      "height": 4,
      "leaves": 3,
      "total_nodes": 9,
      "rotations": {"LL": 1, "RR": 0, "LR": 1, "RL": 0},
      "total_rotations": 2
    }
  },
  "bst": {
    "tree": { /* árbol serializado */ },
    "metrics": {
      "height": 6,
      "leaves": 2,
      "total_nodes": 9
    }
  },
  "comparison": {
    "avl_height": 4,
    "bst_height": 6,
    "avl_rotations": 2,
    "avl_optimized": true
  }
}
```

### Status 400 (Error de validación)
```json
{
  "detail": "Error en JSON: Modo topology requiere un campo 'root'"
}
```

### Status 500 (Error interno del servidor)
```json
{
  "detail": "Error procesando archivo: ..."
}
```

---

## Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `"type" inválido` | Usar value distinto a "topology" o "insertion" | Usar "topology" o "insertion" |
| `Campo 'root' faltante` | Modo topology sin raíz | Agregar campo "root" |
| `Campo 'flights' faltante` | Modo insertion sin vuelos | Agregar array "flights" |
| `JSON inválido` | Sintaxis JSON incorrecta | Validar JSON (usar jsonlint.com) |
| `"codigo" faltante` | Vuelo sin identificador | Cada nodo necesita "codigo" |

---

## Ejemplos de Archivos

### TopologiaEjemplo.json
Archivo con estructura de árbol predefinida para modo topología.

### InsercionEjemplo.json
Archivo con lista de vuelos para modo inserción.

---

## Notas Importantes

1. **Single Responsibility**: BST no tiene rotaciones, solo gestiona estructura.
2. **OCP (Open for Extension)**: Fácil agregar nuevas estrategias de balanceo.
3. **stress_mode**: Si está activo, el AVL no aplica rotaciones (solo se actualizan alturas).
4. **Alturas**: Se calculan automáticamente después de cualquier inserción/rotación.
5. **Comparación**: Es útil para visualizar el impacto del balanceo AVL.
