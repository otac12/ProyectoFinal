# Ubicación de Funciones del Diagrama de Red

Este documento muestra dónde se encuentran todas las funciones mencionadas en el discurso, organizadas por **Frontend** y **Backend**.

---

## 📁 FRONTEND - Funciones de Visualización

### Archivo: `frontend/src/components/NetworkDiagram.js`

Todas las funciones de visualización y construcción del diagrama están en este archivo.

#### Funciones Principales:

| Función | Línea | Descripción |
|---------|-------|-------------|
| `buildDiagram()` | **81** | Función principal que detecta el tipo de topología y llama a la función correspondiente |
| `buildStarTopology()` | **180** | Construye la visualización de topología en estrella |
| `buildBusTopology()` | **232** | Construye la visualización de topología en bus |
| `buildRingTopology()` | **332** | Construye la visualización de topología en anillo |
| `buildTreeTopology()` | **491** | Construye la visualización de topología en árbol |

#### Funciones de Creación de Nodos:

| Función | Línea | Descripción |
|---------|-------|-------------|
| `createOLTNode(x, y)` | **104** | Crea un nodo visual para el OLT con posición (x, y) |
| `createSplitterNode(splitter, x, y)` | **129** | Crea un nodo visual para un splitter con posición (x, y) |
| `createONUNode(onu, x, y)` | **154** | Crea un nodo visual para una ONU con posición (x, y) |

#### Funciones de Power Budget:

| Función | Línea | Descripción |
|---------|-------|-------------|
| `loadPowerBudget()` | **31** | Carga el power budget desde la API y actualiza los nodos |
| `updateNodesWithPowerBudget(powerBudgetData)` | **50** | Actualiza los nodos ONU con información de power budget |

#### Funciones de React Hooks:

| Hook/Función | Línea | Descripción |
|--------------|-------|-------------|
| `useEffect` (networkData) | **19** | Se ejecuta cuando cambia networkData y reconstruye el diagrama |
| `useEffect` (topology) | **25** | Se ejecuta cuando cambia topology y carga el power budget |
| `onConnect` | **588** | Callback para conectar nodos manualmente (ReactFlow) |

---

## 🔧 BACKEND - Funciones de Lógica de Negocio

### Archivo 1: `backend/models/network_elements.py`

Funciones de modelo y cálculo de la red óptica.

#### Clase: `OpticalNetwork`

| Función | Línea | Descripción |
|---------|-------|-------------|
| `create_ftth_topology(num_onus, split_ratio, topology_type)` | **187** | Función principal que crea la topología según el tipo especificado |
| `_create_star_topology(num_onus, split_ratio)` | **210** | Genera la estructura de datos para topología estrella |
| `_create_bus_topology(num_onus)` | **244** | Genera la estructura de datos para topología bus |
| `_create_ring_topology(num_onus)` | **292** | Genera la estructura de datos para topología anillo |
| `_create_tree_topology(num_onus, split_ratio)` | **365** | Genera la estructura de datos para topología árbol |
| `calculate_power_budget_path(onu)` | **440** | Calcula el power budget para una ONU específica |

#### Clase: `OLT`

| Función | Línea | Descripción |
|---------|-------|-------------|
| `calculate_power_budget()` | **19** | Calcula el power budget disponible del OLT |

### Archivo 2: `backend/app.py`

Funciones de API REST (endpoints).

| Función | Línea | Descripción |
|---------|-------|-------------|
| `calculate_power_budget(topology_id)` | **159** | Endpoint GET `/api/topologies/<id>/power-budget` que calcula y retorna el power budget |

---

## 📊 Flujo de Datos entre Frontend y Backend

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND                                 │
│  frontend/src/components/NetworkDiagram.js                 │
│                                                             │
│  1. buildDiagram() [Línea 81]                             │
│     ↓                                                        │
│  2. buildStarTopology() [Línea 180]                        │
│     - createOLTNode() [Línea 104]                          │
│     - createSplitterNode() [Línea 129]                     │
│     - createONUNode() [Línea 154]                          │
│                                                             │
│  3. loadPowerBudget() [Línea 31]                          │
│     ↓ HTTP GET Request                                      │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND                                  │
│  backend/app.py                                             │
│                                                             │
│  calculate_power_budget(topology_id) [Línea 159]           │
│     ↓                                                        │
│  backend/models/network_elements.py                       │
│                                                             │
│  OpticalNetwork.calculate_power_budget_path() [Línea 440]  │
│     ↓                                                        │
│  Retorna: powerBudgetData (JSON)                            │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND                                 │
│                                                             │
│  updateNodesWithPowerBudget() [Línea 50]                   │
│     - Actualiza nodos con información de power budget       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 Detalles de Implementación

### Frontend - Construcción de Topologías

**buildStarTopology()** (Línea 180-230):
- Distribuye ONUs en círculo alrededor del splitter central
- Usa trigonometría: `Math.cos()` y `Math.sin()` para posicionamiento

**buildBusTopology()** (Línea 232-330):
- Construye mapa de conexiones desde `networkData.fibers`
- Ordena splitters secuencialmente según conexiones
- Distribuye ONUs verticalmente sobre cada splitter

**buildRingTopology()** (Línea 332-489):
- Construye anillo con splitters y ONUs
- Maneja conexiones circulares entre splitters
- Distribuye elementos en círculo con radio adaptativo

**buildTreeTopology()** (Línea 491-586):
- Estructura jerárquica con splitters raíz, intermedios y terminales
- Distribuye ONUs en niveles según profundidad del árbol

### Backend - Generación de Topologías

**create_ftth_topology()** (Línea 187-208):
- Función principal que delega según `topology_type`
- Crea objetos Python: `OLT`, `Splitter`, `ONU`, `OpticalFiber`
- Retorna estructura de datos serializable

**calculate_power_budget_path()** (Línea 440-491):
- Calcula pérdidas de fibra, splitters y empalmes
- Calcula margen de seguridad
- Retorna diccionario con todos los valores calculados

---

## 📝 Resumen por Ubicación

### ✅ Frontend (1 archivo):
- **`frontend/src/components/NetworkDiagram.js`** - 630 líneas
  - 10 funciones principales de visualización
  - 2 hooks de React (useEffect)
  - 1 callback (onConnect)

### ✅ Backend (2 archivos):
- **`backend/models/network_elements.py`** - ~500 líneas
  - 6 funciones de generación de topologías
  - 1 función de cálculo de power budget
  
- **`backend/app.py`** - ~200 líneas
  - 1 endpoint REST para power budget

---

## 🎯 Funciones Clave para la Presentación

### Para mostrar visualización:
- **Frontend**: `buildDiagram()`, `buildStarTopology()`, `createOLTNode()`, `createONUNode()`

### Para mostrar cálculos:
- **Backend**: `calculate_power_budget_path()`, `calculate_power_budget()` (endpoint)

### Para mostrar integración:
- **Frontend**: `loadPowerBudget()` → **Backend**: `calculate_power_budget()` → **Frontend**: `updateNodesWithPowerBudget()`

---

**Nota**: Todas las funciones del frontend están en un solo archivo para facilitar el mantenimiento y la comprensión del flujo de visualización.


