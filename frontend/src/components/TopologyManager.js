import React, { useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Grid,
  Card,
  CardContent,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  Divider,
} from '@mui/material';
import api from '../services/api';

function TopologyManager({ topologies, onTopologyCreated, onTopologySelected, selectedTopology }) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    num_onus: 32,
    split_ratio: '1:32',
    topology_type: 'star',
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await api.post('/topologies', formData);
      if (response.data.success) {
        alert('Topología creada exitosamente');
        setFormData({
          name: '',
          description: '',
          num_onus: 32,
          split_ratio: '1:32',
          topology_type: 'star',
        });
        onTopologyCreated(response.data.data);
      }
    } catch (error) {
      console.error('Error creating topology:', error);
      alert('Error al crear topología');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Crear Nueva Topología
            </Typography>
            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
              <TextField
                fullWidth
                label="Nombre"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                margin="normal"
                required
              />
              <TextField
                fullWidth
                label="Descripción"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                margin="normal"
                multiline
                rows={3}
              />
              <FormControl fullWidth margin="normal">
                <InputLabel>Tipo de Topología</InputLabel>
                <Select
                  value={formData.topology_type}
                  onChange={(e) => setFormData({ ...formData, topology_type: e.target.value })}
                >
                  <MenuItem value="star">Estrella (Star) - GPON Estándar</MenuItem>
                  <MenuItem value="bus">Bus - Topología Lineal</MenuItem>
                  <MenuItem value="ring">Anillo (Ring) - Topología Circular</MenuItem>
                  <MenuItem value="tree">Árbol (Tree) - Topología Jerárquica</MenuItem>
                </Select>
              </FormControl>
              <TextField
                fullWidth
                type="number"
                label="Número de ONUs"
                value={formData.num_onus}
                onChange={(e) => setFormData({ ...formData, num_onus: parseInt(e.target.value) })}
                margin="normal"
                required
                inputProps={{ min: 1, max: 128 }}
              />
              {formData.topology_type === 'star' || formData.topology_type === 'tree' ? (
                <FormControl fullWidth margin="normal">
                  <InputLabel>Ratio de Splitter</InputLabel>
                  <Select
                    value={formData.split_ratio}
                    onChange={(e) => setFormData({ ...formData, split_ratio: e.target.value })}
                  >
                    <MenuItem value="1:8">1:8</MenuItem>
                    <MenuItem value="1:16">1:16</MenuItem>
                    <MenuItem value="1:32">1:32</MenuItem>
                    <MenuItem value="1:64">1:64</MenuItem>
                  </Select>
                </FormControl>
              ) : null}
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                sx={{ mt: 2 }}
                disabled={loading}
              >
                {loading ? 'Creando...' : 'Crear Topología'}
              </Button>
            </Box>
          </CardContent>
        </Card>
      </Grid>

      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Topologías Existentes
            </Typography>
            <List>
              {topologies.length === 0 ? (
                <ListItem>
                  <ListItemText primary="No hay topologías creadas" />
                </ListItem>
              ) : (
                topologies.map((topology) => (
                  <React.Fragment key={topology.id}>
                    <ListItemButton
                      selected={selectedTopology?.id === topology.id}
                      onClick={() => onTopologySelected(topology.id)}
                    >
                      <ListItemText
                        primary={topology.name}
                        secondary={`ID: ${topology.id} - Creado: ${new Date(topology.created_at).toLocaleDateString()}`}
                      />
                    </ListItemButton>
                    <Divider />
                  </React.Fragment>
                ))
              )}
            </List>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
}

export default TopologyManager;

