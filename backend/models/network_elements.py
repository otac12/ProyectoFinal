"""
Clases para modelar elementos de la red GPON
"""

class OLT:
    """Optical Line Terminal - Terminal de línea óptica"""
    
    def __init__(self, id="OLT-1", name="OLT Principal", tx_power=2.5, rx_sensitivity=-27):
        self.id = id
        self.name = name
        self.tx_power = tx_power  # dBm
        self.rx_sensitivity = rx_sensitivity  # dBm
        self.connected_splitters = []
        self.total_capacity = 2500  # Mbps (GPON estándar)
        
    def connect_splitter(self, splitter):
        """Conectar un splitter al OLT"""
        if splitter not in self.connected_splitters:
            self.connected_splitters.append(splitter)
            splitter.connect_olt(self)
    
    def calculate_power_budget(self):
        """Calcular el power budget disponible"""
        return self.tx_power - self.rx_sensitivity
    
    def to_dict(self):
        """Convertir a diccionario para serialización"""
        return {
            "id": self.id,
            "name": self.name,
            "type": "OLT",
            "tx_power": self.tx_power,
            "rx_sensitivity": self.rx_sensitivity,
            "total_capacity": self.total_capacity,
            "connected_splitters": len(self.connected_splitters)
        }


class ONU:
    """Optical Network Unit - Unidad de red óptica"""
    
    def __init__(self, id="ONU-1", name="ONU", tx_power=1.5, rx_sensitivity=-24):
        self.id = id
        self.name = name
        self.tx_power = tx_power  # dBm
        self.rx_sensitivity = rx_sensitivity  # dBm
        self.connected_splitter = None
        self.traffic_rate = 0  # Mbps
        self.requested_bandwidth = 0  # Mbps
        
    def connect_splitter(self, splitter):
        """Conectar la ONU a un splitter"""
        self.connected_splitter = splitter
        splitter.connect_onu(self)
    
    def set_traffic_rate(self, rate):
        """Establecer tasa de tráfico"""
        self.traffic_rate = rate
        self.requested_bandwidth = rate * 1.2  # 20% overhead
    
    def to_dict(self):
        """Convertir a diccionario para serialización"""
        return {
            "id": self.id,
            "name": self.name,
            "type": "ONU",
            "tx_power": self.tx_power,
            "rx_sensitivity": self.rx_sensitivity,
            "traffic_rate": self.traffic_rate,
            "requested_bandwidth": self.requested_bandwidth,
            "splitter_id": self.connected_splitter.id if self.connected_splitter else None
        }


class Splitter:
    """Splitter óptico pasivo"""
    
    def __init__(self, id="SPLIT-1", name="Splitter", ratio="1:32"):
        self.id = id
        self.name = name
        self.ratio = ratio
        self.split_loss = self._calculate_split_loss(ratio)
        self.connected_olt = None
        self.connected_onus = []
        
    def _calculate_split_loss(self, ratio):
        """Calcular pérdida por splitting"""
        # Formato esperado: "1:32" o "1:8"
        if ":" in ratio:
            split_count = int(ratio.split(":")[1])
            # Fórmula: 10 * log10(N) donde N es el número de puertos de salida
            return 10 * __import__('math').log10(split_count)
        return 15  # Valor por defecto
    
    def connect_olt(self, olt):
        """Conectar el splitter a un OLT"""
        self.connected_olt = olt
    
    def connect_onu(self, onu):
        """Conectar una ONU al splitter"""
        if onu not in self.connected_onus:
            self.connected_onus.append(onu)
    
    def to_dict(self):
        """Convertir a diccionario para serialización"""
        return {
            "id": self.id,
            "name": self.name,
            "type": "SPLITTER",
            "ratio": self.ratio,
            "split_loss": self.split_loss,
            "olt_id": self.connected_olt.id if self.connected_olt else None,
            "connected_onus": len(self.connected_onus)
        }


