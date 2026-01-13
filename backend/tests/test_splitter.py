"""
Tests para la clase Splitter
"""
import sys
import os
import math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.network_elements import Splitter, OLT, ONU


def test_splitter_initialization():
    """Test de inicialización básica del Splitter"""
    print("\n=== TEST: Inicialización básica Splitter ===")
    print("ENTRADA: Crear Splitter con valores por defecto")
    
    splitter = Splitter()
    
    print("\nDATOS DE SALIDA:")
    print(f"  - ID: {splitter.id}")
    print(f"  - Nombre: {splitter.name}")
    print(f"  - Ratio: {splitter.ratio}")
    print(f"  - Split Loss: {splitter.split_loss:.2f} dB")
    print(f"  - OLT conectado: {splitter.connected_olt.id if splitter.connected_olt else 'None'}")
    print(f"  - ONUs conectadas: {len(splitter.connected_onus)}")
    
    # Verificaciones
    assert splitter.id == "SPLIT-1", f"Error: ID esperado 'SPLIT-1', obtenido '{splitter.id}'"
    assert splitter.name == "Splitter", f"Error: Nombre esperado 'Splitter', obtenido '{splitter.name}'"
    assert splitter.ratio == "1:32", f"Error: Ratio esperado '1:32', obtenido '{splitter.ratio}'"
    assert splitter.connected_olt is None, "Error: connected_olt debería ser None"
    assert len(splitter.connected_onus) == 0, f"Error: connected_onus debería estar vacío, tiene {len(splitter.connected_onus)} elementos"
    
    print("\n✓ VERIFICACIÓN: Todos los valores por defecto son correctos")
    print("✓ TEST PASADO: Splitter initialization OK\n")


def test_splitter_split_loss_calculation():
    """Test del cálculo de pérdida por splitting"""
    print("\n=== TEST: Cálculo de pérdida por splitting ===")
    print("ENTRADA:")
    print("  - Crear Splitter con ratio='1:8'")
    print("  - Crear Splitter con ratio='1:32'")
    
    print("\nPASO 1: Crear Splitter con ratio 1:8")
    splitter_8 = Splitter(ratio="1:8")
    expected_loss_8 = 10 * math.log10(8)
    print(f"  Fórmula: Loss = 10 * log10(N) donde N es el número de puertos")
    print(f"  Cálculo: 10 * log10(8) = {expected_loss_8:.2f} dB")
    print(f"  Resultado obtenido: {splitter_8.split_loss:.2f} dB")
    
    print("\nPASO 2: Crear Splitter con ratio 1:32")
    splitter_32 = Splitter(ratio="1:32")
    expected_loss_32 = 10 * math.log10(32)
    print(f"  Cálculo: 10 * log10(32) = {expected_loss_32:.2f} dB")
    print(f"  Resultado obtenido: {splitter_32.split_loss:.2f} dB")
    
    print("\nDATOS DE SALIDA:")
    print(f"  - Splitter 1:8 - Loss: {splitter_8.split_loss:.2f} dB (esperado: {expected_loss_8:.2f} dB)")
    print(f"  - Splitter 1:32 - Loss: {splitter_32.split_loss:.2f} dB (esperado: {expected_loss_32:.2f} dB)")
    
    # Verificaciones
    assert abs(splitter_8.split_loss - expected_loss_8) < 0.01, f"Error: Loss 1:8 esperado {expected_loss_8:.2f}, obtenido {splitter_8.split_loss:.2f}"
    assert abs(splitter_32.split_loss - expected_loss_32) < 0.01, f"Error: Loss 1:32 esperado {expected_loss_32:.2f}, obtenido {splitter_32.split_loss:.2f}"
    
    print("\n✓ VERIFICACIÓN: Pérdidas calculadas correctamente según la fórmula")
    print("✓ TEST PASADO: Splitter split_loss calculation OK\n")


def test_splitter_connect_olt():
    """Test de conexión del splitter al OLT"""
    print("\n=== TEST: Conexión Splitter a OLT ===")
    print("ENTRADA:")
    print("  - Crear Splitter")
    print("  - Crear OLT")
    print("  - Conectar Splitter al OLT")
    
    splitter = Splitter()
    olt = OLT(id="OLT-TEST")
    
    print(f"\nPASO 1: Crear Splitter y OLT (ID: {olt.id})")
    print(f"PASO 2: Conectar Splitter al OLT usando connect_olt()")
    
    splitter.connect_olt(olt)
    
    print("\nDATOS DE SALIDA:")
    print(f"  - Splitter.connected_olt: {splitter.connected_olt.id if splitter.connected_olt else 'None'}")
    
    # Verificaciones
    assert splitter.connected_olt == olt, "Error: Splitter no está conectado al OLT"
    
    print("\n✓ VERIFICACIÓN: Conexión establecida correctamente")
    print("✓ TEST PASADO: Splitter connect_olt OK\n")


