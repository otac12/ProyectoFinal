"""
Tests para la clase OpticalNetwork
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.network_elements import OpticalNetwork


def test_network_initialization():
    """Test de inicialización básica de la red óptica"""
    print("\n=== TEST: Inicialización básica OpticalNetwork ===")
    print("ENTRADA: Crear OpticalNetwork con valores por defecto")
    
    network = OpticalNetwork()
    
    print("\nDATOS DE SALIDA:")
    print(f"  - Nombre: {network.name}")
    print(f"  - OLT: {network.olt.id if network.olt else 'None'}")
    print(f"  - Splitters: {len(network.splitters)}")
    print(f"  - ONUs: {len(network.onus)}")
    print(f"  - Fibers: {len(network.fibers)}")
    
    # Verificaciones
    assert network.name == "GPON Network", f"Error: Nombre esperado 'GPON Network', obtenido '{network.name}'"
    assert network.olt is None, "Error: OLT debería ser None"
    assert len(network.splitters) == 0, f"Error: Splitters debería estar vacío, tiene {len(network.splitters)} elementos"
    assert len(network.onus) == 0, f"Error: ONUs debería estar vacío, tiene {len(network.onus)} elementos"
    assert len(network.fibers) == 0, f"Error: Fibers debería estar vacío, tiene {len(network.fibers)} elementos"
    
    print("\n✓ VERIFICACIÓN: Todos los valores por defecto son correctos")
    print("✓ TEST PASADO: OpticalNetwork initialization OK\n")


def test_network_custom_initialization():
    """Test de inicialización con nombre personalizado"""
    print("\n=== TEST: Inicialización OpticalNetwork con nombre personalizado ===")
    print("ENTRADA:")
    print("  - name='Test Network'")
    
    network = OpticalNetwork(name="Test Network")
    
    print("\nDATOS DE SALIDA:")
    print(f"  - Nombre: {network.name}")
    
    # Verificaciones
    assert network.name == "Test Network", f"Error: Nombre esperado 'Test Network', obtenido '{network.name}'"
    
    print("\n✓ VERIFICACIÓN: Nombre personalizado correcto")
    print("✓ TEST PASADO: OpticalNetwork custom initialization OK\n")


def test_network_create_star_topology():
    """Test de creación de topología en estrella"""
    print("\n=== TEST: Creación de topología en estrella ===")
    print("ENTRADA:")
    print("  - name='Star Network'")
    print("  - num_onus=4")
    print("  - split_ratio='1:8'")
    
    network = OpticalNetwork("Star Network")
    print(f"\nPASO 1: Crear red (nombre: {network.name})")
    
    network.create_ftth_topology(num_onus=4, split_ratio="1:8")
    print(f"PASO 2: Crear topología en estrella con {4} ONUs y ratio {1:8}")
    
    print("\nDATOS DE SALIDA:")
    print(f"  - OLT creado: {'Sí' if network.olt else 'No'} (ID: {network.olt.id if network.olt else 'N/A'})")
    print(f"  - Splitters: {len(network.splitters)} (Ratio: {network.splitters[0].ratio if network.splitters else 'N/A'})")
    print(f"  - ONUs: {len(network.onus)}")
    print(f"  - Fibers: {len(network.fibers)}")
    
    # Verificaciones
    assert network.olt is not None, "Error: OLT no fue creado"
    assert len(network.splitters) == 1, f"Error: Debería haber 1 splitter, hay {len(network.splitters)}"
    assert len(network.onus) == 4, f"Error: Deberían haber 4 ONUs, hay {len(network.onus)}"
    assert len(network.fibers) >= 4, f"Error: Deberían haber al menos 4 fibras, hay {len(network.fibers)}"
    assert network.olt.id == "OLT-1", f"Error: OLT ID esperado 'OLT-1', obtenido '{network.olt.id}'"
    assert network.splitters[0].ratio == "1:8", f"Error: Ratio esperado '1:8', obtenido '{network.splitters[0].ratio}'"
    
    print("\n✓ VERIFICACIÓN: Topología en estrella creada correctamente")
    print("✓ TEST PASADO: OpticalNetwork create_star_topology OK\n")


def test_network_create_star_topology_32_onus():
    """Test de creación de topología en estrella con 32 ONUs"""
    print("\n=== TEST: Creación de topología en estrella con 32 ONUs ===")
    print("ENTRADA:")
    print("  - num_onus=32")
    print("  - split_ratio='1:32'")
    
    network = OpticalNetwork()
    print(f"\nPASO 1: Crear red")
    print(f"PASO 2: Crear topología con 32 ONUs y ratio 1:32")
    
    network.create_ftth_topology(num_onus=32, split_ratio="1:32")
    
    print("\nDATOS DE SALIDA:")
    print(f"  - ONUs creadas: {len(network.onus)}")
    print(f"  - Splitter ratio: {network.splitters[0].ratio if network.splitters else 'N/A'}")
    print(f"  - ONUs conectadas al splitter: {len(network.splitters[0].connected_onus) if network.splitters else 0}")
    
    # Verificaciones
    assert len(network.onus) == 32, f"Error: Deberían haber 32 ONUs, hay {len(network.onus)}"
    assert network.splitters[0].ratio == "1:32", f"Error: Ratio esperado '1:32', obtenido '{network.splitters[0].ratio}'"
    assert len(network.splitters[0].connected_onus) == 32, f"Error: Deberían haber 32 ONUs conectadas, hay {len(network.splitters[0].connected_onus)}"
    
    print("\n✓ VERIFICACIÓN: 32 ONUs creadas y conectadas correctamente")
    print("✓ TEST PASADO: OpticalNetwork create_star_topology 32 ONUs OK\n")


def test_network_connections():
    """Test de que las conexiones se establecen correctamente"""
    print("\n=== TEST: Verificación de conexiones en la red ===")
    print("ENTRADA:")
    print("  - Crear topología con 2 ONUs y ratio 1:8")
    
    network = OpticalNetwork()
    network.create_ftth_topology(num_onus=2, split_ratio="1:8")
    
    print(f"\nPASO 1: Crear topología (2 ONUs)")
    print(f"PASO 2: Verificar conexiones OLT-Splitter-ONU")
    
    print("\nDATOS DE SALIDA:")
    print(f"  - OLT.connected_splitters: {len(network.olt.connected_splitters)}")
    print(f"  - Splitter.connected_olt: {network.splitters[0].connected_olt.id if network.splitters[0].connected_olt else 'None'}")
    print(f"  - Splitter.connected_onus: {len(network.splitters[0].connected_onus)}")
    print(f"  - ONU[0].connected_splitter: {network.onus[0].connected_splitter.id if network.onus[0].connected_splitter else 'None'}")
    print(f"  - ONU[1].connected_splitter: {network.onus[1].connected_splitter.id if network.onus[1].connected_splitter else 'None'}")
    
    # Verificaciones
    assert len(network.olt.connected_splitters) == 1, f"Error: OLT debería tener 1 splitter conectado, tiene {len(network.olt.connected_splitters)}"
    assert network.splitters[0].connected_olt == network.olt, "Error: Splitter no está conectado al OLT"
    assert len(network.splitters[0].connected_onus) == 2, f"Error: Splitter debería tener 2 ONUs, tiene {len(network.splitters[0].connected_onus)}"
    for onu in network.onus:
        assert onu.connected_splitter == network.splitters[0], f"Error: ONU {onu.id} no está conectada al splitter"
    
    print("\n✓ VERIFICACIÓN: Todas las conexiones establecidas correctamente")
    print("✓ TEST PASADO: OpticalNetwork connections OK\n")


def test_network_power_budget_calculation():
    """Test del cálculo de power budget"""
    print("\n=== TEST: Cálculo de power budget para ruta OLT-ONU ===")
    print("ENTRADA:")
    print("  - Crear topología con 2 ONUs")
    print("  - Calcular power budget para primera ONU")
    
    network = OpticalNetwork()
    network.create_ftth_topology(num_onus=2, split_ratio="1:8")
    
    print(f"\nPASO 1: Crear topología con 2 ONUs")
    print(f"PASO 2: Calcular power budget para ONU {network.onus[0].id}")
    
    power_budget = network.calculate_power_budget_path(network.onus[0])
    
    print("\nDATOS DE SALIDA:")
    if power_budget:
        print(f"  - Power Budget total: {power_budget['power_budget']:.2f} dB")
        print(f"  - Pérdida total: {power_budget['total_loss']:.2f} dB")
        print(f"  - Potencia disponible: {power_budget['available_power']:.2f} dB")
        print(f"  - Es válido: {'Sí' if power_budget['is_valid'] else 'No'}")
    else:
        print("  - Power budget: None")
    
    # Verificaciones
    assert power_budget is not None, "Error: Power budget no debería ser None"
    assert 'power_budget' in power_budget, "Error: 'power_budget' no está en el resultado"
    assert 'total_loss' in power_budget, "Error: 'total_loss' no está en el resultado"
    assert 'available_power' in power_budget, "Error: 'available_power' no está en el resultado"
    assert 'is_valid' in power_budget, "Error: 'is_valid' no está en el resultado"
    assert power_budget['power_budget'] > 0, f"Error: Power budget debería ser positivo, obtenido {power_budget['power_budget']}"
    
    print("\n✓ VERIFICACIÓN: Power budget calculado correctamente")
    print("✓ TEST PASADO: OpticalNetwork power_budget calculation OK\n")


def test_network_to_dict():
    """Test de conversión a diccionario"""
    print("\n=== TEST: Conversión OpticalNetwork a diccionario ===")
    print("ENTRADA:")
    print("  - name='Test Network'")
    print("  - Crear topología con 2 ONUs")
    print("  - Convertir a diccionario")
    
    network = OpticalNetwork("Test Network")
    network.create_ftth_topology(num_onus=2, split_ratio="1:8")
    
    print(f"\nPASO 1: Crear red y topología")
    print(f"PASO 2: Convertir a diccionario usando to_dict()")
    
    network_dict = network.to_dict()
    
    print("\nDATOS DE SALIDA (resumen del diccionario):")
    print(f"  - name: {network_dict['name']}")
    print(f"  - topology_type: {network_dict['topology_type']}")
    print(f"  - OLT: {'Presente' if network_dict['olt'] else 'None'}")
    print(f"  - ONUs: {len(network_dict['onus'])}")
    print(f"  - Splitters: {len(network_dict['splitters'])}")
    print(f"  - Fibers: {len(network_dict['fibers'])}")
    
    # Verificaciones
    assert network_dict['name'] == "Test Network", f"Error: Nombre esperado 'Test Network', obtenido '{network_dict['name']}'"
    assert network_dict['topology_type'] == "star", f"Error: Tipo esperado 'star', obtenido '{network_dict['topology_type']}'"
    assert network_dict['olt'] is not None, "Error: OLT debería estar en el diccionario"
    assert len(network_dict['onus']) == 2, f"Error: Deberían haber 2 ONUs, hay {len(network_dict['onus'])}"
    assert len(network_dict['splitters']) == 1, f"Error: Debería haber 1 splitter, hay {len(network_dict['splitters'])}"
    assert len(network_dict['fibers']) > 0, f"Error: Deberían haber fibras, hay {len(network_dict['fibers'])}"
    
    print("\n✓ VERIFICACIÓN: Diccionario contiene toda la información de la red")
    print("✓ TEST PASADO: OpticalNetwork to_dict OK\n")


def test_network_add_elements():
    """Test de agregar elementos manualmente"""
    print("\n=== TEST: Agregar elementos manualmente a la red ===")
    print("ENTRADA:")
    print("  - Crear elementos individuales (OLT, ONU, Splitter, Fiber)")
    print("  - Agregarlos a la red manualmente")
    
    from models.network_elements import OLT, ONU, Splitter, OpticalFiber
    
    network = OpticalNetwork()
    olt = OLT(id="OLT-TEST")
    onu = ONU(id="ONU-TEST")
    splitter = Splitter(id="SPLIT-TEST")
    fiber = OpticalFiber(id="FIBER-TEST")
    
    print(f"\nPASO 1: Crear elementos")
    print(f"  - OLT: {olt.id}")
    print(f"  - ONU: {onu.id}")
    print(f"  - Splitter: {splitter.id}")
    print(f"  - Fiber: {fiber.id}")
    
    print(f"\nPASO 2: Agregar elementos a la red")
    network.add_olt(olt)
    network.add_onu(onu)
    network.add_splitter(splitter)
    network.add_fiber(fiber)
    
    print("\nDATOS DE SALIDA:")
    print(f"  - OLT en red: {network.olt.id if network.olt else 'None'}")
    print(f"  - ONUs en red: {len(network.onus)}")
    print(f"  - Splitters en red: {len(network.splitters)}")
    print(f"  - Fibers en red: {len(network.fibers)}")
    
    # Verificaciones
    assert network.olt == olt, "Error: OLT no coincide"
    assert len(network.onus) == 1, f"Error: Debería haber 1 ONU, hay {len(network.onus)}"
    assert len(network.splitters) == 1, f"Error: Debería haber 1 splitter, hay {len(network.splitters)}"
    assert len(network.fibers) == 1, f"Error: Debería haber 1 fibra, hay {len(network.fibers)}"
    
    print("\n✓ VERIFICACIÓN: Elementos agregados correctamente")
    print("✓ TEST PASADO: OpticalNetwork add_elements OK\n")


if __name__ == "__main__":
    print("=" * 70)
    print("EJECUTANDO TESTS DE OPTICAL NETWORK")
    print("=" * 70)
    test_network_initialization()
    test_network_custom_initialization()
    test_network_create_star_topology()
    test_network_create_star_topology_32_onus()
    test_network_connections()
    test_network_power_budget_calculation()
    test_network_to_dict()
    test_network_add_elements()
    print("=" * 70)
    print("✓ TODOS LOS TESTS DE OPTICAL NETWORK PASARON CORRECTAMENTE")
    print("=" * 70)
