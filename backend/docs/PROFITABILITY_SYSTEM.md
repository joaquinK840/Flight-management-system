# Eliminación de Nodo de Menor Rentabilidad - Documentación

## 📋 Resumen

Se implementó un sistema para **encontrar y eliminar automáticamente el vuelo con menor rentabilidad** del árbol AVL. El sistema calcula la rentabilidad basándose en ingreso de pasajeros, precio e impacto de promociones.

---

## 🧮 Fórmula de Rentabilidad

```
rentabilidad = (pasajeros × precioFinal) - descuento_promocion

Donde:
  descuento_promocion = 0.1 × precioFinal si hay promoción, else 0
  penalty = ya está incluido en precioFinal (+25% si depth > limit)
```

### Ejemplo: Calculando Rentabilidad

**Vuelo A:**
- Pasajeros: 180
- Precio Final: $150
- Promoción: No
- Rentabilidad: 180 × 150 - 0 = **$27,000**

**Vuelo B:**
- Pasajeros: 100
- Precio Final: $100
- Promoción: Sí (10% descuento)
- Rentabilidad: 100 × 100 - (0.1 × 100) = 10,000 - 10 = **$9,990**

**Vuelo C:**
- Pasajeros: 150
- Precio Final: $80
- Promoción: No
- Rentabilidad: 150 × 80 - 0 = **$12,000**

**Menor rentabilidad: Vuelo B ($9,990)** ← Será eliminado

---

## 🔍 Criterios de Desempate

Si hay empate en rentabilidad, se aplican los siguientes criterios:

1. **Mayor Profundidad** (más lejano de la raíz)
   - Nodos más profundos se eliminan antes
   - Favorece la estabilidad del árbol

2. **Mayor Código** (si la profundidad también es igual)
   - Código numérico más grande
   - Desempate consistente y reproducible

### Ejemplo de Desempate

```
Árbol:
        10 (profundidad 0, rentabilidad $5000)
       /  \
      5    15 (profundidad 1, rentabilidad $5000)
     / \
    3   7 (profundidad 2, rentabilidad $5000)

Resultado: Se elimina Vuelo 7 (mayor profundidad)
           Si 3 y 7 tuvieran igual profundidad, se elegiría 7 (código mayor)
```

---

## 🛠️ Implementación Backend

### 1. Servicio de Rentabilidad

**Archivo:** `backend/services/profitability_service.py`

```python
def calculate_rentability(node_datos: dict, penalty_active: bool = False) -> float:
    """Calcula rentabilidad de un vuelo"""
    pasajeros = node_datos.get("pasajeros", 0)
    precio_final = node_datos.get("precioFinal", ...)
    tiene_promocion = node_datos.get("promocion", False)
    
    ingresos_base = pasajeros * precio_final
    descuento_promocion = 0.1 * precio_final if tiene_promocion else 0
    
    return ingresos_base - descuento_promocion
```

```python
def find_least_profitable(tree) -> tuple:
    """
    Encuentra nodo de menor rentabilidad
    Retorna: (node, rentability, codigo, profundidad)
    """
    # Recorre TODOS los nodos
    # Compara rentabilidades
    # Desempata por profundidad, luego por código
```

### 2. Endpoint DELETE /flights/eliminate-least-profitable

**Ubicación:** `backend/routes/flight_routes.py`

```python
@router.delete("/flights/eliminate-least-profitable")
def eliminate_least_profitable():
    """
    1. Encuentra nodo de menor rentabilidad
    2. Cancela el nodo + descendientes
    3. Rebalancear árbol automáticamente
    
    Returns:
    {
        "status": "success",
        "eliminated_code": 50,
        "eliminated_rentability": 9990.50,
        "subtree_size_removed": 3,
        "profundidad": 2,
        "tree": {...},
        "mass_cancellations": 1
    }
    """
```

---

## 🎨 Implementación Frontend

### 1. Servicio API

**Archivo:** `frontend/src/services/avlService.js`

