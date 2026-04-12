#!/bin/bash

# Ejemplos de Modo Estrés (Stress Mode)
# Ejecutar comandos individuales o toda la secuencia

API="http://localhost:8000"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           MODO ESTRÉS - EJEMPLOS DE USO CON CURL              ║"
echo "╚════════════════════════════════════════════════════════════════╝"

echo ""
echo "📌 CASO 1: Comparar AVL vs BST"
echo "─────────────────────────────────────────────────────────────────"

echo ""
echo "1.1 Insertar datos en AVL normal (con balanceo)"
echo "   POST /flights/insert"
curl -X POST "$API/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": 100,
    "origen": "Madrid",
    "destino": "Barcelona",
    "horaSalida": "10:00",
    "precioBase": 150.0,
    "pasajeros": 180,
    "prioridad": 1
  }' | jq '.'

echo ""
echo "1.2 Insertar más datos (AVL se balancea automáticamente)"
echo "   POST /flights/insert (x3)"
for codigo in 50 150 75; do
  curl -X POST "$API/flights/insert" \
    -H "Content-Type: application/json" \
    -d "{
      \"codigo\": $codigo,
      \"origen\": \"Madrid\",
      \"destino\": \"City$codigo\",
      \"horaSalida\": \"10:00\",
      \"precioBase\": 100.0,
      \"pasajeros\": 100,
      \"prioridad\": 1
    }" > /dev/null
  echo "  ✓ Insertado código $codigo"
done

echo ""
echo "1.3 Ver métricas del AVL (altura, rotaciones)"
echo "   GET /flights/metrics"
curl "$API/flights/metrics" | jq '.metrics | {height, total_nodes, total_leaves, rotation_counts}'

echo ""
echo "1.4 Habilitar Modo Estrés"
echo "   POST /avl/stress-mode/enable"
curl -X POST "$API/avl/stress-mode/enable" -H "Content-Type: application/json" | jq '.'

echo ""
echo "1.5 Insertar datos en stress_mode (BST SIN balanceo)"
echo "   POST /flights/insert (x3, sin rotación)"
for codigo in 25 35 60; do
  curl -X POST "$API/flights/insert" \
    -H "Content-Type: application/json" \
    -d "{
      \"codigo\": $codigo,
      \"origen\": \"Barcelona\",
      \"destino\": \"City$codigo\",
      \"horaSalida\": \"11:00\",
      \"precioBase\": 90.0,
      \"pasajeros\": 90,
      \"prioridad\": 2
    }" > /dev/null
  echo "  ✓ Insertado código $codigo (sin rotación)"
done

echo ""
echo "1.6 Ver métricas en stress_mode (altura puede ser > altura AVL)"
echo "   GET /flights/metrics"
curl "$API/flights/metrics" | jq '.metrics | {height, total_nodes, total_leaves, rotation_counts}'

echo ""
echo "1.7 Auditar integridad del árbol (disponible SOLO en stress_mode)"
echo "   GET /avl/audit"
curl "$API/avl/audit" | jq '.'

echo ""
echo ""
echo "📌 CASO 2: Rebalanceo Controlado"
echo "─────────────────────────────────────────────────────────────────"

echo ""
echo "2.1 Deshabilitar stress_mode"
echo "   POST /avl/stress-mode/disable"
curl -X POST "$API/avl/stress-mode/disable" -H "Content-Type: application/json" | jq '.'

echo ""
echo "2.2 Rebalancear el árbol (recorrido postorden)"
echo "   POST /avl/rebalance"
curl -X POST "$API/avl/rebalance" -H "Content-Type: application/json" | jq '.'

echo ""
echo "2.3 Ver métricas después del rebalanceo"
echo "   GET /flights/metrics"
curl "$API/flights/metrics" | jq '.metrics | {height, total_nodes, total_leaves, rotation_counts}'

echo ""
echo ""
echo "📌 CASO 3: Auditoría (Integridad)"
echo "─────────────────────────────────────────────────────────────────"

echo ""
echo "3.1 Intentar auditar fuera de stress_mode (debe fallar con 403)"
echo "   GET /avl/audit (con stress_mode = false)"
echo "   Resultado esperado: HTTP 403 Forbidden"
curl -i "$API/avl/audit" 2>/dev/null | head -n 1

echo ""
echo "3.2 Habilitar stress_mode de nuevo"
echo "   POST /avl/stress-mode/enable"
curl -X POST "$API/avl/stress-mode/enable" -H "Content-Type: application/json" > /dev/null
echo "  ✓ stress_mode habilitado"

echo ""
echo "3.3 Auditar con stress_mode = true (debe funcionar)"
echo "   GET /avl/audit"
curl "$API/avl/audit" | jq '.'

echo ""
echo ""
echo "📌 RESUMEN DE ENDPOINTS"
echo "─────────────────────────────────────────────────────────────────"
echo ""
echo "POST /avl/stress-mode/enable    → Activar stress_mode (BST)"
echo "POST /avl/stress-mode/disable   → Desactivar stress_mode (AVL)"
echo "POST /avl/rebalance             → Rebalancear árbol completo"
echo "GET  /avl/audit                 → Auditar integridad (SOLO en stress_mode)"
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              ✅ EJEMPLOS COMPLETADOS EXITOSAMENTE             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
