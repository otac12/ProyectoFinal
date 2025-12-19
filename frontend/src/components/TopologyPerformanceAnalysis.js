import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Paper,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Alert,
} from '@mui/material';

function TopologyPerformanceAnalysis({ networkData, powerBudgetData }) {
  if (!networkData) {
    return (
      <Card sx={{ mt: 2 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            📊 Análisis de Rendimiento por Topología
          </Typography>
          <Alert severity="info">
            Selecciona una topología para ver el análisis de rendimiento
          </Alert>
        </CardContent>
      </Card>
    );
  }

  const topologyType = networkData.topology_type || 'star';
  const onus = networkData.onus || [];
  const splitters = networkData.splitters || [];
  const fibers = networkData.fibers || [];
  const olt = networkData.olt;

  // Calcular métricas de topología
  const calculateTopologyMetrics = () => {
    let avgPathLength = 0;
    let maxPathLength = 0;
    let totalFiberLength = 0;
    let avgLatency = 0;
    let bandwidthSharingFactor = 1;

    // Calcular longitudes de fibra
    fibers.forEach(fiber => {
      totalFiberLength += fiber.length || 0;
    });

    switch (topologyType) {
      case 'star':
        // En estrella: todas las ONUs están a la misma distancia del splitter central
        // Path = OLT -> Splitter -> ONU
        avgPathLength = totalFiberLength / Math.max(onus.length, 1);
        maxPathLength = avgPathLength;
        // Latencia = distancia / velocidad de la luz en fibra (≈ 2e8 m/s = 200,000 km/s)
        avgLatency = (avgPathLength / 200000) * 1000; // ms
        // En estrella, el ancho de banda se divide equitativamente entre ONUs
        bandwidthSharingFactor = 1 / onus.length;
        break;

      case 'bus':
        // En bus: las ONUs más lejos tienen más latencia
        // La última ONU tiene el path más largo
        const busSplitters = splitters.length;
        avgPathLength = totalFiberLength / Math.max(onus.length, 1);
        maxPathLength = totalFiberLength * 0.8; // Aproximación
        // Latencia variable: la primera ONU tiene menos, la última más
        avgLatency = (avgPathLength / 200000) * 1000 * 1.5; // Factor de corrección para bus
        // En bus, el ancho de banda se comparte secuencialmente (peor eficiencia)
        bandwidthSharingFactor = 1.5 / onus.length; // Penalización por bus
        break;

      case 'ring':
        // En anillo: el path puede ir en dos direcciones (mejor latencia)
        // Pero hay overhead por el routing
        avgPathLength = (totalFiberLength / 2) / Math.max(onus.length, 1); // Path promedio es la mitad del anillo
        maxPathLength = totalFiberLength / 2; // El peor caso es la mitad del anillo
        avgLatency = (avgPathLength / 200000) * 1000 * 1.2; // Pequeño overhead por routing
        // En anillo, mejor uso del ancho de banda pero con overhead
        bandwidthSharingFactor = 1.1 / onus.length;
        break;

      case 'tree':
        // En árbol: diferentes niveles tienen diferentes latencias
        const treeLevels = Math.ceil(Math.log2(onus.length + 1));
        avgPathLength = totalFiberLength / Math.max(onus.length, 1);
        maxPathLength = avgPathLength * treeLevels * 0.6; // Las hojas más profundas
        avgLatency = (avgPathLength / 200000) * 1000 * treeLevels * 0.4;
        // En árbol, el ancho de banda se divide jerárquicamente
        bandwidthSharingFactor = 1.2 / onus.length;
        break;

      default:
        avgPathLength = totalFiberLength / Math.max(onus.length, 1);
        maxPathLength = avgPathLength;
        avgLatency = (avgPathLength / 200000) * 1000;
        bandwidthSharingFactor = 1 / onus.length;
    }

    return {
      avgPathLength: avgPathLength.toFixed(2),
      maxPathLength: maxPathLength.toFixed(2),
      totalFiberLength: totalFiberLength.toFixed(2),
      avgLatency: avgLatency.toFixed(2),
      bandwidthSharingFactor: bandwidthSharingFactor.toFixed(4),
      topologyType
    };
  };

  const metrics = calculateTopologyMetrics();
  const oltCapacity = olt?.total_capacity || 2500; // Mbps

  // Calcular capacidad efectiva por ONU
  const effectiveCapacityPerONU = (oltCapacity * parseFloat(metrics.bandwidthSharingFactor)).toFixed(2);

  return (
    <Card sx={{ mt: 2 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          📊 Análisis de Rendimiento por Topología
        </Typography>
        <Typography variant="body2" color="textSecondary" gutterBottom>
          Cómo la topología {topologyType.toUpperCase()} afecta la velocidad y latencia de la red
        </Typography>

        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid item xs={12} md={6}>
            <Paper elevation={1} sx={{ p: 2, bgcolor: '#e3f2fd' }}>
              <Typography variant="subtitle2" gutterBottom>
                <strong>Factores que Afectan la Velocidad:</strong>
              </Typography>
              <Box component="ul" sx={{ pl: 3, mt: 1 }}>
                <li><strong>Longitud de la fibra:</strong> Mayor distancia = más atenuación = menor señal</li>
                <li><strong>Número de saltos:</strong> Más elementos intermedios = más latencia</li>
                <li><strong>Compartición de ancho de banda:</strong> Más ONUs = menos ancho de banda por ONU</li>
                <li><strong>Tipo de topología:</strong> Estructura física afecta eficiencia</li>
              </Box>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper elevation={1} sx={{ p: 2, bgcolor: '#fff3e0' }}>
              <Typography variant="subtitle2" gutterBottom>
                <strong>Métricas de esta Topología:</strong>
              </Typography>
              <Box sx={{ mt: 1, fontFamily: 'monospace' }}>
                <Typography variant="body2">
                  Tipo: <strong>{topologyType.toUpperCase()}</strong>
                </Typography>
                <Typography variant="body2">
                  Longitud total de fibra: {metrics.totalFiberLength} km
                </Typography>
                <Typography variant="body2">
                  Path promedio OLT-ONU: {metrics.avgPathLength} km
                </Typography>
                <Typography variant="body2">
                  Path máximo: {metrics.maxPathLength} km
                </Typography>
                <Typography variant="body2">
                  Latencia promedio: {metrics.avgLatency} ms
                </Typography>
                <Typography variant="body2" color="primary">
                  Capacidad efectiva por ONU: ~{effectiveCapacityPerONU} Mbps
                </Typography>
              </Box>
            </Paper>
          </Grid>
        </Grid>

        <Paper elevation={1} sx={{ p: 2, mt: 2, bgcolor: '#f5f5f5' }}>
          <Typography variant="subtitle2" gutterBottom>
            <strong>Comparación de Topologías:</strong>
          </Typography>
          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell><strong>Topología</strong></TableCell>
                  <TableCell align="right"><strong>Latencia</strong></TableCell>
                  <TableCell align="right"><strong>Ancho de Banda</strong></TableCell>
                  <TableCell align="right"><strong>Escalabilidad</strong></TableCell>
                  <TableCell align="right"><strong>Redundancia</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                <TableRow sx={{ bgcolor: topologyType === 'star' ? '#e8f5e9' : 'inherit' }}>
                  <TableCell><strong>Estrella (Star)</strong></TableCell>
                  <TableCell align="right">Baja (1 salto)</TableCell>
                  <TableCell align="right">Alta (equitativa)</TableCell>
                  <TableCell align="right">Buena</TableCell>
                  <TableCell align="right">Baja</TableCell>
                </TableRow>
                <TableRow sx={{ bgcolor: topologyType === 'bus' ? '#e8f5e9' : 'inherit' }}>
                  <TableCell><strong>Bus</strong></TableCell>
                  <TableCell align="right">Variable</TableCell>
                  <TableCell align="right">Media (compartida)</TableCell>
                  <TableCell align="right">Media</TableCell>
                  <TableCell align="right">Baja</TableCell>
                </TableRow>
                <TableRow sx={{ bgcolor: topologyType === 'ring' ? '#e8f5e9' : 'inherit' }}>
                  <TableCell><strong>Anillo (Ring)</strong></TableCell>
                  <TableCell align="right">Media</TableCell>
                  <TableCell align="right">Alta (doble path)</TableCell>
                  <TableCell align="right">Buena</TableCell>
                  <TableCell align="right">Alta</TableCell>
                </TableRow>
                <TableRow sx={{ bgcolor: topologyType === 'tree' ? '#e8f5e9' : 'inherit' }}>
                  <TableCell><strong>Árbol (Tree)</strong></TableCell>
                  <TableCell align="right">Variable</TableCell>
                  <TableCell align="right">Media (jerárquica)</TableCell>
                  <TableCell align="right">Excelente</TableCell>
                  <TableCell align="right">Media</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>

        <Paper elevation={1} sx={{ p: 2, mt: 2, bgcolor: '#e8f5e9' }}>
          <Typography variant="subtitle2" gutterBottom>
            <strong>Fórmulas de Cálculo de Velocidad Efectiva:</strong>
          </Typography>
          <Box sx={{ mt: 1, fontFamily: 'monospace', fontSize: '0.9rem' }}>
            <Typography variant="body2" paragraph>
              <strong>1. Capacidad Efectiva por ONU:</strong>
            </Typography>
            <Box sx={{ pl: 2, mb: 2 }}>
              Capacidad Efectiva = Capacidad Total × Factor de Compartición
              <br />
              Capacidad Efectiva = {oltCapacity} Mbps × {metrics.bandwidthSharingFactor}
              <br />
              <Typography variant="body2" color="primary">
                Capacidad Efectiva = {effectiveCapacityPerONU} Mbps por ONU
              </Typography>
            </Box>

            <Typography variant="body2" paragraph>
              <strong>2. Latencia de Propagación:</strong>
            </Typography>
            <Box sx={{ pl: 2, mb: 2 }}>
              Latencia (ms) = (Distancia (km) / Velocidad de la luz en fibra (200,000 km/s)) × 1000
              <br />
              Latencia = ({metrics.avgPathLength} km / 200,000 km/s) × 1000
              <br />
              <Typography variant="body2" color="primary">
                Latencia ≈ {metrics.avgLatency} ms
              </Typography>
            </Box>

            <Typography variant="body2" paragraph>
              <strong>3. Throughput Real (considerando overhead):</strong>
            </Typography>
            <Box sx={{ pl: 2 }}>
              Throughput Real = Capacidad Efectiva × (1 - Overhead)
              <br />
              Donde Overhead ≈ 5-10% (encapsulación GPON, headers, etc.)
              <br />
              <Typography variant="body2" color="primary">
                Throughput Real ≈ {(parseFloat(effectiveCapacityPerONU) * 0.95).toFixed(2)} Mbps
              </Typography>
            </Box>
          </Box>
        </Paper>

        <Alert severity="info" sx={{ mt: 2 }}>
          <Typography variant="body2">
            <strong>Nota importante:</strong> La velocidad real también depende del power budget. 
            Si el power budget es insuficiente, la señal se degrada y la velocidad efectiva puede 
            reducirse significativamente debido a errores de transmisión.
          </Typography>
        </Alert>
      </CardContent>
    </Card>
  );
}

export default TopologyPerformanceAnalysis;

