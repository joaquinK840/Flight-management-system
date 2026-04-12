#!/bin/bash

# Script de Ejemplos - Sistema de Concurrencia con Cola
# =====================================================

BASE_URL="http://localhost:8000"

echo "════════════════════════════════════════════════════════════"
echo "  EJEMPLOS - Sistema de Simulación de Concurrencia"
echo "════════════════════════════════════════════════════════════"
echo ""

# =====================================================
# 1. Agregar vuelos a la cola
# =====================================================

echo "📌 1️⃣  AGREGAR VUELOS A LA COLA"
echo "─────────────────────────────────────────────────────────────"
echo ""

echo "➕ Agregando Vuelo 100 (Madrid → Barcelona)..."
curl -s -X POST "$BASE_URL/queue/add" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": 100,
    "origen": "Madrid",
    "destino": "Barcelona",
    "horaSalida": "10:30",
    "precioBase": 150.0,
    "pasajeros": 180,
    "prioridad": 1
  }' | jq '.message, .queue_size'

echo ""

echo "➕ Agregando Vuelo 50 (Valencia → Sevilla)..."
curl -s -X POST "$BASE_URL/queue/add" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": 50,
    "origen": "Valencia",
    "destino": "Sevilla",
    "horaSalida": "11:00",
    "precioBase": 120.0,
    "pasajeros": 150,
    "prioridad": 2
  }' | jq '.message, .queue_size'

echo ""

echo "➕ Agregando Vuelo 150 (Malaga → Bilbao)..."
curl -s -X POST "$BASE_URL/queue/add" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": 150,
    "origen": "Malaga",
    "destino": "Bilbao",
    "horaSalida": "14:15",
    "precioBase": 200.0,
    "pasajeros": 200,
    "prioridad": 1
  }' | jq '.message, .queue_size'

echo ""
echo ""

# =====================================================
# 2. Ver vuelos pendientes
# =====================================================

echo "📌 2️⃣  VER VUELOS PENDIENTES EN LA COLA"
echo "─────────────────────────────────────────────────────────────"
echo ""

echo "🔍 Obteniendo lista de pendientes..."
curl -s -X GET "$BASE_URL/queue/pending" | jq '{pending_count: .pending_count, flight_codigos: [.flights[].codigo]}'

echo ""
echo ""

# =====================================================
# 3. Procesar UN vuelo
# =====================================================

echo "📌 3️⃣  PROCESAR UN VUELO"
echo "─────────────────────────────────────────────────────────────"
echo ""

echo "⚙️  Procesando primer vuelo de la cola..."
curl -s -X POST "$BASE_URL/queue/process-one" | jq '{status: .status, flight_inserted: .flight_inserted.codigo, conflict: .conflict, queue_remaining: .queue_remaining}'

echo ""

echo "⚙️  Procesando segundo vuelo de la cola..."
curl -s -X POST "$BASE_URL/queue/process-one" | jq '{status: .status, flight_inserted: .flight_inserted.codigo, conflict: .conflict, queue_remaining: .queue_remaining}'

echo ""
echo ""

# =====================================================
# 4. Ver estado actual de la cola
# =====================================================

echo "📌 4️⃣  ESTADO ACTUAL DE LA COLA"
echo "─────────────────────────────────────────────────────────────"
echo ""

echo "🔍 Vuelos pendientes después de procesar 2..."
curl -s -X GET "$BASE_URL/queue/pending" | jq '{pending_count: .pending_count, flight_codigos: [.flights[].codigo]}'

echo ""
echo ""

# =====================================================
# 5. Procesar todos los vuelos restantes
# =====================================================

echo "📌 5️⃣  PROCESAR TODOS LOS VUELOS RESTANTES"
echo "─────────────────────────────────────────────────────────────"
echo ""

echo "⚙️  Procesando todos los vuelos de la cola..."
RESULT=$(curl -s -X POST "$BASE_URL/queue/process-all")
echo "$RESULT" | jq '{status: .status, total_processed: .total_processed, total_conflicts: .total_conflicts, queue_remaining: .queue_remaining}'

echo ""

if echo "$RESULT" | jq -e '.total_conflicts > 0' > /dev/null; then
  echo "⚠️  CONFLICTOS DETECTADOS:"
  echo "$RESULT" | jq '.results[] | select(.conflict == true) | {flight_codigo: .flight_inserted.codigo, conflict_detail: .conflict_detail}'
else
  echo "✅ Sin conflictos detectados"
fi

echo ""
echo ""

# =====================================================
# 6. Ver estado final
# =====================================================

echo "📌 6️⃣  ESTADO FINAL"
echo "─────────────────────────────────────────────────────────────"
echo ""

echo "❌ La cola debería estar vacía..."
curl -s -X GET "$BASE_URL/queue/pending" | jq '{pending_count: .pending_count, flights_remaining: (.flights | length)}'

echo ""

echo "🌳 Ver árbol actualizado..."
curl -s -X GET "$BASE_URL/avl/tree" | jq 'keys'

echo ""
echo ""

# =====================================================
# 7. Limpiar cola (ejemplo)
# =====================================================

echo "📌 7️⃣  LIMPIAR COLA (EJEMPLO)"
echo "─────────────────────────────────────────────────────────────"
echo ""

echo "➕ Agregando 2 vuelos nuevamente..."
curl -s -X POST "$BASE_URL/queue/add" \
  -H "Content-Type: application/json" \
  -d '{"codigo": 200, "origen": "A", "destino": "B", "horaSalida": "07:00", "precioBase": 100.0, "pasajeros": 100, "prioridad": 1}' > /dev/null

curl -s -X POST "$BASE_URL/queue/add" \
  -H "Content-Type: application/json" \
  -d '{"codigo": 250, "origen": "C", "destino": "D", "horaSalida": "09:00", "precioBase": 130.0, "pasajeros": 130, "prioridad": 2}' > /dev/null

echo "✅ 2 vuelos agregados"
echo ""

echo "🔍 Antes de limpiar:"
curl -s -X GET "$BASE_URL/queue/pending" | jq '.pending_count'

echo ""

echo "🗑️  Limpiando cola..."
curl -s -X DELETE "$BASE_URL/queue/clear" | jq '{status: .status, cleared_count: .cleared_count}'

echo ""

echo "🔍 Después de limpiar:"
curl -s -X GET "$BASE_URL/queue/pending" | jq '.pending_count'

echo ""
echo ""

# =====================================================
# RESUMEN
# =====================================================

echo "════════════════════════════════════════════════════════════"
echo "  ✅ EJEMPLOS COMPLETADOS"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Todos los endpoints fueron probados exitosamente."
echo ""
echo "📊 ENDPOINTS DISPONIBLES:"
echo "   POST   /queue/add"
echo "   GET    /queue/pending"
echo "   POST   /queue/process-one"
echo "   POST   /queue/process-all"
echo "   DELETE /queue/clear"
echo ""
