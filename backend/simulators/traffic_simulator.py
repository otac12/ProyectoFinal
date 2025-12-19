"""
Simulador de tráfico usando SimPy
"""
import simpy
import random
import numpy as np


class TrafficGenerator:
    """Generador de tráfico para ONUs"""
    
    def __init__(self, env, onu_id, traffic_pattern='poisson', rate=10):
        self.env = env
        self.onu_id = onu_id
        self.traffic_pattern = traffic_pattern  # 'constant', 'poisson', 'bursty'
        self.rate = rate  # Mbps
        self.packets_sent = 0
        self.bytes_sent = 0
        
    def generate_packet_size(self):
        """Generar tamaño de paquete según patrón"""
        if self.traffic_pattern == 'constant':
            return 1500  # MTU estándar
        elif self.traffic_pattern == 'poisson':
            # Distribución exponencial para tamaños
            return int(np.random.exponential(1000))
        elif self.traffic_pattern == 'bursty':
            # Modo bursty: paquetes grandes en ráfagas
            if random.random() < 0.3:
                return random.randint(1400, 1500)
            else:
                return random.randint(64, 512)
        return 1500
    
    def traffic_process(self):
        """Proceso de generación de tráfico"""
        while True:
            if self.traffic_pattern == 'constant':
                interval = 8 * self.generate_packet_size() / (self.rate * 1e6)
            elif self.traffic_pattern == 'poisson':
                interval = np.random.exponential(8 * self.generate_packet_size() / (self.rate * 1e6))
            else:  # bursty
                if random.random() < 0.2:
                    interval = 0.001  # Ráfaga corta
                else:
                    interval = np.random.exponential(8 * self.generate_packet_size() / (self.rate * 1e6))
            
            yield self.env.timeout(interval)
            
            packet_size = self.generate_packet_size()
            self.packets_sent += 1
            self.bytes_sent += packet_size


class TrafficSimulator:
    """Simulador de tráfico para red GPON"""
    
    def __init__(self, num_onus=32, simulation_time=100):
        self.num_onus = num_onus
        self.simulation_time = simulation_time
        self.env = simpy.Environment()
        self.generators = []
        
    def setup_onus(self, traffic_profiles=None):
        """Configurar generadores de tráfico para ONUs"""
        if traffic_profiles is None:
            # Perfiles por defecto: Triple Play
            traffic_profiles = []
            for i in range(self.num_onus):
                # Mezcla de servicios: video, internet, voz
                service_type = random.choice(['video', 'internet', 'voice'])
                if service_type == 'video':
                    rate = random.uniform(10, 25)  # Mbps para video
                    pattern = 'constant'
                elif service_type == 'internet':
                    rate = random.uniform(5, 15)  # Mbps para internet
                    pattern = 'poisson'
                else:  # voice
                    rate = random.uniform(0.064, 0.1)  # Mbps para voz
                    pattern = 'constant'
                
                traffic_profiles.append({
                    'onu_id': f'ONU-{i+1}',
                    'rate': rate,
                    'pattern': pattern
                })
        
        for profile in traffic_profiles:
            generator = TrafficGenerator(
                self.env,
                profile['onu_id'],
                profile['pattern'],
                profile['rate']
            )
            self.generators.append(generator)
            self.env.process(generator.traffic_process())
    
    def run(self, traffic_profiles=None):
        """Ejecutar simulación"""
        self.setup_onus(traffic_profiles)
        
        # Ejecutar simulación
        self.env.run(until=self.simulation_time)
        
        # Calcular métricas
        metrics = []
        total_throughput = 0
        total_packets = 0
        
        for generator in self.generators:
            throughput = (generator.bytes_sent * 8) / (self.simulation_time * 1e6)  # Mbps
            total_throughput += throughput
            total_packets += generator.packets_sent
            
            metrics.append({
                'onu_id': generator.onu_id,
                'type': 'throughput',
                'value': throughput,
                'timestamp': self.simulation_time
            })
            
            metrics.append({
                'onu_id': generator.onu_id,
                'type': 'packets_sent',
                'value': generator.packets_sent,
                'timestamp': self.simulation_time
            })
        
        return {
            'simulation_time': self.simulation_time,
            'total_throughput': total_throughput,
            'total_packets': total_packets,
            'average_throughput': total_throughput / self.num_onus if self.num_onus > 0 else 0,
            'metrics': metrics
        }

