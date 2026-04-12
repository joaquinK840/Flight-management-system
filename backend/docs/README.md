# Flight Management System - Backend

Sistema de gestión de vuelos implementado con estructuras de datos AVL y BST en Python, con API REST en FastAPI.

## 📋 Tabla de Contenidos

- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Arquitectura](#arquitectura)
- [Endpoints Disponibles](#endpoints-disponibles)
- [Documentación Completa](#documentación-completa)

---

## 🏗️ Estructura del Proyecto

```
backend/
├── core/
│   └── structures/
│       ├── avl_tree/              # Árbol AVL (balanceado)
│       │   ├── tree.py            # Clase AVL
│       │   ├── insert.py          # Inserción
│       │   ├── delete.py          # Eliminación
│       │   ├── balance.py         # Balanceo y rotaciones
│       │   ├── rotations.py       # Rotaciones izq/dcha
│       │   ├── search.py          # Búsqueda
│       │   └── traversal.py       # Recorridos
│       ├── bst_tree/              # Árbol BST (sin balanceo)
│       │   └── bst.py             # Clase BST
│       ├── node/                  # Nodos
│       │   └── node.py            # Clase Node
│       ├── stack/                 # Estructura Stack
│       │   └── stack.py           # Pila para undo
│       └── queue/                 # Estructura Queue
│           └── queue.py
├── controllers/                   # Lógica de negocio (opcional)
├── routes/                        # Rutas (Endpoints FastAPI)
│   ├── avl_routes.py             # Rutas AVL base
│   └── flight_routes.py          # Rutas de operaciones de vuelos
├── services/                      # Servicios-utilitarios
│   ├── tree_repository.py        # Patrón Repository (gestión de undo)
│   ├── json_manager.py           # Carga JSON
│   ├── serialize_tree.py         # Serialización de árboles
│   ├── metrics.py                # Cálculo de métricas
│   └── validator.py
├── models/                        # Modelos de datos
│   └── flight.py
├── data/                          # Archivos JSON de ejemplo
│   ├── TopologiaEjemplo.json
│   └── InsercionEjemplo.json
├── docs/                          # Documentación
│   ├── FLIGHTS_ENDPOINTS.md      # Documentación de endpoints
│   ├── LOAD_FILE_ENDPOINT.md     # Endpoint de carga
│   └── README.md                 # Este archivo
├── main.py                        # Punto de entrada FastAPI
├── requirements.txt               # Dependencias Python
└── .env                           # Variables de entorno (si es necesario)
```

---

## ✋ Requisitos

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic

---

## 🚀 Instalación

```bash
# Crear y activar entorno virtual
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate       # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

---

## ▶️ Ejecución

```bash
# Desde la carpeta backend/
uvicorn main:app --reload --port 8000
```

La API estará disponible en: `http://localhost:8000`

API Docs (Swagger): `http://localhost:8000/docs`

---

## 🏛️ Arquitectura

### Capas

```
┌────────────────────────────────┐
│   REST API (FastAPI)           │
│   - flight_routes.py           │
│   - avl_routes.py              │
├────────────────────────────────┤
│   Services Layer               │
│   - TreeRepository (Patrón)    │
│   - json_manager               │
│   - metrics                    │
├────────────────────────────────┤
│   Data Structures              │
│   - AVL (balanceado)           │
│   - BST (sin balanceo)         │
│   - Node                       │
│   - Stack (undo)               │
└────────────────────────────────┘
```

### Patrones Implementados

1. **Repository Pattern**: `TreeRepository` encapsula lógica de árbol
2. **Single Responsibility**: Cada clase tiene una responsabilidad
3. **Open/Closed Principle**: Fácil extender (nuevos tipos de árboles)
4. **Separation of Concerns**: Rutas → Servicios → Modelos

---

## 🔗 Endpoints Disponibles

### Router `/avl` (Operaciones AVL base)

- `POST /avl/insert/{value}` - Insertar número
- `GET /avl/tree` - Obtener árbol
- `GET /avl/search/{value}` - Buscar
- `DELETE /avl/reset` - Reiniciar
- `GET /avl/metrics` - Métricas
- `POST /avl/load-file` - Cargar desde JSON

### Router `/flights` (Operaciones de vuelos) ⭐ NUEVO

- `POST /flights/insert` - Insertar vuelo
- `DELETE /flights/delete/{codigo}` - Eliminar vuelo
- `DELETE /flights/cancel/{codigo}` - Cancelar subárbol
- `PUT /flights/update/{codigo}` - Actualizar datos
- `POST /flights/undo` - Deshacer operación
- `POST /flights/redo` - Rehacer operación
- `GET /flights/tree` - Obtener árbol
- `GET /flights/metrics` - Métricas
- `POST /flights/stress-mode/{enabled}` - Toggle stress mode
- `DELETE /flights/reset` - Reiniciar

---

## 📖 Documentación Completa

### Documentación por Componente

- **[FLIGHTS_ENDPOINTS.md](FLIGHTS_ENDPOINTS.md)** - Documentación completa de endpoints de vuelos
- **[LOAD_FILE_ENDPOINT.md](LOAD_FILE_ENDPOINT.md)** - Carga de árboles desde JSON

### Ejemplos de Uso

Consulta `FLIGHTS_ENDPOINTS.md` para:
- Ejemplos de solicitudes curl
- Estructura de responses
- Códigos de error
- Flujos completos

---

## 🎯 Características Principales

### Operaciones de Vuelos

✅ **Inserción**: Con balanceo AVL o sin balanceo (stress_mode)  
✅ **Eliminación**: Elimina solo el nodo (sucesor lo reemplaza)  
✅ **Cancelación**: Elimina todo el subárbol + descendientes  
✅ **Actualización**: Modifica datos sin cambiar posición  

### Gestión de Undo

✅ **Pila de Undo**: Cada operación guarda estado anterior  
✅ **Redo**: Rehace operaciones deshecha  
✅ **Serialización**: Estados completos guardados  

### Modos de Operación

✅ **Balance AVL**: Altura optimizada (~log n)  
✅ **Stress Mode**: Sin rotaciones, como BST  
✅ **Comparación**: Métricas de ambos árboles  

---

## 📊 Modelo de Datos: Vuelo

```json
{
  "codigo": 100,           // int - Identificador único
  "origen": "Madrid",      // str - Ciudad de origen
  "destino": "Barcelona",  // str - Ciudad destino
  "horaSalida": "10:30",   // str - Hora de salida
  "precioBase": 150.00,    // float - Precio sin descuento
  "precioFinal": 150.00,   // float - Precio final
  "pasajeros": 180,        // int - Número de pasajeros
  "promocion": false,      // bool - Tiene promoción
  "alerta": "normal",      // str - Nivel de alerta
  "prioridad": 1           // int - Prioridad del vuelo
}
```

---

## 🔧 Configuración

### TreeRepository

```python
# Usar AVL (con balanceo)
repo = TreeRepository(use_bst=False)

# Usar BST (sin balanceo)
repo = TreeRepository(use_bst=True)
```

### Stress Mode

```python
# Activa desde endpoint
POST /flights/stress-mode/true

# O directamente
flight_repository.tree.stress_mode = True
```

---

## 🧪 Testing

Para testear los endpoints, puedes usar:

1. **Swagger UI**: `http://localhost:8000/docs`
2. **curl**: Ver ejemplos en FLIGHTS_ENDPOINTS.md
3. **Postman**: Importar colección

---

## 📝 Notas de Desarrollo

### Stack (Pila de Undo)

- Implementada en `core/structures/stack/stack.py`
- Usada por `TreeRepository` para gestionar undo
- LIFO (Last In, First Out)
- Métodos: `push()`, `pop()`, `peek()`, `is_empty()`, `size()`

### TreeRepository

- Patrón Repository para encapsular lógica
- Gestiona serialización/deserialización de estados
- Maneja pila de undo y redo
- Single Responsibility

### Datos de Vuelo

- Guardados como `datos` dict en cada `Node`
- Opcionalmente descompuesto en campos específicos
- Flexible para agregar más campos

---

## 🤝 Contribuciones

Las contribuciones siguen estos principios:
1. Single Responsibility Principle (SRP)
2. Open/Closed Principle (OCP)
3. Dependency Inversion Principle (DIP)

---

## 📄 Licencia

[Especificar licencia si aplica]

---

**Última actualización**: 12 de abril de 2026
