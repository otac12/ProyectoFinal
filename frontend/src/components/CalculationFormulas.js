import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Box,
  Paper,
  Chip,
  Grid,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

function CalculationFormulas({ networkData, powerBudgetData }) {
  const [expanded, setExpanded] = useState('powerBudget'); // Expandir el primero por defecto

  const handleChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };

  // Calcular valores de ejemplo desde los datos
  const olt = networkData?.olt;
  const splitter = networkData?.splitters?.[0];
  const fiber = networkData?.fibers?.[0];
  const exampleOnu = powerBudgetData?.[0];

  if (!networkData) {
    return (
      <Card sx={{ mt: 2 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            📐 Fórmulas y Cálculos Ópticos
          </Typography>
          <Typography variant="body2" color="textSecondary">
            Por favor selecciona una topología para ver las fórmulas de cálculo
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card sx={{ mt: 2 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          📐 Fórmulas y Cálculos Ópticos
        </Typography>
        <Typography variant="body2" color="textSecondary" gutterBottom>
          Visualización paso a paso de los cálculos utilizados en la red GPON
        </Typography>

        {/* Power Budget */}
        <Accordion expanded={expanded === 'powerBudget'} onChange={handleChange('powerBudget')}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography variant="subtitle1">
              <strong>Power Budget (Presupuesto de Potencia Óptica)</strong>
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Box>
              <Typography variant="body2" paragraph>
                El Power Budget determina si hay suficiente potencia óptica disponible para que la señal llegue
                correctamente del OLT a la ONU.
              </Typography>

              <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: '#f5f5f5' }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>Fórmula Principal:</strong>
                </Typography>
                <Box sx={{ fontFamily: 'monospace', fontSize: '1.1rem', mb: 1 }}>
                  Power Budget = TX Power (OLT) - RX Sensitivity (OLT)
                </Box>
                {olt && (
                  <Box sx={{ mt: 1, fontFamily: 'monospace' }}>
                    <Typography variant="body2">
                      Power Budget = {olt.tx_power} dBm - ({olt.rx_sensitivity} dBm)
                    </Typography>
                    <Typography variant="body2" color="primary">
                      Power Budget = {olt.tx_power - olt.rx_sensitivity} dB
                    </Typography>
                  </Box>
                )}
              </Paper>

              <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: '#fff3e0' }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>Paso 1: Pérdida en Splitter</strong>
                </Typography>
                <Box sx={{ fontFamily: 'monospace', fontSize: '1rem', mb: 1 }}>
                  Splitter Loss = 10 × log₁₀(N)
                </Box>
                <Typography variant="body2" paragraph>
                  Donde <strong>N</strong> es el número de puertos de salida del splitter.
                </Typography>
                {splitter && (
                  <Box sx={{ mt: 1, fontFamily: 'monospace' }}>
                    <Typography variant="body2">
                      Ratio: {splitter.ratio} → N = {splitter.ratio.split(':')[1]}
                    </Typography>
                    <Typography variant="body2">
                      Splitter Loss = 10 × log₁₀({splitter.ratio.split(':')[1]})
                    </Typography>
                    <Typography variant="body2" color="primary">
                      Splitter Loss = {splitter.split_loss?.toFixed(2) || '0.00'} dB
                    </Typography>
                  </Box>
                )}
              </Paper>

              <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: '#e8f5e9' }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>Paso 2: Pérdida en Fibra Óptica</strong>
                </Typography>
                <Box sx={{ fontFamily: 'monospace', fontSize: '1rem', mb: 1 }}>
                  Fiber Loss = Length × Attenuation
                </Box>
                <Typography variant="body2" paragraph>
                  Donde:
                </Typography>
                <Box component="ul" sx={{ pl: 3, mb: 2 }}>
                  <li><strong>Length</strong>: Longitud de la fibra en kilómetros (km)</li>
                  <li><strong>Attenuation</strong>: Atenuación típica = 0.2 dB/km (SMF-28 estándar ITU-T G.652)</li>
                </Box>
                {fiber && (
                  <Box sx={{ mt: 1, fontFamily: 'monospace' }}>
                    <Typography variant="body2">
                      Fiber Loss = {fiber.length} km × {fiber.attenuation} dB/km
                    </Typography>
                    <Typography variant="body2" color="primary">
                      Fiber Loss = {(fiber.length * fiber.attenuation).toFixed(2)} dB
                    </Typography>
                  </Box>
                )}
              </Paper>

              <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: '#e3f2fd' }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>Paso 3: Pérdida Total con Empalmes</strong>
                </Typography>
                <Box sx={{ fontFamily: 'monospace', fontSize: '1rem', mb: 1 }}>
                  Total Loss = Fiber Loss + Splice Loss
                </Box>
                <Typography variant="body2" paragraph>
                  Splice Loss = 0.1 dB × (número de empalmes)
                  <br />
                  Se considera un empalme cada 2 km aproximadamente.
                </Typography>
                {fiber && (
                  <Box sx={{ mt: 1, fontFamily: 'monospace' }}>
                    <Typography variant="body2">
                      Número de empalmes = ⌊{fiber.length} / 2⌋ + 1 = {Math.floor(fiber.length / 2) + 1}
                    </Typography>
                    <Typography variant="body2">
                      Splice Loss = 0.1 dB × {Math.floor(fiber.length / 2) + 1} = {(0.1 * (Math.floor(fiber.length / 2) + 1)).toFixed(2)} dB
                    </Typography>
                    <Typography variant="body2">
                      Total Loss = {(fiber.length * fiber.attenuation).toFixed(2)} + {(0.1 * (Math.floor(fiber.length / 2) + 1)).toFixed(2)}
                    </Typography>
                    <Typography variant="body2" color="primary">
                      Total Loss = {(fiber.length * fiber.attenuation + 0.1 * (Math.floor(fiber.length / 2) + 1)).toFixed(2)} dB
                    </Typography>
                  </Box>
                )}
              </Paper>

              <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: '#fce4ec' }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>Paso 4: Potencia Disponible</strong>
                </Typography>
                <Box sx={{ fontFamily: 'monospace', fontSize: '1rem', mb: 1 }}>
                  Available Power = Power Budget - Total Loss - Safety Margin
                </Box>
                <Typography variant="body2" paragraph>
                  El <strong>Safety Margin</strong> es de 3 dB (margen de seguridad recomendado por ITU-T).
                </Typography>
                {exampleOnu && olt && (
                  <Box sx={{ mt: 1, fontFamily: 'monospace' }}>
                    <Typography variant="body2">
                      Available Power = {olt.tx_power - olt.rx_sensitivity} dB - {exampleOnu.total_loss?.toFixed(2) || '0.00'} dB - 3 dB
                    </Typography>
                    <Typography variant="body2" color={exampleOnu.is_valid ? 'success.main' : 'error.main'}>
                      Available Power = {exampleOnu.available_power?.toFixed(2) || '0.00'} dB
                    </Typography>
                    <Chip
                      label={exampleOnu.is_valid ? '✓ Válido (≥ 0 dB)' : '✗ Inválido (< 0 dB)'}
                      color={exampleOnu.is_valid ? 'success' : 'error'}
                      size="small"
                      sx={{ mt: 1 }}
                    />
                  </Box>
                )}
              </Paper>

              <Box sx={{ mt: 2, p: 2, bgcolor: '#fff9c4', borderRadius: 1 }}>
                <Typography variant="caption" display="block">
                  <strong>Nota:</strong> Para que la conexión sea válida, el Available Power debe ser ≥ 0 dB.
                  Según ITU-T G.984, el power budget máximo para GPON clase B+ es de 28 dB.
                </Typography>
              </Box>
            </Box>
          </AccordionDetails>
        </Accordion>

        {/* DBA Algorithm */}
        <Accordion expanded={expanded === 'dba'} onChange={handleChange('dba')}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography variant="subtitle1">
              <strong>DBA - Dynamic Bandwidth Allocation (IPACT)</strong>
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Box>
              <Typography variant="body2" paragraph>
                El algoritmo IPACT (Interleaved Polling with Adaptive Cycle Time) asigna ancho de banda dinámicamente
                a cada ONU según sus necesidades.
              </Typography>

              <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: '#f5f5f5' }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>Fórmula de Asignación:</strong>
                </Typography>
                <Box sx={{ fontFamily: 'monospace', fontSize: '1rem', mb: 1 }}>
                  Granted = min(Requested, Remaining Capacity)
                </Box>
                <Typography variant="body2" paragraph>
                  El algoritmo IPACT asigna en orden de llegada (FIFO), asignando a cada ONU el mínimo entre
                  lo que solicita y lo que queda disponible.
                </Typography>
              </Paper>

              <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: '#e8f5e9' }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>Utilización:</strong>
                </Typography>
                <Box sx={{ fontFamily: 'monospace', fontSize: '1rem', mb: 1 }}>
                  Utilization (%) = (Granted / Requested) × 100
                </Box>
                <Typography variant="body2" paragraph>
                  Indica qué porcentaje de la capacidad solicitada se otorgó a la ONU.
                </Typography>
              </Paper>

              <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: '#fff3e0' }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>Capacidad Total GPON:</strong>
                </Typography>
                <Box sx={{ fontFamily: 'monospace', fontSize: '1rem' }}>
                  Total Capacity = 2500 Mbps (GPON estándar)
                  <br />
                  Downstream: 2.5 Gbps
                  <br />
                  Upstream: 1.25 Gbps (compartido)
                </Box>
              </Paper>
            </Box>
          </AccordionDetails>
        </Accordion>

        {/* Throughput Calculation */}
        <Accordion expanded={expanded === 'throughput'} onChange={handleChange('throughput')}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography variant="subtitle1">
              <strong>Cálculo de Throughput</strong>
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Box>
              <Typography variant="body2" paragraph>
                El throughput se calcula dividiendo los bits enviados entre el tiempo de simulación.
              </Typography>

              <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: '#f5f5f5' }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>Fórmula:</strong>
                </Typography>
                <Box sx={{ fontFamily: 'monospace', fontSize: '1rem', mb: 1 }}>
                  Throughput (Mbps) = (Bytes Sent × 8) / (Simulation Time × 10⁶)
                </Box>
                <Typography variant="body2" paragraph>
                  Donde:
                </Typography>
                <Box component="ul" sx={{ pl: 3, mb: 2 }}>
                  <li><strong>Bytes Sent</strong>: Total de bytes enviados por la ONU</li>
                  <li><strong>8</strong>: Factor de conversión de bytes a bits</li>
                  <li><strong>Simulation Time</strong>: Tiempo de simulación en segundos</li>
                  <li><strong>10⁶</strong>: Factor de conversión de bits a Megabits</li>
                </Box>
                <Box sx={{ mt: 1, fontFamily: 'monospace', fontSize: '0.9rem' }}>
                  <Typography variant="body2">
                    Ejemplo: Si una ONU envió 1,250,000 bytes en 100 segundos:
                  </Typography>
                  <Typography variant="body2">
                    Throughput = (1,250,000 × 8) / (100 × 1,000,000)
                  </Typography>
                  <Typography variant="body2" color="primary">
                    Throughput = 10,000,000 / 100,000,000 = 0.1 Mbps
                  </Typography>
                </Box>
              </Paper>
            </Box>
          </AccordionDetails>
        </Accordion>

        {/* Topology Impact on Speed */}
        <Accordion expanded={expanded === 'topology'} onChange={handleChange('topology')}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography variant="subtitle1">
              <strong>Influencia de la Topología en la Velocidad</strong>
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Box>
              <Typography variant="body2" paragraph>
                La topología de la red afecta directamente la velocidad y latencia porque determina:
                la distancia física, el número de saltos, y cómo se comparte el ancho de banda.
              </Typography>

              <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: '#e3f2fd' }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>1. Distancia y Atenuación:</strong>
                </Typography>
                <Typography variant="body2" paragraph>
                  A mayor distancia = mayor atenuación = señal más débil = velocidad reducida
                </Typography>
                <Box sx={{ fontFamily: 'monospace', fontSize: '0.9rem' }}>
                  Velocidad efectiva ∝ 1 / (Distancia × Atenuación)
                </Box>
              </Paper>

              <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: '#fff3e0' }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>2. Latencia de Propagación:</strong>
                </Typography>
                <Box sx={{ fontFamily: 'monospace', fontSize: '1rem', mb: 1 }}>
                  Latencia (ms) = (Distancia (km) / 200,000 km/s) × 1000
                </Box>
                <Typography variant="body2" paragraph>
                  En fibra óptica, la velocidad de propagación es aproximadamente 2/3 de la velocidad 
                  de la luz en el vacío (200,000 km/s).
                </Typography>
                <Box component="ul" sx={{ pl: 3, mb: 2 }}>
                  <li><strong>Estrella:</strong> Latencia uniforme y baja (1 salto desde splitter)</li>
                  <li><strong>Bus:</strong> Latencia variable (últimas ONUs tienen más latencia)</li>
                  <li><strong>Anillo:</strong> Latencia moderada (path promedio = mitad del anillo)</li>
                  <li><strong>Árbol:</strong> Latencia variable según nivel jerárquico</li>
                </Box>
              </Paper>

              <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: '#e8f5e9' }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>3. Compartición de Ancho de Banda:</strong>
                </Typography>
                <Box sx={{ fontFamily: 'monospace', fontSize: '1rem', mb: 1 }}>
                  Ancho de Banda por ONU = Capacidad Total × Factor de Compartición
                </Box>
                <Typography variant="body2" paragraph>
                  Diferentes topologías comparten el ancho de banda de manera distinta:
                </Typography>
                <Box component="ul" sx={{ pl: 3, mb: 2 }}>
                  <li><strong>Estrella:</strong> División equitativa (Factor = 1/N)</li>
                  <li><strong>Bus:</strong> Compartición secuencial con penalización (Factor ≈ 1.5/N)</li>
                  <li><strong>Anillo:</strong> Mejor uso del ancho de banda (Factor ≈ 1.1/N)</li>
                  <li><strong>Árbol:</strong> División jerárquica (Factor ≈ 1.2/N)</li>
                </Box>
                {networkData?.olt && (
                  <Box sx={{ mt: 1, fontFamily: 'monospace' }}>
                    <Typography variant="body2">
                      Capacidad Total GPON: {networkData.olt.total_capacity} Mbps
                    </Typography>
                    <Typography variant="body2">
                      Número de ONUs: {networkData.onus?.length || 0}
                    </Typography>
                    <Typography variant="body2" color="primary">
                      Ancho de banda aproximado por ONU: ~{Math.round((networkData.olt.total_capacity / (networkData.onus?.length || 1)))} Mbps
                    </Typography>
                  </Box>
                )}
              </Paper>

              <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: '#fce4ec' }}>
                <Typography variant="subtitle2" gutterBottom>
                  <strong>4. Relación Power Budget ↔ Velocidad:</strong>
                </Typography>
                <Typography variant="body2" paragraph>
                  Si el power budget es insuficiente (Available Power &lt; 0 dB), la señal se degrada:
                </Typography>
                <Box component="ul" sx={{ pl: 3, mb: 2 }}>
                  <li>Mayor tasa de errores (BER - Bit Error Rate)</li>
                  <li>Retransmisiones necesarias</li>
                  <li>Reducción del throughput efectivo</li>
                  <li>Posible pérdida de conectividad</li>
                </Box>
                <Box sx={{ fontFamily: 'monospace', fontSize: '0.9rem' }}>
                  Throughput Efectivo = Throughput Ideal × (1 - BER) × (1 - Overhead)
                </Box>
              </Paper>

              <Box sx={{ mt: 2, p: 2, bgcolor: '#fff9c4', borderRadius: 1 }}>
                <Typography variant="caption" display="block">
                  <strong>Resumen:</strong> La topología en <strong>Estrella</strong> generalmente ofrece 
                  el mejor rendimiento para GPON debido a su latencia uniforme y distribución equitativa 
                  del ancho de banda. Las otras topologías tienen diferentes trade-offs entre escalabilidad, 
                  redundancia y rendimiento.
                </Typography>
              </Box>
            </Box>
          </AccordionDetails>
        </Accordion>

        {/* Optical Loss Summary */}
        <Accordion expanded={expanded === 'losses'} onChange={handleChange('losses')}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography variant="subtitle1">
              <strong>Resumen de Pérdidas Ópticas</strong>
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Box>
              <Typography variant="body2" paragraph>
                Las pérdidas ópticas en una red GPON provienen de varios componentes:
              </Typography>

              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Paper elevation={1} sx={{ p: 2, bgcolor: '#fff3e0' }}>
                    <Typography variant="subtitle2" gutterBottom>
                      <strong>1. Pérdida en Splitter</strong>
                    </Typography>
                    <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                      10 × log₁₀(N) dB
                    </Typography>
                    <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                      Ejemplos comunes:
                    </Typography>
                    <Box component="ul" sx={{ margin: '8px 0', paddingLeft: '20px', fontSize: '0.75rem' }}>
                      <li>1:8 → 9.03 dB</li>
                      <li>1:16 → 12.04 dB</li>
                      <li>1:32 → 15.05 dB</li>
                      <li>1:64 → 18.06 dB</li>
                    </Box>
                  </Paper>
                </Grid>

                <Grid item xs={12} md={6}>
                  <Paper elevation={1} sx={{ p: 2, bgcolor: '#e8f5e9' }}>
                    <Typography variant="subtitle2" gutterBottom>
                      <strong>2. Pérdida en Fibra</strong>
                    </Typography>
                    <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                      Length × 0.2 dB/km
                    </Typography>
                    <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                      Ejemplo:
                      <br />
                      5 km × 0.2 dB/km = 1.0 dB
                    </Typography>
                  </Paper>
                </Grid>

                <Grid item xs={12} md={6}>
                  <Paper elevation={1} sx={{ p: 2, bgcolor: '#e3f2fd' }}>
                    <Typography variant="subtitle2" gutterBottom>
                      <strong>3. Pérdida en Empalmes</strong>
                    </Typography>
                    <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                      0.1 dB × número_empalmes
                    </Typography>
                    <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                      Típicamente: 0.1 dB cada 2 km
                    </Typography>
                  </Paper>
                </Grid>

                <Grid item xs={12} md={6}>
                  <Paper elevation={1} sx={{ p: 2, bgcolor: '#fce4ec' }}>
                    <Typography variant="subtitle2" gutterBottom>
                      <strong>4. Margen de Seguridad</strong>
                    </Typography>
                    <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                      3.0 dB
                    </Typography>
                    <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                      Recomendado por ITU-T para compensar variaciones y envejecimiento
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </Box>
          </AccordionDetails>
        </Accordion>
      </CardContent>
    </Card>
  );
}

export default CalculationFormulas;

