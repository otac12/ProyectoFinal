"""
Tests para la clase ONU
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.network_elements import ONU, Splitter


def test_onu_initialization():
    """Test de inicialización básica de la ONU"""
    print("\n=== TEST: Inicialización básica ONU ===")
    print("ENTRADA: Crear ONU con valores por defecto")
    
    onu = ONU()
    
    print("\nDATOS DE SALIDA:")
    print(f"  - ID: {onu.id}")
    print(f"  - Nombre: {onu.name}")
    print(f"  - Potencia TX: {onu.tx_power} dBm")
    print(f"  - Sensibilidad RX: {onu.rx_sensitivity} dBm")
    print(f"  - Tasa de tráfico: {onu.traffic_rate} Mbps")
    print(f"  - Ancho de banda solicitado: {onu.requested_bandwidth} Mbps")
    
    # Verificaciones
    assert onu.id == "ONU-1", f"Error: ID esperado 'ONU-1', obtenido '{onu.id}'"
    assert onu.name == "ONU", f"Error: Nombre esperado 'ONU', obtenido '{onu.name}'"
    assert onu.tx_power == 1.5, f"Error: TX power esperado 1.5, obtenido {onu.tx_power}"
    assert onu.rx_sensitivity == -24, f"Error: RX sensitivity esperado -24, obtenido {onu.rx_sensitivity}"
    assert onu.traffic_rate == 0, f"Error: Traffic rate esperado 0, obtenido {onu.traffic_rate}"
    assert onu.requested_bandwidth == 0, f"Error: Requested bandwidth esperado 0, obtenido {onu.requested_bandwidth}"
    
    print("\n✓ VERIFICACIÓN: Todos los valores por defecto son correctos")
    print("✓ TEST PASADO: ONU initialization OK\n")


def test_onu_set_traffic_rate():
    """Test de establecimiento de tasa de tráfico"""
    print("\n=== TEST: Establecer tasa de tráfico en ONU ===")
    print("ENTRADA:")
    print("  - Crear ONU")
    print("  - Establecer traffic_rate = 10 Mbps")
    
    onu = ONU()
    print(f"\nPASO 1: Crear ONU (traffic_rate inicial: {onu.traffic_rate} Mbps)")
    
    traffic_rate_input = 10
    onu.set_traffic_rate(traffic_rate_input)
    
    print(f"\nPASO 2: Ejecutar set_traffic_rate({traffic_rate_input})")
    print(f"  Fórmula: requested_bandwidth = traffic_rate * 1.2 (20% overhead)")
    expected_bandwidth = traffic_rate_input * 1.2
    print(f"  Cálculo: {traffic_rate_input} * 1.2 = {expected_bandwidth} Mbps")
    
    print("\nDATOS DE SALIDA:")
    print(f"  - Traffic Rate: {onu.traffic_rate} Mbps")
    print(f"  - Requested Bandwidth: {onu.requested_bandwidth} Mbps")
    
    # Verificaciones
    assert onu.traffic_rate == 10, f"Error: Traffic rate esperado 10, obtenido {onu.traffic_rate}"
    assert onu.requested_bandwidth == 12.0, f"Error: Requested bandwidth esperado 12.0, obtenido {onu.requested_bandwidth}"
    
    print("\n✓ VERIFICACIÓN: Tasa de tráfico y ancho de banda calculados correctamente")
    print("✓ TEST PASADO: ONU set_traffic_rate OK\n")


def test_onu_connect_splitter():
    """Test de conexión de ONU a splitter"""
    print("\n=== TEST: Conexión ONU a Splitter ===")
    print("ENTRADA:")
    print("  - Crear ONU")
    print("  - Crear Splitter")
    print("  - Conectar ONU al Splitter")
    
    onu = ONU(id="ONU-TEST")
    splitter = Splitter(id="SPLIT-TEST")
    
    print(f"\nPASO 1: Crear ONU (ID: {onu.id})")
    print(f"PASO 2: Crear Splitter (ID: {splitter.id})")
    print(f"PASO 3: Conectar ONU al Splitter usando connect_splitter()")
    
    onu.connect_splitter(splitter)
    
    print("\nDATOS DE SALIDA:")
    print(f"  - ONU.connected_splitter: {onu.connected_splitter.id if onu.connected_splitter else 'None'}")
    print(f"  - Splitter.connected_onus: {len(splitter.connected_onus)} ONU(s)")
    print(f"  - ONU en splitter: {'Sí' if onu in splitter.connected_onus else 'No'}")
    
    # Verificaciones
    assert onu.connected_splitter == splitter, "Error: ONU no está conectada al splitter"
    assert onu in splitter.connected_onus, "Error: ONU no está en la lista de ONUs del splitter"
    
    print("\n✓ VERIFICACIÓN: Conexión establecida correctamente en ambas direcciones")
    print("✓ TEST PASADO: ONU connect_splitter OK\n")


def test_onu_to_dict():
    """Test de conversión a diccionario"""
    print("\n=== TEST: Conversión ONU a diccionario ===")
    print("ENTRADA:")
    print("  - Crear ONU con ID='ONU-TEST'")
    print("  - Establecer traffic_rate=15 Mbps")
    print("  - Convertir a diccionario")
    
    onu = ONU(id="ONU-TEST")
    print(f"\nPASO 1: Crear ONU (ID: {onu.id})")
    
    onu.set_traffic_rate(15)
    print(f"PASO 2: Establecer traffic_rate = 15 Mbps")
    print(f"  - Traffic rate: {onu.traffic_rate} Mbps")
    print(f"  - Requested bandwidth: {onu.requested_bandwidth} Mbps")
    
    onu_dict = onu.to_dict()
    
    print(f"\nPASO 3: Convertir a diccionario usando to_dict()")
    print("\nDATOS DE SALIDA (diccionario):")
    for key, value in onu_dict.items():
        print(f"  - {key}: {value}")
    
    # Verificaciones
    assert onu_dict['id'] == "ONU-TEST", f"Error: ID esperado 'ONU-TEST', obtenido '{onu_dict['id']}'"
    assert onu_dict['type'] == "ONU", f"Error: Tipo esperado 'ONU', obtenido '{onu_dict['type']}'"
    assert onu_dict['tx_power'] == 1.5, f"Error: TX power esperado 1.5, obtenido {onu_dict['tx_power']}"
    assert onu_dict['traffic_rate'] == 15, f"Error: Traffic rate esperado 15, obtenido {onu_dict['traffic_rate']}"
    assert onu_dict['requested_bandwidth'] == 18.0, f"Error: Requested bandwidth esperado 18.0, obtenido {onu_dict['requested_bandwidth']}"
    assert onu_dict['splitter_id'] is None, f"Error: splitter_id debería ser None, obtenido {onu_dict['splitter_id']}"
    
    print("\n✓ VERIFICACIÓN: Todos los campos del diccionario son correctos")
    print("✓ TEST PASADO: ONU to_dict OK\n")


def test_onu_to_dict_with_splitter():
    """Test de conversión a diccionario con splitter conectado"""
    print("\n=== TEST: Conversión ONU a diccionario con Splitter conectado ===")
    print("ENTRADA:")
    print("  - Crear ONU")
    print("  - Crear Splitter con ID='SPLIT-TEST'")
    print("  - Conectar ONU al Splitter")
    print("  - Convertir a diccionario")
    
    onu = ONU()
    splitter = Splitter(id="SPLIT-TEST")
    
    print(f"\nPASO 1: Crear ONU y Splitter (ID: {splitter.id})")
    print(f"PASO 2: Conectar ONU al Splitter")
    
    onu.connect_splitter(splitter)
    onu_dict = onu.to_dict()
    
    print(f"\nPASO 3: Convertir a diccionario")
    print("\nDATOS DE SALIDA:")
    print(f"  - splitter_id en diccionario: {onu_dict['splitter_id']}")
    print(f"  - Splitter real conectado: {onu.connected_splitter.id if onu.connected_splitter else 'None'}")
    
    # Verificaciones
    assert onu_dict['splitter_id'] == "SPLIT-TEST", f"Error: splitter_id esperado 'SPLIT-TEST', obtenido '{onu_dict['splitter_id']}'"
    
    print("\n✓ VERIFICACIÓN: splitter_id está correctamente en el diccionario")
    print("✓ TEST PASADO: ONU to_dict with splitter OK\n")


if __name__ == "__main__":
    print("=" * 70)
    print("EJECUTANDO TESTS DE ONU")
    print("=" * 70)
    test_onu_initialization()
    test_onu_set_traffic_rate()
    test_onu_connect_splitter()
    test_onu_to_dict()
    test_onu_to_dict_with_splitter()
    print("=" * 70)
    print("✓ TODOS LOS TESTS DE ONU PASARON CORRECTAMENTE")
    print("=" * 70)
