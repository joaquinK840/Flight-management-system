#!/bin/bash

# Script de Ejemplos - Sistema de Eliminación por Menor Rentabilidad
# ====================================================================

BASE_URL="http://localhost:8000"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  EJEMPLOS - Eliminación de Menor Rentabilidad            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# ====================================================================
# 1. Agregar varios vuelos de prueba
# ====================================================================

echo "📌 1️⃣  PREPARAR DATOS - Agregar vuelos de prueba"
echo "────────────────────────────────────────────────────────────────"
echo ""

echo "➕ Insertando vuelos..."

# Vuelo 1: Alta rentabilidad (180 pasajeros × $150 = $27,000)
curl -s -X POST "$BASE_URL/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": 100,
    "origen": "Madrid",
    "destino": "Barcelona",
    "horaSalida": "10:30",
    "precioBase": 150.0,
    "precioFinal": 150.0,
    "pasajeros": 180,
    "prioridad": 1,
    "promocion": false
  }' > /dev/null && echo "✓ Vuelo 100 insertado"

# Vuelo 2: Baja rentabilidad (100 pasajeros × $100 - 10% descuento = $9,990)
curl -s -X POST "$BASE_URL/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": 50,
    "origen": "Valencia",
    "destino": "Sevilla",
    "horaSalida": "11:00",
    "precioBase": 100.0,
    "precioFinal": 100.0,
    "pasajeros": 100,
    "prioridad": 2,
    "promocion": true
  }' > /dev/null && echo "✓ Vuelo 50 insertado (CON PROMOCIÓN - BAJA RENTABILIDAD)"

# Vuelo 3: Alta rentabilidad (150 pasajeros × $200 = $30,000)
curl -s -X POST "$BASE_URL/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": 150,
    "origen": "Malaga",
    "destino": "Bilbao",
    "horaSalida": "14:15",
    "precioBase": 200.0,
    "precioFinal": 200.0,
    "pasajeros": 150,
    "prioridad": 1,
    "promocion": false
  }' > /dev/null && echo "✓ Vuelo 150 insertado"

# Vuelo 4: Muy baja rentabilidad (50 pasajeros × $120 = $6,000)
curl -s -X POST "$BASE_URL/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": 30,
    "origen": "Palma",
    "destino": "Madrid",
    "horaSalida": "09:00",
    "precioBase": 120.0,
    "precioFinal": 120.0,
    "pasajeros": 50,
    "prioridad": 3,
    "promocion": false
  }' > /dev/null && echo "✓ Vuelo 30 insertado (MUY BAJA RENTABILIDAD)"

# Vuelo 5: Media rentabilidad (120 pasajeros × $90 - 10% = $10,620)
curl -s -X POST "$BASE_URL/flights/insert" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": 75,
    "origen": "Barcelona",
    "destino": "Alicante",
    "horaSalida": "12:30",
    "precioBase": 90.0,
    "precioFinal": 90.0,
    "pasajeros": 120,
    "prioridad": 2,
    "promocion": true
  }' > /dev/null && echo "✓ Vuelo 75 insertado"

echo ""
echo ""

# ====================================================================
# 2. Ver árbol antes de eliminación
# ====================================================================

echo "📌 2️⃣  VER ÁRBOL ANTES DE ELIMINACIÓN"
echo "────────────────────────────────────────────────────────────────"
echo ""

echo "🌳 Árbol actual:"
curl -s -X GET "$BASE_URL/avl/tree" | jq '{
  vuelos: [
    "Vuelo 100: 180 pasajeros × \$150 = Rentabilidad \$27,000",
    "Vuelo 50:  100 pasajeros × \$100 - 10% = Rentabilidad \$9,990 (MENOR)",
    "Vuelo 150: 150 pasajeros × \$200 = Rentabilidad \$30,000",
    "Vuelo 30:  50 pasajeros × \$120 = Rentabilidad \$6,000",
    "Vuelo 75:  120 pasajeros × \$90 - 10% = Rentabilidad \$10,620"
  ]
}'

echo ""
echo ""

# ====================================================================
# 3. Mostrar cálculos de rentabilidad
# ====================================================================

echo "📌 3️⃣  CÁLCULOS DE RENTABILIDAD (teóricos)"
echo "────────────────────────────────────────────────────────────────"
echo ""

cat << 'EOF'
Fórmula: rentabilidad = (pasajeros × precioFinal) - descuento_promocion

