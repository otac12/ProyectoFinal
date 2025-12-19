import React, { useEffect, useCallback, useState } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  addEdge,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Box, Typography, Card } from '@mui/material';
import api from '../services/api';

function NetworkDiagram({ networkData, topology, onPowerBudgetLoad }) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [powerBudgetData, setPowerBudgetData] = useState([]);

  useEffect(() => {
    if (networkData) {
      buildDiagram();
    }
  }, [networkData]);

  useEffect(() => {
    if (topology && networkData) {
      loadPowerBudget();
    }
  }, [topology, networkData]);

  const loadPowerBudget = async () => {
    if (!topology?.id) return;
    try {
      const response = await api.get(`/topologies/${topology.id}/power-budget`);
      if (response.data.success) {
        // Guardar datos para mostrar en fórmulas
        setPowerBudgetData(response.data.data);
        // Notificar al componente padre
        if (onPowerBudgetLoad) {
          onPowerBudgetLoad(response.data.data);
        }
        // Actualizar nodos con información de power budget
        updateNodesWithPowerBudget(response.data.data);
      }
    } catch (error) {
      console.error('Error loading power budget:', error);
    }
  };

  const updateNodesWithPowerBudget = (powerBudgetData) => {
    const powerBudgetMap = {};
    powerBudgetData.forEach((item) => {
      powerBudgetMap[item.onu_id] = item;
    });

    setNodes((nds) =>
      nds.map((node) => {
        if (powerBudgetMap[node.id]) {
          const pb = powerBudgetMap[node.id];
          return {
            ...node,
            data: {
              ...node.data,
              powerBudget: pb,
              label: (
                <div>
                  <div>{node.data.label}</div>
                  <div style={{ fontSize: '10px', color: pb.is_valid ? 'green' : 'red' }}>
                    Power: {pb.available_power.toFixed(2)} dB
                  </div>
                </div>
              ),
            },
          };
        }
        return node;
      })
    );
  };

  const buildDiagram = () => {
    if (!networkData) return;

    const topologyType = networkData.topology_type || 'star';
    
    switch (topologyType) {
      case 'star':
        buildStarTopology();
        break;
      case 'bus':
        buildBusTopology();
        break;
      case 'ring':
        buildRingTopology();
        break;
      case 'tree':
        buildTreeTopology();
        break;
      default:
        buildStarTopology();
    }
  };

  const createOLTNode = (x, y) => {
    if (!networkData.olt) return null;
    return {
      id: networkData.olt.id,
      type: 'input',
      position: { x, y },
      data: {
        label: (
          <div>
            <strong>{networkData.olt.name}</strong>
            <div style={{ fontSize: '10px' }}>TX: {networkData.olt.tx_power} dBm</div>
          </div>
        ),
      },
      style: {
        background: '#2196F3',
        color: '#fff',
        border: '2px solid #1976D2',
        borderRadius: '10px',
        padding: '10px',
        width: 150,
      },
    };
  };

  const createSplitterNode = (splitter, x, y) => {
    return {
      id: splitter.id,
      type: 'default',
      position: { x, y },
      data: {
        label: (
          <div>
            <strong>{splitter.name}</strong>
            <div style={{ fontSize: '10px' }}>Ratio: {splitter.ratio}</div>
            <div style={{ fontSize: '10px' }}>Loss: {splitter.split_loss?.toFixed(2) || '0'} dB</div>
          </div>
        ),
      },
      style: {
        background: '#FF9800',
        color: '#fff',
        border: '2px solid #F57C00',
        borderRadius: '10px',
        padding: '10px',
        width: 140,
      },
    };
  };

  const createONUNode = (onu, x, y) => {
    return {
      id: onu.id,
      type: 'output',
      position: { x, y },
      data: {
        label: (
          <div>
            <strong>{onu.name}</strong>
            <div style={{ fontSize: '10px' }}>
              Rate: {onu.traffic_rate ? `${onu.traffic_rate.toFixed(1)} Mbps` : 'N/A'}
            </div>
          </div>
        ),
      },
      style: {
        background: '#4CAF50',
        color: '#fff',
        border: '2px solid #388E3C',
        borderRadius: '10px',
        padding: '8px',
        width: 120,
      },
    };
  };

  const buildStarTopology = () => {
    const newNodes = [];
    const newEdges = [];
    const centerX = 500;
    const centerY = 400;
    const radius = 300;

    // OLT en la parte superior
    const oltNode = createOLTNode(centerX - 75, 100);
    if (oltNode) newNodes.push(oltNode);

    // Splitter central
    const mainSplitter = networkData.splitters?.[0];
    if (mainSplitter) {
      const splitterNode = createSplitterNode(mainSplitter, centerX - 70, centerY - 50);
      newNodes.push(splitterNode);

      // Conectar OLT a Splitter
      if (networkData.olt) {
        newEdges.push({
          id: `e-${networkData.olt.id}-${mainSplitter.id}`,
          source: networkData.olt.id,
          target: mainSplitter.id,
          animated: true,
          style: { stroke: '#FF9800', strokeWidth: 3 },
        });
      }

      // ONUs distribuidas en círculo alrededor del splitter
      const onus = networkData.onus || [];
      onus.forEach((onu, idx) => {
        const angle = (idx / onus.length) * 2 * Math.PI;
        const onuX = centerX + radius * Math.cos(angle) - 60;
        const onuY = centerY + radius * Math.sin(angle) - 20;

        const onuNode = createONUNode(onu, onuX, onuY);
        newNodes.push(onuNode);

        newEdges.push({
          id: `e-${mainSplitter.id}-${onu.id}`,
          source: mainSplitter.id,
          target: onu.id,
          animated: true,
          style: { stroke: '#4CAF50', strokeWidth: 2 },
        });
      });
    }

    setNodes(newNodes);
    setEdges(newEdges);
  };

  const buildBusTopology = () => {
    const newNodes = [];
    const newEdges = [];
    const startX = 100;
    const busY = 400;
    const spacing = 250;

    // OLT a la izquierda
    const oltNode = createOLTNode(startX, busY - 50);
    if (oltNode) newNodes.push(oltNode);

    // Construir mapa de conexiones desde fibers
    const fiberMap = {};
    networkData.fibers?.forEach(fiber => {
      if (fiber.from_element && fiber.to_element) {
        if (!fiberMap[fiber.from_element]) fiberMap[fiber.from_element] = [];
        fiberMap[fiber.from_element].push(fiber.to_element);
      }
    });

    // Ordenar splitters según su conexión secuencial
    const splitters = networkData.splitters || [];
    const orderedSplitters = [];
    let currentElement = networkData.olt?.id;
    
    // Construir orden de splitters basado en conexiones
    while (currentElement && orderedSplitters.length < splitters.length) {
      const nextElements = fiberMap[currentElement] || [];
      const nextSplitter = nextElements.find(el => 
        splitters.some(s => s.id === el) && !orderedSplitters.some(s => s.id === el)
      );
      
      if (nextSplitter) {
        const splitter = splitters.find(s => s.id === nextSplitter);
        if (splitter) {
          orderedSplitters.push(splitter);
          currentElement = nextSplitter;
        } else {
          break;
        }
      } else {
        break;
      }
    }

    // Si no se puede ordenar, usar el orden original
    const finalSplitters = orderedSplitters.length > 0 ? orderedSplitters : splitters;

    // Dibujar splitters en línea
    finalSplitters.forEach((splitter, idx) => {
      const splitterX = startX + 300 + idx * spacing;
      const splitterNode = createSplitterNode(splitter, splitterX - 70, busY - 50);
      newNodes.push(splitterNode);

      // Conectar al elemento anterior
      if (idx === 0 && networkData.olt) {
        newEdges.push({
          id: `e-${networkData.olt.id}-${splitter.id}`,
          source: networkData.olt.id,
          target: splitter.id,
          animated: true,
          style: { stroke: '#FF9800', strokeWidth: 3 },
        });
      } else if (idx > 0) {
        const prevSplitter = finalSplitters[idx - 1];
        newEdges.push({
          id: `e-${prevSplitter.id}-${splitter.id}`,
          source: prevSplitter.id,
          target: splitter.id,
          animated: true,
          style: { stroke: '#FF9800', strokeWidth: 2 },
        });
      }

      // Buscar ONUs conectadas a este splitter usando fibers
      const onusForSplitter = networkData.onus?.filter(onu => 
        fiberMap[splitter.id]?.includes(onu.id)
      ) || [];

      onusForSplitter.forEach((onu, onuIdx) => {
        const onuX = splitterX;
        const onuY = busY - 150 - (onuIdx * 100);

        const onuNode = createONUNode(onu, onuX - 60, onuY);
        newNodes.push(onuNode);

        newEdges.push({
          id: `e-${splitter.id}-${onu.id}`,
          source: splitter.id,
          target: onu.id,
          animated: true,
          style: { stroke: '#4CAF50', strokeWidth: 2 },
        });
      });
    });

    setNodes(newNodes);
    setEdges(newEdges);
  };

  const buildRingTopology = () => {
    const newNodes = [];
    const newEdges = [];
    const centerX = 600;
    const centerY = 400;
    const ringRadius = Math.min(400, 50 + (networkData.onus?.length || 0) * 8);

    // OLT en el centro
    const oltNode = createOLTNode(centerX - 75, centerY - 50);
    if (oltNode) newNodes.push(oltNode);

    // Splitter principal conectado al OLT
    const mainSplitter = networkData.splitters?.find(s => s.id.includes('RING-0') || s.id.includes('ROOT')) || networkData.splitters?.[0];
    if (mainSplitter) {
      const splitterNode = createSplitterNode(mainSplitter, centerX - 70, centerY - 150);
      newNodes.push(splitterNode);

      if (networkData.olt) {
        newEdges.push({
          id: `e-${networkData.olt.id}-${mainSplitter.id}`,
          source: networkData.olt.id,
          target: mainSplitter.id,
          animated: true,
          style: { stroke: '#FF9800', strokeWidth: 3 },
        });
      }
    }

    // Construir mapa de conexiones
    const fiberMap = {};
    networkData.fibers?.forEach(fiber => {
      if (fiber.from_element && fiber.to_element) {
        if (!fiberMap[fiber.from_element]) fiberMap[fiber.from_element] = [];
        fiberMap[fiber.from_element].push({
          to: fiber.to_element,
          fiber: fiber
        });
      }
    });

    // ONUs y splitters en círculo
    const onus = networkData.onus || [];
    const ringSplitters = networkData.splitters?.filter(s => 
      s.id.includes('RING') && s.id !== mainSplitter?.id
    ) || [];

    // Ordenar splitters del anillo
    const orderedRingSplitters = [];
    let currentElement = mainSplitter?.id;
    const visited = new Set();

    // Construir orden del anillo
    while (currentElement && orderedRingSplitters.length < ringSplitters.length) {
      const connections = fiberMap[currentElement] || [];
      const nextConnection = connections.find(conn => 
        ringSplitters.some(s => s.id === conn.to) && 
        !visited.has(conn.to) &&
        !conn.to.includes('RING-0')
      );
      
      if (nextConnection) {
        const splitter = ringSplitters.find(s => s.id === nextConnection.to);
        if (splitter) {
          orderedRingSplitters.push(splitter);
          visited.add(splitter.id);
          currentElement = splitter.id;
        } else {
          break;
        }
      } else {
        break;
      }
    }

    const finalSplitters = orderedRingSplitters.length > 0 ? orderedRingSplitters : ringSplitters;

    // Distribuir splitters y ONUs en círculo
    finalSplitters.forEach((splitter, idx) => {
      const angle = (idx / finalSplitters.length) * 2 * Math.PI;
      const splitterX = centerX + (ringRadius * 0.7) * Math.cos(angle) - 70;
      const splitterY = centerY + (ringRadius * 0.7) * Math.sin(angle) - 50;
      
      const splitterNode = createSplitterNode(splitter, splitterX, splitterY);
      if (!newNodes.find(n => n.id === splitter.id)) {
        newNodes.push(splitterNode);
      }

      // Conectar splitters en anillo
      if (idx === 0 && mainSplitter) {
        newEdges.push({
          id: `e-${mainSplitter.id}-${splitter.id}`,
          source: mainSplitter.id,
          target: splitter.id,
          animated: true,
          style: { stroke: '#FF9800', strokeWidth: 2 },
        });
      }
      
      const nextIdx = (idx + 1) % finalSplitters.length;
      const nextSplitter = finalSplitters[nextIdx];
      newEdges.push({
        id: `e-${splitter.id}-${nextSplitter.id}`,
        source: splitter.id,
        target: nextSplitter.id,
        animated: true,
        style: { stroke: '#FF9800', strokeWidth: 2 },
      });

      // Buscar ONU conectada a este splitter
      const connectedOnu = networkData.onus?.find(onu => 
        fiberMap[splitter.id]?.some(conn => conn.to === onu.id)
      );

      if (connectedOnu) {
        const onuX = centerX + ringRadius * Math.cos(angle) - 60;
        const onuY = centerY + ringRadius * Math.sin(angle) - 20;
        
        const onuNode = createONUNode(connectedOnu, onuX, onuY);
        newNodes.push(onuNode);

        newEdges.push({
          id: `e-${splitter.id}-${connectedOnu.id}`,
          source: splitter.id,
          target: connectedOnu.id,
          animated: true,
          style: { stroke: '#4CAF50', strokeWidth: 2 },
        });
      }
    });

    // Agregar ONUs restantes que no estén conectadas
    onus.forEach((onu, idx) => {
      if (!newNodes.find(n => n.id === onu.id)) {
        const angle = (idx / onus.length) * 2 * Math.PI;
        const onuX = centerX + ringRadius * Math.cos(angle) - 60;
        const onuY = centerY + ringRadius * Math.sin(angle) - 20;
        
        const onuNode = createONUNode(onu, onuX, onuY);
        newNodes.push(onuNode);

        // Conectar al splitter más cercano
        if (finalSplitters.length > 0) {
          const closestSplitterIdx = Math.round((idx / onus.length) * finalSplitters.length) % finalSplitters.length;
          const closestSplitter = finalSplitters[closestSplitterIdx];
          newEdges.push({
            id: `e-${closestSplitter.id}-${onu.id}`,
            source: closestSplitter.id,
            target: onu.id,
            animated: true,
            style: { stroke: '#4CAF50', strokeWidth: 2 },
          });
        }
      }
    });

    setNodes(newNodes);
    setEdges(newEdges);
  };

  const buildTreeTopology = () => {
    const newNodes = [];
    const newEdges = [];
    const startX = 400;
    const startY = 100;
    const levelHeight = 200;
    const levelWidth = 300;

    // OLT en la parte superior
    const oltNode = createOLTNode(startX - 75, startY);
    if (oltNode) newNodes.push(oltNode);

    // Splitter raíz
    const rootSplitter = networkData.splitters?.find(s => s.id.includes('ROOT')) || networkData.splitters?.[0];
    if (rootSplitter) {
      const rootX = startX - 70;
      const rootY = startY + 150;
      const rootSplitterNode = createSplitterNode(rootSplitter, rootX, rootY);
      newNodes.push(rootSplitterNode);

      if (networkData.olt) {
        newEdges.push({
          id: `e-${networkData.olt.id}-${rootSplitter.id}`,
          source: networkData.olt.id,
          target: rootSplitter.id,
          animated: true,
          style: { stroke: '#FF9800', strokeWidth: 3 },
        });
      }

      // Splitters intermedios
      const intermediateSplitters = networkData.splitters?.filter(s => 
        s.id.includes('INTER') && s.id !== rootSplitter.id
      ) || [];
      
      intermediateSplitters.forEach((splitter, idx) => {
        const interX = startX - 400 + (idx * levelWidth);
        const interY = startY + 350;
        const interNode = createSplitterNode(splitter, interX, interY);
        newNodes.push(interNode);

        // Conectar raíz a intermedio
        newEdges.push({
          id: `e-${rootSplitter.id}-${splitter.id}`,
          source: rootSplitter.id,
          target: splitter.id,
          animated: true,
          style: { stroke: '#FF9800', strokeWidth: 2 },
        });

        // ONUs conectadas a splitters intermedios
        const onus = networkData.onus || [];
        const onusPerSplitter = Math.ceil(onus.length / intermediateSplitters.length);
        const startOnuIdx = idx * onusPerSplitter;
        
        onus.slice(startOnuIdx, startOnuIdx + onusPerSplitter).forEach((onu, onuIdx) => {
          const onuX = interX - 100 + (onuIdx % 3) * 150;
          const onuY = startY + 550 + Math.floor(onuIdx / 3) * 120;
          
          const onuNode = createONUNode(onu, onuX, onuY);
          newNodes.push(onuNode);

          newEdges.push({
            id: `e-${splitter.id}-${onu.id}`,
            source: splitter.id,
            target: onu.id,
            animated: true,
            style: { stroke: '#4CAF50', strokeWidth: 2 },
          });
        });
      });

      // Si no hay splitters intermedios, conectar ONUs directamente a la raíz
      if (intermediateSplitters.length === 0) {
        const onus = networkData.onus || [];
        onus.forEach((onu, idx) => {
          const onuX = startX - 200 + (idx % 5) * 150;
          const onuY = startY + 350 + Math.floor(idx / 5) * 120;
          
          const onuNode = createONUNode(onu, onuX, onuY);
          newNodes.push(onuNode);

          newEdges.push({
            id: `e-${rootSplitter.id}-${onu.id}`,
            source: rootSplitter.id,
            target: onu.id,
            animated: true,
            style: { stroke: '#4CAF50', strokeWidth: 2 },
          });
        });
      }
    }

    setNodes(newNodes);
    setEdges(newEdges);
  };

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  if (!networkData) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Typography variant="h6" color="textSecondary">
          No hay topología seleccionada. Crea una nueva topología en la pestaña anterior.
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ width: '100%', height: '70vh' }}>
      <Card sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6">Diagrama de Red GPON</Typography>
        <Typography variant="body2" color="textSecondary">
          {topology?.name || 'Red GPON'} - {networkData.onus?.length || 0} ONUs
          {networkData.topology_type && ` - Tipo: ${networkData.topology_type.toUpperCase()}`}
        </Typography>
      </Card>
      <div style={{ width: '100%', height: '100%', border: '1px solid #ddd', borderRadius: '4px' }}>
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
      </div>
    </Box>
  );
}

export default NetworkDiagram;

