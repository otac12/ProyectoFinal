"""
Algoritmo DBA (Dynamic Bandwidth Allocation) - IPACT
"""
import numpy as np


class DynamicBandwidthAllocation:
    """Asignación dinámica de ancho de banda usando IPACT"""
    
    def __init__(self, total_capacity=2500):
        self.total_capacity = total_capacity  # Mbps (GPON estándar)
    
    def allocate_bandwidth(self, onu_requests, total_capacity=None):
        """
        Asignar ancho de banda usando estrategia IPACT
        
        Args:
            onu_requests: Diccionario con requests de cada ONU {onu_id: requested_mbps}
            total_capacity: Capacidad total disponible en Mbps
        
        Returns:
            Diccionario con asignaciones {onu_id: allocated_mbps}
        """
        if total_capacity is None:
            total_capacity = self.total_capacity
        
        allocation = {}
        remaining = total_capacity
        
        # IPACT: asignar en orden de llegada (sorted by ONU ID para consistencia)
        sorted_requests = sorted(onu_requests.items())
        
        for onu_id, requested in sorted_requests:
            # Asignar mínimo entre lo solicitado y lo disponible
            granted = min(requested, remaining)
            allocation[onu_id] = {
                'requested': requested,
                'granted': granted,
                'utilization': (granted / requested * 100) if requested > 0 else 0
            }
            remaining -= granted
            
            if remaining <= 0:
                # Si no hay más capacidad, asignar 0 a las restantes
                for remaining_onu_id, _ in sorted_requests[sorted_requests.index((onu_id, requested)) + 1:]:
                    allocation[remaining_onu_id] = {
                        'requested': onu_requests[remaining_onu_id],
                        'granted': 0,
                        'utilization': 0
                    }
                break
        
        # Calcular métricas globales
        total_requested = sum(onu_requests.values())
        total_granted = sum(a['granted'] for a in allocation.values())
        global_utilization = (total_granted / total_capacity * 100) if total_capacity > 0 else 0
        
        return {
            'allocations': allocation,
            'total_requested': total_requested,
            'total_granted': total_granted,
            'total_capacity': total_capacity,
            'remaining_capacity': remaining,
            'global_utilization': global_utilization
        }
    
    def fair_allocate(self, onu_requests, total_capacity=None):
        """
        Asignación justa (Fair) - distribuir equitativamente
        """
        if total_capacity is None:
            total_capacity = self.total_capacity
        
        num_onus = len(onu_requests)
        if num_onus == 0:
            return {}
        
        fair_share = total_capacity / num_onus
        allocation = {}
        
        for onu_id, requested in onu_requests.items():
            granted = min(requested, fair_share)
            allocation[onu_id] = {
                'requested': requested,
                'granted': granted,
                'utilization': (granted / requested * 100) if requested > 0 else 0
            }
        
        return {
            'allocations': allocation,
            'total_capacity': total_capacity,
            'fair_share': fair_share
        }

