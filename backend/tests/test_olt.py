"""
Tests para la clase OLT
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.network_elements import OLT


def test_olt_initialization():
    """Test de inicialización básica del OLT"""
    print("\n=== TEST: Inicialización básica OLT ===")
    print("ENTRADA: Crear OLT con valores por defecto")
    
    olt = OLT()
    
    print("\nDATOS DE SALIDA:")
    print(f"  - ID: {olt.id}")
    print(f"  - Nombre: {olt.name}")
    print(f"  - Potencia TX: {olt.tx_power} dBm")
    print(f"  - Sensibilidad RX: {olt.rx_sensitivity} dBm")
    print(f"  - Capacidad total: {olt.total_capacity} Mbps")
    
    # Verificaciones
    assert olt.id == "OLT-1", f"Error: ID esperado 'OLT-1', obtenido '{olt.id}'"
    assert olt.name == "OLT Principal", f"Error: Nombre esperado 'OLT Principal', obtenido '{olt.name}'"
    assert olt.tx_power == 2.5, f"Error: TX power esperado 2.5, obtenido {olt.tx_power}"
    assert olt.rx_sensitivity == -27, f"Error: RX sensitivity esperado -27, obtenido {olt.rx_sensitivity}"
    assert olt.total_capacity == 2500, f"Error: Capacidad esperada 2500, obtenida {olt.total_capacity}"
    
    print("\n✓ VERIFICACIÓN: Todos los valores por defecto son correctos")
    print("✓ TEST PASADO: OLT initialization OK\n")


def test_olt_custom_initialization():
    """Test de inicialización con parámetros personalizados"""
    print("\n=== TEST: Inicialización OLT con parámetros personalizados ===")
    print("ENTRADA:")
    print("  - id='OLT-TEST'")
    print("  - name='OLT Test'")
    print("  - tx_power=3.0 dBm")
    print("  - rx_sensitivity=-28 dBm")
    
    olt = OLT(id="OLT-TEST", name="OLT Test", tx_power=3.0, rx_sensitivity=-28)
    
    print("\nDATOS DE SALIDA:")
    print(f"  - ID: {olt.id}")
    print(f"  - Nombre: {olt.name}")
    print(f"  - Potencia TX: {olt.tx_power} dBm")
    print(f"  - Sensibilidad RX: {olt.rx_sensitivity} dBm")
    
    # Verificaciones
    assert olt.id == "OLT-TEST", f"Error: ID esperado 'OLT-TEST', obtenido '{olt.id}'"
    assert olt.name == "OLT Test", f"Error: Nombre esperado 'OLT Test', obtenido '{olt.name}'"
    assert olt.tx_power == 3.0, f"Error: TX power esperado 3.0, obtenido {olt.tx_power}"
    assert olt.rx_sensitivity == -28, f"Error: RX sensitivity esperado -28, obtenido {olt.rx_sensitivity}"
    
    print("\n✓ VERIFICACIÓN: Todos los valores personalizados son correctos")
    print("✓ TEST PASADO: OLT custom initialization OK\n")


def test_olt_power_budget():
    """Test del cálculo de power budget"""
    print("\n=== TEST: Cálculo de Power Budget ===")
    print("ENTRADA:")
    print("  - OLT con tx_power=2.5 dBm")
    print("  - OLT con rx_sensitivity=-27 dBm")
    
    olt = OLT()
    print(f"\nPASO 1: Crear OLT (TX={olt.tx_power} dBm, RX={olt.rx_sensitivity} dBm)")
    
    power_budget = olt.calculate_power_budget()
    expected = 2.5 - (-27)  # tx_power - rx_sensitivity
    
    print("\nPASO 2: Calcular power budget")
    print(f"  Fórmula: Power Budget = TX_power - RX_sensitivity")
    print(f"  Cálculo: {olt.tx_power} - ({olt.rx_sensitivity}) = {power_budget} dB")
    
    print("\nDATOS DE SALIDA:")
    print(f"  - Power Budget calculado: {power_budget} dB")
    print(f"  - Power Budget esperado: {expected} dB")
    
    # Verificaciones
    assert power_budget == expected, f"Error: Power budget esperado {expected}, obtenido {power_budget}"
    assert power_budget == 29.5, f"Error: Power budget esperado 29.5, obtenido {power_budget}"
    
    print("\n✓ VERIFICACIÓN: Power budget calculado correctamente")
    print("✓ TEST PASADO: OLT power budget calculation OK\n")


def test_olt_to_dict():
    """Test de conversión a diccionario"""
    print("\n=== TEST: Conversión OLT a diccionario ===")
    print("ENTRADA: Crear OLT y convertir a diccionario")
    
    olt = OLT()
    print("\nPASO 1: Crear OLT")
    print(f"  - ID: {olt.id}")
    print(f"  - Nombre: {olt.name}")
    
    olt_dict = olt.to_dict()
    
    print("\nPASO 2: Convertir a diccionario usando to_dict()")
    print("\nDATOS DE SALIDA (diccionario):")
    for key, value in olt_dict.items():
        print(f"  - {key}: {value}")
    
    # Verificaciones
    assert olt_dict['id'] == "OLT-1", f"Error: ID esperado 'OLT-1', obtenido '{olt_dict['id']}'"
    assert olt_dict['name'] == "OLT Principal", f"Error: Nombre esperado 'OLT Principal', obtenido '{olt_dict['name']}'"
    assert olt_dict['type'] == "OLT", f"Error: Tipo esperado 'OLT', obtenido '{olt_dict['type']}'"
    assert olt_dict['tx_power'] == 2.5, f"Error: TX power esperado 2.5, obtenido {olt_dict['tx_power']}"
    assert olt_dict['rx_sensitivity'] == -27, f"Error: RX sensitivity esperado -27, obtenido {olt_dict['rx_sensitivity']}"
    assert olt_dict['total_capacity'] == 2500, f"Error: Capacidad esperada 2500, obtenida {olt_dict['total_capacity']}"
    assert 'connected_splitters' in olt_dict, "Error: 'connected_splitters' no está en el diccionario"
    
    print("\n✓ VERIFICACIÓN: Todos los campos del diccionario son correctos")
    print("✓ TEST PASADO: OLT to_dict OK\n")


if __name__ == "__main__":
    print("=" * 70)
    print("EJECUTANDO TESTS DE OLT")
    print("=" * 70)
    test_olt_initialization()
    test_olt_custom_initialization()
    test_olt_power_budget()
    test_olt_to_dict()
    print("=" * 70)
    print("✓ TODOS LOS TESTS DE OLT PASARON CORRECTAMENTE")
    print("=" * 70)
