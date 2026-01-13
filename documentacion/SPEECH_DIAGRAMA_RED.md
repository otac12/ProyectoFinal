# Discurso de Presentación: Diagrama de Red FTTH GPON

## Introducción

Buenos días/tardes. Hoy les presentaré el **Diagrama de Red Interactivo** de nuestro simulador FTTH GPON, explicando las funciones implementadas y su impacto en la arquitectura del sistema.

---

## 1. Ubicación y Especificación Técnica

### 1.1. Archivo del Componente

El componente del Diagrama de Red se encuentra en:
```
frontend/src/components/NetworkDiagram.js
```

Este archivo contiene **630 líneas de código** y utiliza las siguientes tecnologías:
- **React** (Hooks: useState, useEffect, useCallback)
- **ReactFlow** (librería de visualización de grafos)
- **Material-UI** (componentes de interfaz)
- **Axios** (comunicación con API REST)

### 1.2. Datos de Entrada (Props)

El componente recibe **tres parámetros** como props:

#### 1. `networkData` (Object)
Estructura completa de la red óptica GPON:
```javascript
{
  name: "GPON Network",
  topology_type: "star" | "bus" | "ring" | "tree",
  olt: {
    id: "OLT-1",
    name: "OLT Principal",
    tx_power: 2.5,        // dBm
    rx_sensitivity: -27,   // dBm
    total_capacity: 2500  // Mbps
  },
  splitters: [
    {
      id: "SPLIT-1",
      name: "Splitter 1",
      ratio: "1:32",
      split_loss: 15.05,  // dB
      insertion_loss: 0.5  // dB
    }
  ],
  onus: [
    {
      id: "ONU-1",
      name: "ONU 1",
      tx_power: 1.5,       // dBm
      rx_sensitivity: -24, // dBm
      traffic_rate: 100,   // Mbps
      requested_bandwidth: 120 // Mbps
    }
  ],
  fibers: [
    {
      id: "FIBER-1",
      name: "Fiber 1",
      length: 5.0,        // km
      from_element: "OLT-1",
      to_element: "SPLIT-1",
      attenuation: 0.2,   // dB/km
      splice_loss: 0.1   // dB
    }
  ]
}
```

#### 2. `topology` (Object)
Información de la topología seleccionada:
```javascript
{
  id: 1,
  name: "Topología Estrella 32 ONUs",
  description: "Red GPON estándar",
  created_at: "2024-01-15T10:30:00",
  // ... otros campos de la base de datos
}
```

#### 3. `onPowerBudgetLoad` (Function)
Callback para notificar al componente padre cuando se carga el power budget:
```javascript
(powerBudgetData) => {
  // Actualiza el estado en App.js
  setPowerBudgetData(powerBudgetData);
}
```

### 1.3. Datos de Salida

El componente **NO retorna datos directamente**, pero genera:

#### A. Estado Interno (React State)
```javascript
// Nodos del diagrama (array de objetos ReactFlow)
nodes: [
  {
    id: "OLT-1",
    type: "input",
    position: { x: 425, y: 100 },
    data: {
      label: <div>OLT Principal<br/>TX: 2.5 dBm</div>
    },
    style: {
      background: '#2196F3',
      color: '#fff',
      border: '2px solid #1976D2',
      borderRadius: '10px',
      padding: '10px',
      width: 150
    }
  },
  // ... más nodos (Splitters, ONUs)
]

// Conexiones entre nodos (array de objetos ReactFlow)
edges: [
  {
    id: "e-OLT-1-SPLIT-1",
    source: "OLT-1",
    target: "SPLIT-1",
    animated: true,
    style: { stroke: '#FF9800', strokeWidth: 3 }
  },
  // ... más edges
]
```

#### B. Llamada a Callback (onPowerBudgetLoad)
Cuando se calcula el power budget, se envía al componente padre:
```javascript
powerBudgetData: [
  {
    onu_id: "ONU-1",
    power_budget: 29.5,        // dB
    tx_power: 2.5,            // dBm
    rx_sensitivity: -27,       // dBm
    splitter_loss: 15.05,      // dB
    split_ratio: "1:32",
    fiber_losses: [
      { fiber_id: "FIBER-1", loss: 1.0 }
    ],
    total_fiber_loss: 1.0,     // dB
    total_splice_loss: 0.1,    // dB
    total_loss: 16.15,         // dB
    margin: 3.0,                // dB
    available_power: 13.35,     // dB
    is_valid: true              // boolean
  },
  // ... un objeto por cada ONU
]
```

#### C. Renderizado Visual
El componente renderiza:
- **Diagrama interactivo** con ReactFlow
- **MiniMap** (vista general)
- **Controles** (zoom, pan, fit view)
- **Fondo con cuadrícula**
- **Información de la topología** (nombre, número de ONUs, tipo)

