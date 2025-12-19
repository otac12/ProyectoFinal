import React, { useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Card,
  CardContent,
  Typography,
  Grid,
  Alert,
  CircularProgress,
} from '@mui/material';
import api from '../services/api';

function SimulationPanel({ topology, onSimulationComplete }) {
  const [simulationParams, setSimulationParams] = useState({
    name: 'Simulación 1',
    simulation_time: 100,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!topology) {
      setError('Por favor selecciona una topología primero');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await api.post('/simulations', {
        topology_id: topology.id,
        name: simulationParams.name,
        parameters: {
          simulation_time: parseFloat(simulationParams.simulation_time),
        },
      });

      if (response.data.success) {
        onSimulationComplete(response.data.data);
      } else {
        setError(response.data.error || 'Error en la simulación');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error al ejecutar simulación');
      console.error('Simulation error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!topology) {
    return (
      <Card>
        <CardContent>
          <Alert severity="warning">
            Por favor selecciona una topología desde la pestaña de Gestión de Topologías
          </Alert>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Ejecutar Simulación
        </Typography>
        <Typography variant="body2" color="textSecondary" gutterBottom>
          Topología seleccionada: <strong>{topology.name}</strong>
        </Typography>

        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Nombre de la Simulación"
                value={simulationParams.name}
                onChange={(e) =>
                  setSimulationParams({ ...simulationParams, name: e.target.value })
                }
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                type="number"
                label="Tiempo de Simulación (segundos)"
                value={simulationParams.simulation_time}
                onChange={(e) =>
                  setSimulationParams({
                    ...simulationParams,
                    simulation_time: e.target.value,
                  })
                }
                required
                inputProps={{ min: 1, step: 0.1 }}
                helperText="Tiempo total de simulación en segundos"
              />
            </Grid>
            <Grid item xs={12}>
              {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {error}
                </Alert>
              )}
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                size="large"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <CircularProgress size={20} sx={{ mr: 1 }} />
                    Ejecutando simulación...
                  </>
                ) : (
                  'Ejecutar Simulación'
                )}
              </Button>
            </Grid>
          </Grid>
        </Box>
      </CardContent>
    </Card>
  );
}

export default SimulationPanel;

