import React, { useState, useEffect } from 'react';
import { Container, AppBar, Toolbar, Typography, Tabs, Tab, Box } from '@mui/material';
import NetworkDiagram from './components/NetworkDiagram';
import TopologyManager from './components/TopologyManager';
import SimulationPanel from './components/SimulationPanel';
import ResultsPanel from './components/ResultsPanel';
import CalculationFormulas from './components/CalculationFormulas';
import TopologyPerformanceAnalysis from './components/TopologyPerformanceAnalysis';
import api from './services/api';
import './App.css';

function TabPanel({ children, value, index }) {
  return (
    <div role="tabpanel" hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

function App() {
  const [tabValue, setTabValue] = useState(0);
  const [topologies, setTopologies] = useState([]);
  const [selectedTopology, setSelectedTopology] = useState(null);
  const [networkData, setNetworkData] = useState(null);
  const [simulationResults, setSimulationResults] = useState(null);
  const [powerBudgetData, setPowerBudgetData] = useState([]);

  useEffect(() => {
    loadTopologies();
  }, []);

  const loadTopologies = async () => {
    try {
      const response = await api.get('/topologies');
      if (response.data.success) {
        setTopologies(response.data.data);
      }
    } catch (error) {
      console.error('Error loading topologies:', error);
    }
  };

  const handleTopologyCreated = async (topologyData) => {
    await loadTopologies();
    if (topologyData.id) {
      const response = await api.get(`/topologies/${topologyData.id}`);
      if (response.data.success) {
        setSelectedTopology(response.data.data);
        setNetworkData(response.data.data.network);
        // Cargar power budget
        try {
          const pbResponse = await api.get(`/topologies/${topologyData.id}/power-budget`);
          if (pbResponse.data.success) {
            setPowerBudgetData(pbResponse.data.data);
          }
        } catch (pbError) {
          console.error('Error loading power budget:', pbError);
        }
        setTabValue(1); // Cambiar a pestaña de diagrama
      }
    }
  };

  const handleTopologySelected = async (topologyId) => {
    try {
      const response = await api.get(`/topologies/${topologyId}`);
      if (response.data.success) {
        setSelectedTopology(response.data.data);
        setNetworkData(response.data.data.network);
        // Cargar power budget
        try {
          const pbResponse = await api.get(`/topologies/${topologyId}/power-budget`);
          if (pbResponse.data.success) {
            setPowerBudgetData(pbResponse.data.data);
          }
        } catch (pbError) {
          console.error('Error loading power budget:', pbError);
        }
      }
    } catch (error) {
      console.error('Error loading topology:', error);
    }
  };

  const handleSimulationComplete = (results) => {
    setSimulationResults(results);
    setTabValue(4); // Cambiar a pestaña de resultados
  };

  return (
    <div className="App">
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Simulador de Red FTTH GPON
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 2, mb: 2 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
            <Tab label="Gestión de Topologías" />
            <Tab label="Diagrama de Red" />
            <Tab label="Fórmulas y Cálculos" />
            <Tab label="Simulación" />
            <Tab label="Resultados" />
          </Tabs>
        </Box>

        <TabPanel value={tabValue} index={0}>
          <TopologyManager
            topologies={topologies}
            onTopologyCreated={handleTopologyCreated}
            onTopologySelected={handleTopologySelected}
            selectedTopology={selectedTopology}
          />
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <NetworkDiagram
            networkData={networkData}
            topology={selectedTopology}
            onPowerBudgetLoad={setPowerBudgetData}
          />
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <CalculationFormulas 
            networkData={networkData} 
            powerBudgetData={powerBudgetData} 
          />
          <TopologyPerformanceAnalysis 
            networkData={networkData} 
            powerBudgetData={powerBudgetData} 
          />
        </TabPanel>

        <TabPanel value={tabValue} index={3}>
          <SimulationPanel
            topology={selectedTopology}
            onSimulationComplete={handleSimulationComplete}
          />
        </TabPanel>

        <TabPanel value={tabValue} index={4}>
          <ResultsPanel results={simulationResults} />
        </TabPanel>
      </Container>
    </div>
  );
}

export default App;