#### D. Llamadas a API
El componente realiza una llamada HTTP GET:
```javascript
GET /api/topologies/{topology_id}/power-budget
```
**Respuesta esperada:**
```json
{
  "success": true,
  "data": [
    {
      "onu_id": "ONU-1",
      "power_budget": 29.5,
      "available_power": 13.35,
      "is_valid": true,
      // ... más campos
    }
  ]
}
```

---

## 2. Visión General del Diagrama de Red

El diagrama de red es el componente central de visualización de nuestro simulador. Permite representar gráficamente las topologías de red GPON de manera interactiva y dinámica, facilitando la comprensión de la estructura de la red y el análisis de su rendimiento.

---

## 3. Funciones Principales Implementadas

### 3.1. Visualización de Múltiples Topologías

El diagrama soporta **cuatro tipos de topologías** diferentes:

- **Topología Estrella (Star)**: La más común en GPON, donde un splitter central distribuye la señal a múltiples ONUs en forma radial.
- **Topología Bus**: Los splitters se conectan secuencialmente en una línea, ideal para despliegues lineales.
- **Topología Anillo (Ring)**: Los elementos se conectan formando un anillo, proporcionando redundancia.
- **Topología Árbol (Tree)**: Estructura jerárquica con splitters raíz, intermedios y terminales.

**Función técnica**: `buildDiagram()` detecta el tipo de topología y llama a la función correspondiente (`buildStarTopology()`, `buildBusTopology()`, `buildRingTopology()`, `buildTreeTopology()`).

### 3.2. Creación Dinámica de Nodos

El sistema crea tres tipos de nodos visuales:

- **Nodos OLT (Optical Line Terminal)**: Representados en azul, muestran el nombre y la potencia de transmisión (TX Power).
- **Nodos Splitter**: Representados en naranja, muestran el ratio de división y la pérdida por split.
- **Nodos ONU (Optical Network Unit)**: Representados en verde, muestran el nombre y la tasa de tráfico.

**Funciones técnicas**: `createOLTNode()`, `createSplitterNode()`, `createONUNode()` generan los nodos con estilos personalizados y posicionamiento automático.

### 3.3. Visualización de Conexiones (Edges)

Las conexiones entre elementos se representan mediante **aristas animadas** que muestran:
- El flujo de datos desde el OLT hacia las ONUs
- Diferentes colores según el tipo de conexión (naranja para OLT-Splitter, verde para Splitter-ONU)
- Animación para indicar el tráfico activo

### 3.4. Cálculo y Visualización de Power Budget

Una de las funciones más importantes es el **cálculo automático del presupuesto de potencia óptica**:

- El sistema consulta el backend mediante la API `/topologies/{id}/power-budget`
- Actualiza los nodos ONU con información de potencia disponible
- Muestra indicadores visuales (verde/rojo) según si el power budget es válido
- La función `loadPowerBudget()` se ejecuta automáticamente cuando se carga una topología

**Impacto**: Permite validar si la red cumple con los requisitos de potencia óptica antes del despliegue real.

### 3.5. Interactividad con ReactFlow

El diagrama utiliza la librería **ReactFlow** que proporciona:

- **Zoom y Pan**: Navegación fluida por redes grandes
- **MiniMap**: Vista general de la topología completa
- **Controles de navegación**: Botones para ajustar la vista
- **Fondo con cuadrícula**: Facilita la alineación visual

### 3.6. Actualización Dinámica

El componente se actualiza automáticamente cuando:
- Se selecciona una nueva topología
- Cambian los datos de la red
- Se calcula un nuevo power budget

**Implementación**: Utiliza `useEffect` hooks de React para detectar cambios y reconstruir el diagrama.

---

## 4. Impacto en la Arquitectura del Sistema

### 4.1. Arquitectura de Microservicios con Docker

El diagrama de red opera dentro de una **arquitectura de microservicios** desplegada con Docker Compose:

```
┌─────────────────────────────────────────────────┐
│           Frontend (React)                       │
│  ┌──────────────────────────────────────────┐   │
│  │   NetworkDiagram Component              │   │
│  │   - ReactFlow Visualization            │   │
│  │   - State Management                    │   │
│  └──────────────────────────────────────────┘   │
└───────────────────┬─────────────────────────────┘
                    │ HTTP/REST API
┌───────────────────▼─────────────────────────────┐
│           Backend (Flask/Python)                  │
│  ┌──────────────────────────────────────────┐   │
│  │   API Endpoints                         │   │
│  │   - /topologies/{id}/power-budget      │   │
│  │   - /topologies/{id}                   │   │
│  └──────────────────────────────────────────┘   │
└───────────────────┬─────────────────────────────┘
                    │ SQL Queries
┌───────────────────▼─────────────────────────────┐
│           MySQL Database                         │
│  ┌──────────────────────────────────────────┐   │
│  │   - Topologies                           │   │
│  │   - OLTs, Splitters, ONUs                │   │
│  │   - Fibers, Power Budget Data            │   │
│  └──────────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘
```

