import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Alert,
} from '@mui/material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

function ResultsPanel({ results }) {
  if (!results) {
    return (
      <Card>
        <CardContent>
          <Alert severity="info">
            No hay resultados de simulación disponibles. Ejecuta una simulación primero.
          </Alert>
        </CardContent>
      </Card>
    );
  }

  const simulationResults = results.results || {};
  const metrics = Array.isArray(simulationResults.metrics) ? simulationResults.metrics : [];

  // Preparar datos para gráficos - manejar tanto 'type' como 'metric_type'
  const throughputData = metrics
    .filter((m) => {
      const metricType = m.metric_type || m.type;
      return metricType === 'throughput';
    })
    .map((m) => {
      const value = m.metric_value !== undefined ? m.metric_value : m.value;
      return {
        name: m.onu_id || 'Unknown',
        throughput: typeof value === 'number' ? value : parseFloat(value) || 0,
      };
    })
    .filter((d) => !isNaN(d.throughput) && d.throughput >= 0)
    .sort((a, b) => a.name.localeCompare(b.name)); // Ordenar por nombre

  const packetsData = metrics
    .filter((m) => {
      const metricType = m.metric_type || m.type;
      return metricType === 'packets_sent';
    })
    .map((m) => {
      const value = m.metric_value !== undefined ? m.metric_value : m.value;
      return {
        name: m.onu_id || 'Unknown',
        packets: typeof value === 'number' ? Math.round(value) : parseInt(value) || 0,
      };
    })
    .filter((d) => !isNaN(d.packets) && d.packets >= 0)
    .sort((a, b) => a.name.localeCompare(b.name)); // Ordenar por nombre

  return (
    <Box>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Resultados de la Simulación
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Nombre: {results.name || 'N/A'}
              </Typography>
              {metrics.length > 0 && (
                <Typography variant="body2" color="textSecondary">
                  Métricas disponibles: {metrics.length} | 
                  Throughput: {throughputData.length} | 
                  Paquetes: {packetsData.length}
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Resumen General
              </Typography>
              <Typography variant="body2">
                <strong>Tiempo de simulación:</strong> {simulationResults.simulation_time || 0} s
              </Typography>
              <Typography variant="body2">
                <strong>Throughput total:</strong>{' '}
                {simulationResults.total_throughput?.toFixed(2) || 0} Mbps
              </Typography>
              <Typography variant="body2">
                <strong>Throughput promedio:</strong>{' '}
                {simulationResults.average_throughput?.toFixed(2) || 0} Mbps
              </Typography>
              <Typography variant="body2">
                <strong>Total de paquetes:</strong>{' '}
                {simulationResults.total_packets || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Throughput por ONU
              </Typography>
              {throughputData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={throughputData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="name" 
                      angle={-45} 
                      textAnchor="end" 
                      height={100}
                      interval={0}
                    />
                    <YAxis label={{ value: 'Mbps', angle: -90, position: 'insideLeft' }} />
                    <Tooltip 
                      formatter={(value) => `${value.toFixed(2)} Mbps`}
                      labelFormatter={(label) => `ONU: ${label}`}
                    />
                    <Legend />
                    <Bar dataKey="throughput" fill="#2196F3" name="Throughput (Mbps)" />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <Alert severity="warning">
                  No hay datos de throughput disponibles para mostrar
                </Alert>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Paquetes Enviados por ONU
              </Typography>
              {packetsData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={packetsData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="name" 
                      angle={-45} 
                      textAnchor="end" 
                      height={100}
                      interval={0}
                    />
                    <YAxis label={{ value: 'Paquetes', angle: -90, position: 'insideLeft' }} />
                    <Tooltip 
                      formatter={(value) => `${value} paquetes`}
                      labelFormatter={(label) => `ONU: ${label}`}
                    />
                    <Legend />
                    <Bar dataKey="packets" fill="#4CAF50" name="Paquetes Enviados" />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <Alert severity="warning">
                  No hay datos de paquetes disponibles para mostrar
                </Alert>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Tabla de Métricas Detalladas
              </Typography>
              <TableContainer component={Paper}>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>ONU</TableCell>
                      <TableCell align="right">Tipo</TableCell>
                      <TableCell align="right">Valor</TableCell>
                      <TableCell align="right">Timestamp</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {metrics.length > 0 ? (
                      metrics.slice(0, 50).map((metric, idx) => (
                        <TableRow key={idx}>
                          <TableCell>{metric.onu_id || metric.onu_id || 'N/A'}</TableCell>
                          <TableCell align="right">{metric.metric_type || metric.type || 'N/A'}</TableCell>
                          <TableCell align="right">
                            {typeof (metric.metric_value || metric.value) === 'number'
                              ? (metric.metric_value || metric.value).toFixed(2)
                              : (metric.metric_value || metric.value || 'N/A')}
                          </TableCell>
                          <TableCell align="right">
                            {metric.timestamp ? metric.timestamp.toFixed(2) : 'N/A'}
                          </TableCell>
                        </TableRow>
                      ))
                    ) : (
                      <TableRow>
                        <TableCell colSpan={4} align="center">
                          No hay métricas disponibles
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default ResultsPanel;

