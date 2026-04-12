#!/bin/bash

# Ejemplos: Sistema de Precios por Profundidad Crítica
# Ejecutar con: bash depth_limit_examples.sh

API="http://localhost:8000"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     CÁLCULO DE PRECIOS POR PROFUNDIDAD - EJEMPLOS              ║"
echo "╚════════════════════════════════════════════════════════════════╝"

echo ""
echo "📌 CASO 1: Árbol con Profundidad Crítica = 2"
echo "─────────────────────────────────────────────────────────────────"

echo ""
echo "1.1 Insertar nodos"
curl -s -X POST "$API/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{"codigo": 100, "origen": "M", "destino": "B", "horaSalida": "10:00", "precioBase": 200.0, "pasajeros": 100, "prioridad": 1}' > /dev/null
curl -s -X POST "$API/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{"codigo": 50, "origen": "M", "destino": "V", "horaSalida": "08:00", "precioBase": 150.0, "pasajeros": 80, "prioridad": 2}' > /dev/null
curl -s -X POST "$API/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{"codigo": 150, "origen": "B", "destino": "M", "horaSalida": "12:00", "precioBase": 120.0, "pasajeros": 120, "prioridad": 1}' > /dev/null
curl -s -X POST "$API/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{"codigo": 25, "origen": "V", "destino": "B", "horaSalida": "09:00", "precioBase": 100.0, "pasajeros": 60, "prioridad": 3}' > /dev/null
curl -s -X POST "$API/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{"codigo": 10, "origen": "M", "destino": "V", "horaSalida": "07:00", "precioBase": 80.0, "pasajeros": 40, "prioridad": 2}' > /dev/null
echo "✓ 5 vuelos insertados"

echo ""
echo "1.2 Ver árbol con depth_limit = 2 (por defecto)"
echo "   GET /avl/tree"
echo ""
curl -s "$API/avl/tree" | jq '.root | {
  codigo: .codigo,
  profundidad: .profundidad,
  nodoCritico: .nodoCritico,
  precioBase: .precioBase,
  precioFinal: .precioFinal,
  depth_limit: .depth_limit
}'

echo ""
echo "Expected:"
echo "  - Códigos en profundidad 0-2: nodoCritico=false, precioFinal=precioBase"
echo "  - Códigos en profundidad > 2: nodoCritico=true, precioFinal=precioBase*1.25"

echo ""
echo "1.3 Estructura del árbol"
curl -s "$API/avl/tree" | jq '{
  total_nodes: .metrics.total_nodes,
  height: .metrics.height,
  depth_limit: .depth_limit
}'

echo ""
echo ""
echo "📌 CASO 2: Cambiar depth_limit a 1"
echo "─────────────────────────────────────────────────────────────────"

echo ""
echo "2.1 Actualizar limit a 1"
echo "   PUT /avl/depth-limit"
curl -s -X PUT "$API/avl/depth-limit" \
  -H "Content-Type: application/json" \
  -d '{"limit": 1}' | jq '{
  status: .status,
  message: .message,
  new_limit: .depth_limit,
  tree_structure: {
    root_codigo: .tree.codigo,
    root_depth: .tree.profundidad,
    root_critico: .tree.nodoCritico
  }
}'

echo ""
echo "Expected:"
echo "  - Nodos en depth 0-1: nodoCritico=false"
echo "  - Nodos en depth > 1: nodoCritico=true, precio +25%"

echo ""
echo "2.2 Todos los precios se recalcularon"
curl -s "$API/avl/tree" | jq '.depth_limit'

echo ""
echo ""
echo "📌 CASO 3: Cambiar depth_limit a 3"
echo "─────────────────────────────────────────────────────────────────"

echo ""
echo "3.1 Actualizar limit a 3"
echo "   PUT /avl/depth-limit"
curl -s -X PUT "$API/avl/depth-limit" \
  -H "Content-Type: application/json" \
  -d '{"limit": 3}' | jq '{
  status: .status,
  new_limit: .depth_limit,
  total_nodes: .metrics.total_nodes,
  height: .metrics.height
}'

echo ""
echo "Expected:"
echo "  - Nodos en depth 0-3: nodoCritico=false, precio normal"
echo "  - Nodos en depth > 3: nodoCritico=true, precio +25%"

echo ""
echo ""
echo "📌 CASO 4: Comparar Precios Antes/Después"
echo "─────────────────────────────────────────────────────────────────"

echo ""
echo "4.1 Resetear y crear árbol simple"
curl -s -X DELETE "$API/flights/reset" > /dev/null

# Crear árbol degenerado
for i in 100 50 25 10 5; do
  curl -s -X POST "$API/flights/insert" \
    -H "Content-Type: application/json" \
    -d "{\"codigo\": $i, \"origen\": \"M\", \"destino\": \"B\", \"horaSalida\": \"10:00\", \"precioBase\": 100.0, \"pasajeros\": 100, \"prioridad\": 1}" > /dev/null
done
echo "✓ Árbol degenerado creado (profundidad 4)"

echo ""
echo "4.2 Con limit=1 (mayoría de nodos son críticos)"
curl -s -X PUT "$API/avl/depth-limit" \
  -H "Content-Type: application/json" \
  -d '{"limit": 1}' > /dev/null

echo ""
echo "   Precios con limit=1:"
curl -s "$API/avl/tree" | jq '.root | recurse(.left, .right) | 
  select(.codigo != null) | 
  {codigo: .codigo, depth: .profundidad, base: .precioBase, final: .precioFinal, critico: .nodoCritico}'

echo ""
echo "4.3 Con limit=4 (minoría o ningún nodo es crítico)"
curl -s -X PUT "$API/avl/depth-limit" \
  -H "Content-Type: application/json" \
  -d '{"limit": 4}' > /dev/null

echo ""
echo "   Precios con limit=4:"
curl -s "$API/avl/tree" | jq '.root | recurse(.left, .right) | 
  select(.codigo != null) | 
  {codigo: .codigo, depth: .profundidad, base: .precioBase, final: .precioFinal, critico: .nodoCritico}'

echo ""
echo ""
echo "📌 CASO 5: Validación de Errores"
echo "─────────────────────────────────────────────────────────────────"

echo ""
echo "5.1 Intento: limit no incluido"
echo "   PUT /avl/depth-limit (sin 'limit')"
curl -s -X PUT "$API/avl/depth-limit" \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.'

echo ""
echo "5.2 Intento: limit negativo"
echo "   PUT /avl/depth-limit {'limit': -1}"
curl -s -X PUT "$API/avl/depth-limit" \
  -H "Content-Type: application/json" \
  -d '{"limit": -1}' | jq '.'

echo ""
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              ✅ EJEMPLOS COMPLETADOS EXITOSAMENTE             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