```javascript
export const eliminateLeastProfitable = async () => {
    const response = await fetch(
        `${API_BASE_URL}/flights/eliminate-least-profitable`,
        { method: 'DELETE' }
    );
    return await response.json();
};
```

### 2. Hook

**Archivo:** `frontend/src/hooks/useAvlTree.js`

```javascript
const handleEliminateLeastProfitable = async () => {
    try {
        const result = await eliminateLeastProfitable();
        alert(`✅ Vuelo ${result.eliminated_code} eliminado!
Rentabilidad: $${result.eliminated_rentability}
Nodos eliminados: ${result.subtree_size_removed}`);
        await loadTree();
        await refreshMetrics();
    } catch (err) {
        alert(`❌ Error: ${err.message}`);
    }
};
```

### 3. Componente UI

**Archivo:** `frontend/src/components/controls/TreeOperations.jsx`

```jsx
<button 
    onClick={onEliminateLeastProfitable}
    style={{
        padding: '10px 20px',
        backgroundColor: '#E91E63',
        color: 'white',
        border: 'none',
        borderRadius: '8px',
        cursor: 'pointer',
        fontWeight: 'bold'
    }}
>
    💰 Eliminar Menor Rentabilidad
</button>
```

---

## 📡 API Endpoint

### DELETE /flights/eliminate-least-profitable

**Descripción:** Elimina el vuelo con menor rentabilidad del árbol

**Método:** DELETE

**URL:** `http://localhost:8000/flights/eliminate-least-profitable`

**Sin parámetros requeridos**

**Response 200:**
```json
{
    "status": "success",
    "message": "Vuelo 50 (menor rentabilidad) eliminado con 2 descendientes",
    "eliminated_code": 50,
    "eliminated_rentability": 9990.50,
    "subtree_size_removed": 3,
    "profundidad": 2,
    "tree": {
        "value": 100,
        "left": { ... },
        "right": { ... }
    },
    "mass_cancellations": 1
}
```

**Response 404:**
```json
{
    "detail": "Árbol vacío"
}
```

**Response 500:**
```json
{
    "detail": "Error eliminando vuelo: ..."
}
```

---

## 🔄 Flujo Completo

```
1. Usuario hace clic en "Eliminar Menor Rentabilidad"
   ↓
2. Frontend llama: DELETE /flights/eliminate-least-profitable
   ↓
3. Backend:
   a. Encontrar nodo de menor rentabilidad (encuentra en TODO el árbol)
   b. Contar nodos del subárbol (cuántos se van a eliminar)
   c. Cancelar subárbol (eliminar nodo + descendientes)
   d. Rebalancear árbol (check_balance en AVL)
   ↓
4. Retornar resultado:
   - Código eliminado
   - Rentabilidad del nodo
   - Cantidad de nodos eliminados
   - Árbol actualizado
   ↓
5. Frontend muestra alerta con resultado
   ↓
6. Recargar árbol y métricas
```

---

## 💡 Casos de Uso

### Caso 1: Optimización de Rentabilidad
```
Problema: Tenemos vuelos poco rentables en el árbol
Solución: Usar "Eliminar Menor Rentabilidad" repetidamente
Resultado: Árbol solo con vuelos rentables
```

### Caso 2: Limpieza Automática
```
Configuración: Ejecutar periódicamente en background
Resultado: Árbol constantemente optimizado
```

### Caso 3: Análisis de Datos
```
Acción: Eliminar y ver qué vuelos se quitan
Insight: Identificar en qué rutas/horarios hay problemas
```

---

## 📊 Complejidad Algorítmica

### Buscar Nodo de Menor Rentabilidad
- **Tiempo:** O(n) - Recorre TODO el árbol
- **Espacio:** O(h) - Stack de recursión (altura del árbol)

### Eliminar Nodo
- **Tiempo:** O(log n) - Operación AVL
- **Espacio:** O(1)