class OpticalFiber:
    """Fibra óptica con propiedades de transmisión"""
    
    def __init__(self, id="FIBER-1", name="Fiber", length=5.0, 
                 attenuation=0.2, dispersion=17):
        self.id = id
        self.name = name
        self.length = length  # km
        self.attenuation = attenuation  # dB/km
        self.dispersion = dispersion  # ps/(nm·km)
        self.from_element = None
        self.to_element = None
        
    def connect(self, from_element, to_element):
        """Conectar fibra entre dos elementos"""
        self.from_element = from_element
        self.to_element = to_element
    
    def calculate_loss(self):
        """Calcular pérdida total de la fibra"""
        return self.length * self.attenuation
    
    def calculate_total_loss(self):
        """Calcular pérdida total incluyendo empalmes"""
        fiber_loss = self.calculate_loss()
        splice_loss = 0.1 * (int(self.length / 2) + 1)  # 0.1 dB por empalme cada 2 km
        return fiber_loss + splice_loss
    
    def to_dict(self):
        """Convertir a diccionario para serialización"""
        return {
            "id": self.id,
            "name": self.name,
            "type": "FIBER",
            "length": self.length,
            "attenuation": self.attenuation,
            "dispersion": self.dispersion,
            "loss": self.calculate_loss(),
            "total_loss": self.calculate_total_loss(),
            "from_element": self.from_element.id if self.from_element else None,
            "to_element": self.to_element.id if self.to_element else None
        }