### 4.2. Separación de Responsabilidades

**Frontend (React)**:
- **Responsabilidad**: Visualización y experiencia de usuario
- **Tecnologías**: React, ReactFlow, Material-UI
- **Funciones**: Renderizado de nodos, manejo de eventos, actualización de UI

**Backend (Flask)**:
- **Responsabilidad**: Lógica de negocio y cálculos
- **Funciones**: Cálculo de power budget, gestión de topologías, persistencia de datos
- **API REST**: Proporciona endpoints para el frontend

**Base de Datos (MySQL)**:
- **Responsabilidad**: Persistencia de datos
- **Almacena**: Topologías, elementos de red, resultados de cálculos

### 4.3. Red Docker (ftth_network)

El diagrama se beneficia de la **red bridge de Docker** (`ftth_network`):

- **Aislamiento**: Los contenedores se comunican de forma segura
- **Resolución de nombres**: El frontend puede acceder al backend mediante el nombre del servicio (`proyecto-final-backend`)
- **Escalabilidad**: Fácil agregar nuevos servicios sin afectar el diagrama

### 4.4. Flujo de Datos

1. **Usuario selecciona topología** → Frontend actualiza estado
2. **Frontend solicita datos** → API call a `/topologies/{id}`
3. **Backend consulta BD** → Retorna datos de red (OLT, Splitters, ONUs, Fibers)
4. **Frontend construye diagrama** → `buildDiagram()` genera nodos y edges
5. **Frontend solicita power budget** → API call a `/topologies/{id}/power-budget`
6. **Backend calcula power budget** → Algoritmo DBA (Dynamic Bandwidth Allocation)
7. **Frontend actualiza nodos** → `updateNodesWithPowerBudget()` muestra resultados

### 4.5. Ventajas Arquitectónicas

**Modularidad**:
- El componente `NetworkDiagram` es independiente y reutilizable
- Puede integrarse en otras aplicaciones sin modificar el backend

**Mantenibilidad**:
- Código separado por responsabilidades
- Fácil agregar nuevas topologías (solo agregar función `buildXTopology()`)

**Escalabilidad**:
- El backend puede manejar múltiples clientes simultáneos
- La base de datos puede crecer sin afectar el rendimiento del diagrama

**Testabilidad**:
- Cada componente puede probarse independientemente
- Los cálculos del backend tienen tests unitarios

---

## 5. Funciones Técnicas Clave

### 5.1. Gestión de Estado
```javascript
const [nodes, setNodes] = useNodesState([]);
const [edges, setEdges] = useEdgesState([]);
```
- Utiliza hooks de ReactFlow para manejar el estado de nodos y edges
- Actualización reactiva cuando cambian los datos

### 5.2. Posicionamiento Inteligente
- **Estrella**: Distribución circular usando trigonometría (`Math.cos`, `Math.sin`)
- **Bus**: Distribución lineal con espaciado calculado
- **Anillo**: Distribución circular con radio adaptativo según número de ONUs
- **Árbol**: Distribución jerárquica con niveles calculados

### 5.3. Mapeo de Conexiones
- Construye mapas de conexiones desde los datos de fibra óptica
- Ordena elementos según su posición en la topología
- Maneja casos especiales (splitters intermedios, conexiones múltiples)

---

## 6. Impacto en el Usuario Final

### 6.1. Visualización Intuitiva
- Los usuarios pueden **ver** la estructura de su red en lugar de solo leer datos
- Colores diferenciados facilitan la identificación de elementos

### 6.2. Validación en Tiempo Real
- El power budget se calcula y muestra automáticamente
- Indicadores visuales (verde/rojo) alertan sobre problemas de potencia

### 6.3. Análisis Comparativo
- Fácil comparar diferentes topologías visualmente
- El minimap permite navegar redes grandes eficientemente

---

## 7. Conclusiones

El **Diagrama de Red** es más que una simple visualización. Es un componente integral que:

1. **Facilita la comprensión** de topologías complejas
2. **Valida técnicamente** las redes mediante power budget
3. **Mejora la experiencia** del usuario con interactividad
4. **Se integra perfectamente** en la arquitectura de microservicios
5. **Escala eficientemente** con el crecimiento del sistema

La arquitectura Docker Compose permite que este componente funcione de manera aislada pero integrada, facilitando el desarrollo, despliegue y mantenimiento del sistema completo.

---

## Preguntas y Respuestas

*[Preparar respuestas para preguntas comunes sobre:*
- *Rendimiento con muchas ONUs*
- *Posibilidad de agregar más topologías*
- *Exportación de diagramas*
- *Integración con otras herramientas*]

---

**Gracias por su atención.**

