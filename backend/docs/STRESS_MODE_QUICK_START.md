# Modo Estrés - Quick Start

## 🚀 Inicio Rápido

### Activar Stress Mode (BST)
```bash
curl -X POST "http://localhost:8000/avl/stress-mode/enable"
```

### Desactivar Stress Mode (AVL)
```bash
curl -X POST "http://localhost:8000/avl/stress-mode/disable"
```

### Rebalancear Árbol
```bash
curl -X POST "http://localhost:8000/avl/rebalance"
```

### Auditar Integridad (Solo en Stress Mode)
```bash
curl "http://localhost:8000/avl/audit"
```

---

## 📊 Caso de Uso: Comparar AVL vs BST

```bash
#!/bin/bash

API="http://localhost:8000"

# 1️⃣ Estado AVL (Balanceado automáticamente)
echo "1. Insertar en AVL (con balanceo automático)"
for i in 100 50 150 25 75 125 175; do
  curl -X POST "$API/flights/insert" \
    -H "Content-Type: application/json" \
    -d "{\"codigo\": $i, \"origen\": \"M\", \"destino\": \"B\", \"horaSalida\": \"10:00\", \"precioBase\": 100, \"pasajeros\": 100, \"prioridad\": 1}" > /dev/null
done

# Guardar métricas AVL
curl "$API/flights/metrics" | jq '.metrics.height' > /tmp/avl_height.txt

# 2️⃣ Cambiar a BST (Sin balanceo)
echo "2. Activar stress_mode (BST)"
curl -X POST "$API/avl/stress-mode/enable" > /dev/null

# Vaciar árbol
curl -X DELETE "$API/flights/reset" > /dev/null

# 3️⃣ Insertar mismos datos en BST
echo "3. Insertar mismos datos en BST (sin balanceo)"
for i in 100 50 150 25 75 125 175; do
  curl -X POST "$API/flights/insert" \
    -H "Content-Type: application/json" \
    -d "{\"codigo\": $i, \"origen\": \"M\", \"destino\": \"B\", \"horaSalida\": \"10:00\", \"precioBase\": 100, \"pasajeros\": 100, \"prioridad\": 1}" > /dev/null
done

# Guardar métricas BST
curl "$API/flights/metrics" | jq '.metrics.height' > /tmp/bst_height.txt

# 4️⃣ Comparar
echo ""
echo "═══════════════════════════════════"
echo "Comparación AVL vs BST:"
echo "═══════════════════════════════════"
echo "AVL Height: $(cat /tmp/avl_height.txt)"
echo "BST Height: $(cat /tmp/bst_height.txt)"

# 5️⃣ Rebalancear BST de vuelta a AVL
echo ""
echo "Rebalanceando BST..."
curl -X POST "$API/avl/stress-mode/disable" > /dev/null
curl -X POST "$API/avl/rebalance" | jq '.rotation_counts'
curl "$API/flights/metrics" | jq '.metrics.height' > /tmp/avl_height_after.txt

echo "AVL Height después: $(cat /tmp/avl_height_after.txt)"
```

---

## 🔍 Auditar en Stress Mode

```bash
# Activar para auditar
curl -X POST "http://localhost:8000/avl/stress-mode/enable"

# Insertar datos (sin balanceo)
curl -X POST "http://localhost:8000/flights/insert" -H "Content-Type: application/json" -d '{"codigo": 100, ...}'

# Auditar
curl "http://localhost:8000/avl/audit" | jq '.'

# Esperar respuesta:
# {
#   "status": "success",
#   "valid": true/false,
#   "nodes_checked": 7,
#   "inconsistent_nodes": [...]
# }
```

---

## ⚠️ Errores Comunes

### Error: "No se puede rebalancear en stress_mode"
```
Solución: POST /avl/stress-mode/disable primero
```

### Error: "Este endpoint solo está disponible en stress_mode"
```
Solución: POST /avl/stress-mode/enable primero
```

---

## 📚 Documentación Completa

Ver archivos:
- `STRESS_MODE.md` - Documentación detallada
- `stress_mode_examples.sh` - Ejemplos ejecutables
- `STRESS_MODE_SUMMARY.md` - Resumen técnico