class OpticalNetwork:
    """Red óptica GPON completa"""
    
    def __init__(self, name="GPON Network"):
        self.name = name
        self.olt = None
        self.splitters = []
        self.onus = []
        self.fibers = []
        
    def add_olt(self, olt):
        """Agregar OLT a la red"""
        self.olt = olt
    
    def add_splitter(self, splitter):
        """Agregar splitter a la red"""
        if splitter not in self.splitters:
            self.splitters.append(splitter)
    
    def add_onu(self, onu):
        """Agregar ONU a la red"""
        if onu not in self.onus:
            self.onus.append(onu)
    
    def add_fiber(self, fiber):
        """Agregar fibra a la red"""
        if fiber not in self.fibers:
            self.fibers.append(fiber)
    
    def create_ftth_topology(self, num_onus=32, split_ratio="1:32", topology_type="star"):
        """
        Generar topología FTTH según el tipo especificado
        
        Args:
            num_onus: Número de ONUs
            split_ratio: Ratio del splitter (para estrella)
            topology_type: Tipo de topología ('star', 'bus', 'ring', 'tree')
        """
        self.topology_type = topology_type
        
        if topology_type == "star":
            self._create_star_topology(num_onus, split_ratio)
        elif topology_type == "bus":
            self._create_bus_topology(num_onus)
        elif topology_type == "ring":
            self._create_ring_topology(num_onus)
        elif topology_type == "tree":
            self._create_tree_topology(num_onus, split_ratio)
        else:
            # Por defecto estrella
            self._create_star_topology(num_onus, split_ratio)
    
    def _create_star_topology(self, num_onus=32, split_ratio="1:32"):
        """Generar topología en estrella (GPON estándar)"""
        # Crear OLT
        self.olt = OLT(id="OLT-1", name="OLT Principal")
        
        # Crear splitter central
        splitter = Splitter(id="SPLIT-1", name=f"Splitter {split_ratio}", ratio=split_ratio)
        self.add_splitter(splitter)
        self.olt.connect_splitter(splitter)
        
        # Crear fibra OLT-Splitter
        fiber_olt_splitter = OpticalFiber(
            id="FIBER-OLT-SPLIT",
            name="OLT to Splitter",
            length=2.0
        )
        fiber_olt_splitter.connect(self.olt, splitter)
        self.add_fiber(fiber_olt_splitter)
        
        # Crear ONUs conectadas al splitter central
        for i in range(num_onus):
            onu = ONU(id=f"ONU-{i+1}", name=f"ONU {i+1}")
            self.add_onu(onu)
            splitter.connect_onu(onu)
            
            # Crear fibra Splitter-ONU
            fiber = OpticalFiber(
                id=f"FIBER-{i+1}",
                name=f"Splitter to ONU {i+1}",
                length=3.0 + (i * 0.1)  # Variar longitudes
            )
            fiber.connect(splitter, onu)
            self.add_fiber(fiber)
    
    def _create_bus_topology(self, num_onus=32):
        """Generar topología en bus - todas las ONUs conectadas a una fibra principal"""
        # Crear OLT
        self.olt = OLT(id="OLT-1", name="OLT Principal")
        
        # Crear splitters en serie a lo largo del bus
        bus_length = num_onus * 0.5  # km
        
        for i in range(num_onus):
            # Cada ONU está conectada directamente al bus principal
            onu = ONU(id=f"ONU-{i+1}", name=f"ONU {i+1}")
            self.add_onu(onu)
            
            # Crear splitter para cada ONU (tapping)
            splitter = Splitter(id=f"SPLIT-TAP-{i+1}", name=f"Tapping Splitter {i+1}", ratio="1:2")
            self.add_splitter(splitter)
            if i == 0:
                # Primer splitter conectado al OLT
                self.olt.connect_splitter(splitter)
                fiber_olt = OpticalFiber(
                    id=f"FIBER-BUS-OLT",
                    name="OLT to Bus",
                    length=1.0
                )
                fiber_olt.connect(self.olt, splitter)
                self.add_fiber(fiber_olt)
            else:
                # Conectar al splitter anterior
                prev_splitter = self.splitters[i-1]
                fiber_bus = OpticalFiber(
                    id=f"FIBER-BUS-{i}",
                    name=f"Bus Segment {i}",
                    length=0.5
                )
                fiber_bus.connect(prev_splitter, splitter)
                self.add_fiber(fiber_bus)
            
            splitter.connect_onu(onu)
            
            # Fibra del splitter a la ONU
            fiber = OpticalFiber(
                id=f"FIBER-{i+1}",
                name=f"Tapping to ONU {i+1}",
                length=0.2
            )
            fiber.connect(splitter, onu)
            self.add_fiber(fiber)
    
    def _create_ring_topology(self, num_onus=32):
        """Generar topología en anillo - ONUs conectadas en círculo"""
        # Crear OLT
        self.olt = OLT(id="OLT-1", name="OLT Principal")
        
        # Crear splitter principal conectado al OLT
        main_splitter = Splitter(id="SPLIT-RING-0", name="Ring Main Splitter", ratio="1:2")
        self.add_splitter(main_splitter)
        self.olt.connect_splitter(main_splitter)
        
        fiber_olt_ring = OpticalFiber(
            id="FIBER-OLT-RING",
            name="OLT to Ring",
            length=2.0
        )
        fiber_olt_ring.connect(self.olt, main_splitter)
        self.add_fiber(fiber_olt_ring)
        
        # Crear ONUs en anillo
        ring_radius = 5.0  # km
        for i in range(num_onus):
            onu = ONU(id=f"ONU-{i+1}", name=f"ONU {i+1}")
            self.add_onu(onu)
            
            # Crear splitter para cada ONU
            splitter = Splitter(id=f"SPLIT-RING-{i+1}", name=f"Ring Splitter {i+1}", ratio="1:2")
            self.add_splitter(splitter)
            
            # Conectar en anillo
            if i == 0:
                # Primera conexión desde el splitter principal
                fiber_ring = OpticalFiber(
                    id=f"FIBER-RING-{i}",
                    name=f"Ring Segment {i}",
                    length=ring_radius / num_onus
                )
                fiber_ring.connect(main_splitter, splitter)
                self.add_fiber(fiber_ring)
            else:
                # Conectar al splitter anterior (índice i en la lista porque ya agregamos main_splitter)
                prev_splitter = self.splitters[i]  # El splitter anterior
                fiber_ring = OpticalFiber(
                    id=f"FIBER-RING-{i}",
                    name=f"Ring Segment {i}",
                    length=ring_radius / num_onus
                )
                fiber_ring.connect(prev_splitter, splitter)
                self.add_fiber(fiber_ring)
            
            # Guardar referencia al splitter actual para el siguiente
            current_splitter = splitter
            
            # Última conexión cierra el anillo
            if i == num_onus - 1:
                fiber_close = OpticalFiber(
                    id="FIBER-RING-CLOSE",
                    name="Ring Closure",
                    length=ring_radius / num_onus
                )
                fiber_close.connect(splitter, main_splitter)
                self.add_fiber(fiber_close)
            
            splitter.connect_onu(onu)
            
            # Fibra del splitter a la ONU
            fiber = OpticalFiber(
                id=f"FIBER-RING-ONU-{i+1}",
                name=f"Ring Splitter to ONU {i+1}",
                length=0.5
            )
            fiber.connect(splitter, onu)
            self.add_fiber(fiber)
    
    def _create_tree_topology(self, num_onus=32, split_ratio="1:32"):
        """Generar topología en árbol - múltiples niveles de splitters"""
        # Crear OLT
        self.olt = OLT(id="OLT-1", name="OLT Principal")
        
        # Calcular niveles del árbol
        import math
        split_num = int(split_ratio.split(":")[1]) if ":" in split_ratio else 32
        
        if num_onus <= split_num:
            # Un solo nivel (árbol degenerado = estrella)
            self._create_star_topology(num_onus, split_ratio)
            return
        
        # Splitter raíz
        root_splitter = Splitter(id="SPLIT-ROOT", name="Root Splitter", ratio=split_ratio)
        self.add_splitter(root_splitter)
        self.olt.connect_splitter(root_splitter)
        
        fiber_root = OpticalFiber(
            id="FIBER-ROOT",
            name="OLT to Root Splitter",
            length=2.0
        )
        fiber_root.connect(self.olt, root_splitter)
        self.add_fiber(fiber_root)
        
        # Crear estructura de árbol de dos niveles para simplificar
        # Nivel 1: Splitters intermedios
        num_intermediate = min(split_num, math.ceil(num_onus / split_num))
        intermediate_splitters = []
        
        for i in range(num_intermediate):
            splitter = Splitter(
                id=f"SPLIT-INTER-{i+1}",
                name=f"Intermediate Splitter {i+1}",
                ratio=split_ratio
            )
            self.add_splitter(splitter)
            intermediate_splitters.append(splitter)
            
            fiber_inter = OpticalFiber(
                id=f"FIBER-INTER-{i+1}",
                name=f"Root to Intermediate {i+1}",
                length=2.0 + (i * 0.3)
            )
            fiber_inter.connect(root_splitter, splitter)
            self.add_fiber(fiber_inter)
        
        # Nivel 2: ONUs conectadas a splitters intermedios
        onu_counter = 0
        for inter_idx, inter_splitter in enumerate(intermediate_splitters):
            onus_per_intermediate = min(split_num, num_onus - onu_counter)
            
            for j in range(onus_per_intermediate):
                onu = ONU(id=f"ONU-{onu_counter+1}", name=f"ONU {onu_counter+1}")
                self.add_onu(onu)
                inter_splitter.connect_onu(onu)
                
                fiber_onu = OpticalFiber(
                    id=f"FIBER-TREE-{onu_counter+1}",
                    name=f"Intermediate {inter_idx+1} to ONU {onu_counter+1}",
                    length=1.5 + (j * 0.2)
                )
                fiber_onu.connect(inter_splitter, onu)
                self.add_fiber(fiber_onu)
                
                onu_counter += 1
                
                if onu_counter >= num_onus:
                    break
            
            if onu_counter >= num_onus:
                break
    
    def calculate_power_budget_path(self, onu):
        """Calcular power budget para una ruta OLT-ONU"""
        if not self.olt or not onu.connected_splitter:
            return None
        
        # Calcular power budget base
        power_budget = self.olt.calculate_power_budget()
        
        # Pérdida en splitter
        splitter_loss = onu.connected_splitter.split_loss
        split_ratio = onu.connected_splitter.ratio
        
        # Pérdidas en fibras
        fiber_losses = []
        total_fiber_loss = 0
        total_splice_loss = 0
        
        for fiber in self.fibers:
            if fiber.to_element == onu or (fiber.from_element == self.olt and fiber.to_element == onu.connected_splitter):
                fiber_attenuation = fiber.calculate_loss()
                splice_loss = 0.1 * (int(fiber.length / 2) + 1)
                total_fiber_loss += fiber_attenuation
                total_splice_loss += splice_loss
                fiber_losses.append({
                    "from": fiber.from_element.id if fiber.from_element else "N/A",
                    "to": fiber.to_element.id if fiber.to_element else "N/A",
                    "length": fiber.length,
                    "attenuation": fiber.attenuation,
                    "fiber_loss": fiber_attenuation,
                    "splice_loss": splice_loss
                })
        
        total_loss = splitter_loss + total_fiber_loss + total_splice_loss
        
        # Margen de seguridad (3 dB)
        margin = 3.0
        available_power = power_budget - total_loss - margin
        
        return {
            "power_budget": power_budget,
            "tx_power": self.olt.tx_power,
            "rx_sensitivity": self.olt.rx_sensitivity,
            "splitter_loss": splitter_loss,
            "split_ratio": split_ratio,
            "fiber_losses": fiber_losses,
            "total_fiber_loss": total_fiber_loss,
            "total_splice_loss": total_splice_loss,
            "total_loss": total_loss,
            "margin": margin,
            "available_power": available_power,
            "is_valid": available_power >= 0
        }
    
    def to_dict(self):
        """Convertir red completa a diccionario"""
        return {
            "name": self.name,
            "topology_type": getattr(self, 'topology_type', 'star'),
            "olt": self.olt.to_dict() if self.olt else None,
            "splitters": [s.to_dict() for s in self.splitters],
            "onus": [o.to_dict() for o in self.onus],
            "fibers": [f.to_dict() for f in self.fibers]
        }