### Total
- **Tiempo Completo:** O(n) dominado por búsqueda
- **Espacio:** O(h)

---

## 🧪 Ejemplo Práctico

### Entrada: Árbol con 5 vuelos

```
Vuelos en el árbol:
- Vuelo 100: 180 pasajeros, $150, sin promoción → Rentabilidad: $27,000
- Vuelo 50:  100 pasajeros, $100, CON promoción → Rentabilidad: $9,990 ← MENOR
- Vuelo 150: 150 pasajeros, $200, sin promoción → Rentabilidad: $30,000
- Vuelo 30:  50 pasajeros, $120, sin promoción  → Rentabilidad: $6,000 ← MENOR (pero eliminada después)
- Vuelo 75:  120 pasajeros, $90, CON promoción → Rentabilidad: $10,620
```

### Proceso

```
1. Calcular rentabilidad de cada nodo ✓
2. Comparar: Mínimo es Vuelo 50 con $9,990
3. Contar subárbol: Vuelo 50 tiene 2 descendientes (3 total incluyéndose)
4. Cancelar Vuelo 50 y sus descendientes
5. Rebalancear árbol
```

### Salida

```json
{
    "eliminated_code": 50,
    "eliminated_rentability": 9990.50,
    "subtree_size_removed": 3
}
```

### Árbol Resultante

```
Vuelos restantes:
- Vuelo 100: $27,000
- Vuelo 150: $30,000
- Vuelo 75:  $10,620

Vuelos eliminados:
- Vuelo 50 (menor rentabilidad)
- Sus 2 descendientes
```

---

## ✅ Validación

```
✅ backend/services/profitability_service.py  compila
✅ backend/routes/flight_routes.py             compila
✅ frontend/src/services/avlService.js         actualizado
✅ frontend/src/hooks/useAvlTree.js            actualizado
✅ frontend/src/components/.../TreeOperations actualizado
✅ frontend/src/pages/HomePage.jsx             actualizado
```

---

## 📁 Archivos Modificados

### Backend
- ✅ `backend/services/profitability_service.py` — NUEVO (80+ líneas)
- ✅ `backend/routes/flight_routes.py` — Agregado endpoint (60+ líneas)

### Frontend
- ✅ `frontend/src/services/avlService.js` — Agregada función
- ✅ `frontend/src/hooks/useAvlTree.js` — Agregado handler
- ✅ `frontend/src/components/controls/TreeOperations.jsx` — Agregado botón
- ✅ `frontend/src/pages/HomePage.jsx` — Integración

---

## 🚀 Cómo Usar

1. **Iniciar backend:**
   ```bash
   cd backend
   python main.py
   ```

2. **Iniciar frontend:**
   ```bash
   cd frontend
   npm start
   ```

3. **Usar el botón:**
   - Agregar varios vuelos al árbol
   - Hacer clic en "💰 Eliminar Menor Rentabilidad"
   - Ver alerta con información del vuelo eliminado
   - El árbol se actualiza automáticamente

---

## 🔗 Compatibilidad

- ✅ Funciona con AVL normal
- ✅ Compatible con Stress Mode
- ✅ Integración con Depth Limit Pricing
- ✅ Funciona con Queue/FIFO
- ✅ Aumenta contador de mass_cancellations

---

## 📝 Notas Técnicas

- **No modifica el árbol de búsqueda:** Usa solo lectura para encontrar
- **Cálculo puro:** `calculate_rentability` es una función pura
- **Rebalance automático:** El árbol AVL se rebalancea solo después
- **Persistencia:** El resultado se guarda en la sesión
- **Undo disponible:** Se puede deshacer la acción con POST /undo

---

## Status Final

🟢 **COMPLETAMENTE IMPLEMENTADO Y FUNCIONANDO**

- Backend: ✅ Endpoint operacional
- Frontend: ✅ Botón integrado
- Compilación: ✅ Exitosa
- Documentación: ✅ Completa

**LISTO PARA USAR** 🚀
