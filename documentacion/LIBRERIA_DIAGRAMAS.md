# Librería para Diagramas de Red

## 📚 Librería Principal: **ReactFlow**

### Información General

- **Nombre**: ReactFlow
- **Versión**: `^11.10.1`
- **Tipo**: Librería de React para visualización de grafos y diagramas de flujo
- **Sitio Web**: https://reactflow.dev/
- **Repositorio**: https://github.com/wbkd/react-flow
- **Licencia**: MIT

---

## 📦 Instalación

La librería está instalada en el proyecto mediante npm:

```json
{
  "dependencies": {
    "reactflow": "^11.10.1"
  }
}
```

**Comando de instalación:**
```bash
npm install reactflow
```

---

## 🔧 Uso en el Proyecto

### Archivo: `frontend/src/components/NetworkDiagram.js`

#### Importación:

```javascript
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  addEdge,
} from 'reactflow';
import 'reactflow/dist/style.css';
```

### Componentes Utilizados:

#### 1. **ReactFlow** (Componente Principal)
```javascript
<ReactFlow
  nodes={nodes}
  edges={edges}
  onNodesChange={onNodesChange}
  onEdgesChange={onEdgesChange}
  onConnect={onConnect}
  fitView
>
  <Background />
  <Controls />
  <MiniMap />
</ReactFlow>
```

**Props utilizadas:**
- `nodes`: Array de nodos a visualizar
- `edges`: Array de conexiones entre nodos
- `onNodesChange`: Callback cuando cambian los nodos
- `onEdgesChange`: Callback cuando cambian las conexiones
- `onConnect`: Callback cuando se conectan nodos manualmente
- `fitView`: Ajusta automáticamente la vista para mostrar todos los nodos

#### 2. **Background** (Fondo con Cuadrícula)
- Muestra una cuadrícula de fondo para facilitar la alineación visual
- Se puede personalizar con diferentes patrones

#### 3. **Controls** (Controles de Navegación)
- Botones de zoom in/out
- Botón de fit view (ajustar vista)
- Botón de pan (mover el canvas)
- Botón de lock/unlock

#### 4. **MiniMap** (Vista General)
- Muestra una vista en miniatura de todo el diagrama
- Permite navegación rápida haciendo clic en el minimap
- Útil para redes grandes

#### 5. **Hooks de ReactFlow**

**useNodesState**: Hook para manejar el estado de los nodos
```javascript
const [nodes, setNodes, onNodesChange] = useNodesState([]);
```

**useEdgesState**: Hook para manejar el estado de las conexiones
```javascript
const [edges, setEdges, onEdgesChange] = useEdgesState([]);
```

**addEdge**: Función para agregar nuevas conexiones
```javascript
const onConnect = useCallback(
  (params) => setEdges((eds) => addEdge(params, eds)),
  [setEdges]
);
```

---

## 🎨 Estructura de Nodos y Edges

### Nodos (Nodes)

Cada nodo tiene la siguiente estructura:

```javascript
{
  id: "OLT-1",                    // ID único
  type: "input",                   // Tipo: "input", "output", "default"
  position: { x: 425, y: 100 },  // Posición en el canvas
  data: {
    label: <div>OLT Principal</div>  // Contenido del nodo (JSX)
  },
  style: {
    background: '#2196F3',
    color: '#fff',
    border: '2px solid #1976D2',
    borderRadius: '10px',
    padding: '10px',
    width: 150
  }
}
```

**Tipos de nodos utilizados:**
- `input`: Para OLT (punto de entrada)
- `output`: Para ONUs (puntos de salida)
- `default`: Para Splitters (nodos intermedios)

### Edges (Conexiones)

Cada conexión tiene la siguiente estructura:

```javascript
{
  id: "e-OLT-1-SPLIT-1",          // ID único
  source: "OLT-1",                // ID del nodo origen
  target: "SPLIT-1",              // ID del nodo destino
  animated: true,                 // Animación de flujo
  style: { 
    stroke: '#FF9800',            // Color de la línea
    strokeWidth: 3                // Grosor de la línea
  }
}
```

---

## ✨ Características Utilizadas

### 1. **Animación de Flujo**
Las conexiones tienen `animated: true` para mostrar el flujo de datos:
```javascript
{
  animated: true,
  style: { stroke: '#FF9800', strokeWidth: 3 }
}
```