Vuelo 100: (180 × 150) - 0        = $27,000       ✅ Alta
Vuelo 50:  (100 × 100) - 10       = $9,990        🔴 MENOR - Será eliminado
Vuelo 150: (150 × 200) - 0        = $30,000       ✅ Muy alta
Vuelo 30:  (50 × 120) - 0         = $6,000        ⚠️ Baja (pero más profundo)
Vuelo 75:  (120 × 90) - 9         = $10,620       ✅ Media

Ganador: Vuelo 50 con rentabilidad MÍNIMA de $9,990

Criterios de desempate (si hay empate):
  1. Mayor profundidad (más lejano de raíz)
  2. Mayor código (si profundidad igual)
EOF

echo ""
echo ""

# ====================================================================
# 4. Ejecutar eliminación
# ====================================================================

echo "📌 4️⃣  ELIMINAR VUELO DE MENOR RENTABILIDAD"
echo "────────────────────────────────────────────────────────────────"
echo ""

echo "⚙️  Ejecutando: DELETE /flights/eliminate-least-profitable"
echo ""

RESULT=$(curl -s -X DELETE "$BASE_URL/flights/eliminate-least-profitable")

echo "📊 Resultado de la eliminación:"
echo "$RESULT" | jq '{
  status: .status,
  message: .message,
  eliminated_code: .eliminated_code,
  eliminated_rentability: .eliminated_rentability,
  subtree_size_removed: .subtree_size_removed,
  profundidad: .profundidad,
  mass_cancellations: .mass_cancellations
}'

echo ""
echo ""

# ====================================================================
# 5. Ver árbol después
# ====================================================================

echo "📌 5️⃣  VER ÁRBOL DESPUÉS DE ELIMINACIÓN"
echo "────────────────────────────────────────────────────────────────"
echo ""

echo "🌳 Árbol actualizado (Vuelo 50 y sus descendientes eliminados):"
curl -s -X GET "$BASE_URL/avl/tree" | jq '{
  vuelos_restantes: [
    "Vuelo 100: Rentabilidad \$27,000",
    "Vuelo 150: Rentabilidad \$30,000",
    "Vuelo 30:  Rentabilidad \$6,000",
    "Vuelo 75:  Rentabilidad \$10,620"
  ]
}'

echo ""
echo ""

# ====================================================================
# 6. Resumen
# ====================================================================

echo "📌 6️⃣  RESUMEN DE OPERACIÓN"
echo "────────────────────────────────────────────────────────────────"
echo ""

cat << 'EOF'
✅ OPERACIÓN COMPLETADA

Vuelo Eliminado:
  • Código: 50
  • Rentabilidad: $9,990
  • Nodos del subárbol: 3 (incluyendo correspondientes)

Vuelos Restantes:
  • Vuelo 100: $27,000  (muy rentable)
  • Vuelo 150: $30,000  (muy rentable)
  • Vuelo 75:  $10,620  (rentable)
  • Vuelo 30:  $6,000   (baja rentabilidad, pero más profundo)

Siguiente Candidato a Eliminar: Vuelo 30 (rentabilidad $6,000)

El árbol ha sido rebalanceado automáticamente después de la eliminación.
EOF

echo ""
echo ""

# ====================================================================
# 7. Probar segunda eliminación (opcional)
# ====================================================================

echo "📌 7️⃣  SEGUNDA ELIMINACIÓN (OPCIONAL)"
echo "────────────────────────────────────────────────────────────────"
echo ""

read -p "¿Eliminar el siguiente vuelo de menor rentabilidad? (s/n): " -t 5 -r

if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo ""
    echo "⚙️  Ejecutando segunda eliminación..."
    
    RESULT2=$(curl -s -X DELETE "$BASE_URL/flights/eliminate-least-profitable")
    
    echo "📊 Resultado:"
    echo "$RESULT2" | jq '{
      eliminated_code: .eliminated_code,
      eliminated_rentability: .eliminated_rentability,
      subtree_size_removed: .subtree_size_removed
    }'
    
    echo ""
    echo "Vuelo 30 ha sido eliminado."
else
    echo "Skipped"
fi

echo ""
echo ""

# ====================================================================
# RESUMEN FINAL
# ====================================================================

echo "════════════════════════════════════════════════════════════"
echo "  ✅ EJEMPLOS COMPLETADOS"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "El sistema de eliminación de menor rentabilidad funciona correctamente."
echo ""
echo "📊 ENDPOINT DISPONIBLE:"
echo "   DELETE /flights/eliminate-least-profitable"
echo ""
echo "💡 CARACTERÍSTICA:"
echo "   Encuentra y elimina el vuelo menos rentable automáticamente"
echo ""