def test_splitter_connect_onu():
    """Test de conexión de ONU al splitter"""
    print("\n=== TEST: Conexión de ONUs al Splitter ===")
    print("ENTRADA:")
    print("  - Crear Splitter")
    print("  - Crear 2 ONUs")
    print("  - Conectar ambas ONUs al Splitter")
    
    splitter = Splitter()
    onu1 = ONU(id="ONU-1")
    onu2 = ONU(id="ONU-2")
    
    print(f"\nPASO 1: Crear Splitter y 2 ONUs (ID: {onu1.id}, {onu2.id})")
    print(f"PASO 2: Conectar primera ONU al Splitter")
    
    splitter.connect_onu(onu1)
    print(f"  ONUs conectadas después de primera conexión: {len(splitter.connected_onus)}")
    
    print(f"PASO 3: Conectar segunda ONU al Splitter")
    splitter.connect_onu(onu2)
    print(f"  ONUs conectadas después de segunda conexión: {len(splitter.connected_onus)}")
    
    print(f"PASO 4: Intentar conectar primera ONU nuevamente (no debería duplicar)")
    splitter.connect_onu(onu1)
    print(f"  ONUs conectadas después de intentar duplicar: {len(splitter.connected_onus)}")
    
    print("\nDATOS DE SALIDA:")
    print(f"  - Número de ONUs conectadas: {len(splitter.connected_onus)}")
    print(f"  - ONU-1 en lista: {'Sí' if onu1 in splitter.connected_onus else 'No'}")
    print(f"  - ONU-2 en lista: {'Sí' if onu2 in splitter.connected_onus else 'No'}")
    
    # Verificaciones
    assert len(splitter.connected_onus) == 2, f"Error: Deberían haber 2 ONUs, hay {len(splitter.connected_onus)}"
    assert onu1 in splitter.connected_onus, "Error: ONU-1 no está en la lista"
    assert onu2 in splitter.connected_onus, "Error: ONU-2 no está en la lista"
    
    print("\n✓ VERIFICACIÓN: Conexiones establecidas correctamente, sin duplicados")
    print("✓ TEST PASADO: Splitter connect_onu OK\n")


def test_splitter_to_dict():
    """Test de conversión a diccionario"""
    print("\n=== TEST: Conversión Splitter a diccionario ===")
    print("ENTRADA:")
    print("  - Crear Splitter con ratio='1:16'")
    print("  - Convertir a diccionario")
    
    splitter = Splitter(ratio="1:16")
    print(f"\nPASO 1: Crear Splitter (ratio: {splitter.ratio})")
    print(f"PASO 2: Convertir a diccionario usando to_dict()")
    
    splitter_dict = splitter.to_dict()
    
    print("\nDATOS DE SALIDA (diccionario):")
    for key, value in splitter_dict.items():
        print(f"  - {key}: {value}")
    
    # Verificaciones
    assert splitter_dict['id'] == "SPLIT-1", f"Error: ID esperado 'SPLIT-1', obtenido '{splitter_dict['id']}'"
    assert splitter_dict['type'] == "SPLITTER", f"Error: Tipo esperado 'SPLITTER', obtenido '{splitter_dict['type']}'"
    assert splitter_dict['ratio'] == "1:16", f"Error: Ratio esperado '1:16', obtenido '{splitter_dict['ratio']}'"
    assert splitter_dict['split_loss'] > 0, f"Error: Split loss debería ser positivo, obtenido {splitter_dict['split_loss']}"
    assert splitter_dict['olt_id'] is None, f"Error: olt_id debería ser None, obtenido {splitter_dict['olt_id']}"
    assert splitter_dict['connected_onus'] == 0, f"Error: connected_onus debería ser 0, obtenido {splitter_dict['connected_onus']}"
    
    print("\n✓ VERIFICACIÓN: Todos los campos del diccionario son correctos")
    print("✓ TEST PASADO: Splitter to_dict OK\n")


def test_splitter_to_dict_with_connections():
    """Test de conversión a diccionario con conexiones"""
    print("\n=== TEST: Conversión Splitter a diccionario con conexiones ===")
    print("ENTRADA:")
    print("  - Crear Splitter")
    print("  - Crear OLT con ID='OLT-TEST'")
    print("  - Crear ONU")
    print("  - Conectar OLT y ONU al Splitter")
    print("  - Convertir a diccionario")
    
    splitter = Splitter()
    olt = OLT(id="OLT-TEST")
    onu = ONU()
    
    print(f"\nPASO 1: Crear elementos (OLT ID: {olt.id})")
    print(f"PASO 2: Conectar OLT al Splitter")
    splitter.connect_olt(olt)
    
    print(f"PASO 3: Conectar ONU al Splitter")
    splitter.connect_onu(onu)
    
    print(f"PASO 4: Convertir a diccionario")
    splitter_dict = splitter.to_dict()
    
    print("\nDATOS DE SALIDA:")
    print(f"  - olt_id: {splitter_dict['olt_id']}")
    print(f"  - connected_onus: {splitter_dict['connected_onus']}")
    
    # Verificaciones
    assert splitter_dict['olt_id'] == "OLT-TEST", f"Error: olt_id esperado 'OLT-TEST', obtenido '{splitter_dict['olt_id']}'"
    assert splitter_dict['connected_onus'] == 1, f"Error: connected_onus esperado 1, obtenido {splitter_dict['connected_onus']}"
    
    print("\n✓ VERIFICACIÓN: Conexiones reflejadas correctamente en el diccionario")
    print("✓ TEST PASADO: Splitter to_dict with connections OK\n")


if __name__ == "__main__":
    print("=" * 70)
    print("EJECUTANDO TESTS DE SPLITTER")
    print("=" * 70)
    test_splitter_initialization()
    test_splitter_split_loss_calculation()
    test_splitter_connect_olt()
    test_splitter_connect_onu()
    test_splitter_to_dict()
    test_splitter_to_dict_with_connections()
    print("=" * 70)
    print("✓ TODOS LOS TESTS DE SPLITTER PASARON CORRECTAMENTE")
    print("=" * 70)