### 2. **Posicionamiento Dinámico**
Los nodos se posicionan usando coordenadas calculadas:
- **Estrella**: Distribución circular con trigonometría
- **Bus**: Distribución lineal con espaciado
- **Anillo**: Distribución circular con radio adaptativo
- **Árbol**: Distribución jerárquica por niveles

### 3. **Interactividad**
- **Drag & Drop**: Los nodos se pueden arrastrar
- **Zoom**: Rueda del mouse o controles
- **Pan**: Click y arrastrar el fondo
- **Selección**: Click en nodos para seleccionarlos

### 4. **Responsive**
- El diagrama se adapta al tamaño del contenedor
- `fitView` ajusta automáticamente la vista inicial

---

## 🎯 Ventajas de ReactFlow

### ✅ Para este Proyecto:

1. **Fácil de usar**: API simple y declarativa
2. **Personalizable**: Estilos y tipos de nodos personalizados
3. **Performante**: Optimizado para grandes cantidades de nodos
4. **Interactivo**: Controles y animaciones integradas
5. **React Native**: Integración perfecta con React
6. **TypeScript**: Soporte completo para TypeScript (aunque este proyecto usa JavaScript)
7. **Comunidad activa**: Mantenimiento constante y documentación completa

### 📊 Comparación con otras librerías:

| Característica | ReactFlow | D3.js | Cytoscape.js | vis.js |
|----------------|-----------|-------|--------------|--------|
| Facilidad de uso | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Integración React | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Performance | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Documentación | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Tamaño bundle | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

---

## 📚 Recursos Adicionales

### Documentación Oficial:
- **Sitio web**: https://reactflow.dev/
- **Guía de inicio**: https://reactflow.dev/learn
- **API Reference**: https://reactflow.dev/api-reference/react-flow
- **Ejemplos**: https://reactflow.dev/examples

### Ejemplos de Uso en el Proyecto:

1. **Crear nodo OLT**:
```javascript
const createOLTNode = (x, y) => {
  return {
    id: networkData.olt.id,
    type: 'input',
    position: { x, y },
    data: { label: <div><strong>{networkData.olt.name}</strong></div> },
    style: { background: '#2196F3', color: '#fff', ... }
  };
};
```

2. **Crear conexión**:
```javascript
newEdges.push({
  id: `e-${source}-${target}`,
  source: source,
  target: target,
  animated: true,
  style: { stroke: '#FF9800', strokeWidth: 3 }
});
```

3. **Actualizar nodos con datos**:
```javascript
setNodes((nds) =>
  nds.map((node) => {
    if (powerBudgetMap[node.id]) {
      return {
        ...node,
        data: {
          ...node.data,
          powerBudget: powerBudgetMap[node.id],
          label: <div>...</div>
        }
      };
    }
    return node;
  })
);
```

---

## 🔄 Versión y Actualizaciones

**Versión actual**: `^11.10.1`

**Última actualización**: La versión `^11.x` incluye:
- Mejoras de rendimiento
- Nuevos tipos de nodos
- Mejor soporte para TypeScript
- Nuevas opciones de personalización
- Mejoras en la API

**Nota**: El símbolo `^` permite actualizaciones menores automáticas (11.10.1 → 11.11.0, pero no 12.0.0)

---

## 💡 Alternativas Consideradas

Aunque ReactFlow fue la elección final, se consideraron otras opciones:

1. **D3.js**: Muy potente pero requiere más código y no está optimizado para React
2. **Cytoscape.js**: Buena opción pero más compleja de integrar
3. **vis.js**: Similar a ReactFlow pero menos mantenida
4. **react-diagrams**: Alternativa específica para React pero menos documentada

**ReactFlow fue elegida por:**
- ✅ Integración nativa con React
- ✅ API simple y declarativa
- ✅ Buen rendimiento
- ✅ Documentación excelente
- ✅ Comunidad activa

---

## 📝 Resumen

**Librería**: ReactFlow v11.10.1

**Uso principal**: Visualización interactiva de topologías de red GPON

**Componentes utilizados**:
- ReactFlow (componente principal)
- Background (cuadrícula de fondo)
- Controls (controles de navegación)
- MiniMap (vista general)

**Características destacadas**:
- Animación de flujo de datos
- Posicionamiento dinámico de nodos
- Interactividad completa (drag, zoom, pan)
- Personalización de estilos
- Integración perfecta con React


