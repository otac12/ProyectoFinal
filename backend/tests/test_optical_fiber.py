"""
Tests para la clase OpticalFiber
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.network_elements import OpticalFiber, OLT, ONU


def test_fiber_initialization():
    """Test de inicialización básica de la fibra óptica"""
    print("\n=== TEST: Inicialización básica OpticalFiber ===")
    print("ENTRADA: Crear OpticalFiber con valores por defecto")
    
    fiber = OpticalFiber()
    
    print("\nDATOS DE SALIDA:")
    print(f"  - ID: {fiber.id}")
    print(f"  - Nombre: {fiber.name}")
    print(f"  - Longitud: {fiber.length} km")
    print(f"  - Atenuación: {fiber.attenuation} dB/km")
    print(f"  - Dispersión: {fiber.dispersion} ps/(nm·km)")
    print(f"  - From element: {fiber.from_element.id if fiber.from_element else 'None'}")
    print(f"  - To element: {fiber.to_element.id if fiber.to_element else 'None'}")
    
    # Verificaciones
    assert fiber.id == "FIBER-1", f"Error: ID esperado 'FIBER-1', obtenido '{fiber.id}'"
    assert fiber.name == "Fiber", f"Error: Nombre esperado 'Fiber', obtenido '{fiber.name}'"
    assert fiber.length == 5.0, f"Error: Longitud esperada 5.0, obtenida {fiber.length}"
    assert fiber.attenuation == 0.2, f"Error: Atenuación esperada 0.2, obtenida {fiber.attenuation}"
    assert fiber.dispersion == 17, f"Error: Dispersión esperada 17, obtenida {fiber.dispersion}"
    assert fiber.from_element is None, "Error: from_element debería ser None"
    assert fiber.to_element is None, "Error: to_element debería ser None"
    
    print("\n✓ VERIFICACIÓN: Todos los valores por defecto son correctos")
    print("✓ TEST PASADO: OpticalFiber initialization OK\n")


def test_fiber_custom_initialization():
    """Test de inicialización con parámetros personalizados"""
    print("\n=== TEST: Inicialización OpticalFiber con parámetros personalizados ===")
    print("ENTRADA:")
    print("  - id='FIBER-TEST'")
    print("  - name='Test Fiber'")
    print("  - length=10.0 km")
    print("  - attenuation=0.25 dB/km")
    
    fiber = OpticalFiber(id="FIBER-TEST", name="Test Fiber", length=10.0, attenuation=0.25)
    
    print("\nDATOS DE SALIDA:")
    print(f"  - ID: {fiber.id}")
    print(f"  - Nombre: {fiber.name}")
    print(f"  - Longitud: {fiber.length} km")
    print(f"  - Atenuación: {fiber.attenuation} dB/km")
    
    # Verificaciones
    assert fiber.id == "FIBER-TEST", f"Error: ID esperado 'FIBER-TEST', obtenido '{fiber.id}'"
    assert fiber.name == "Test Fiber", f"Error: Nombre esperado 'Test Fiber', obtenido '{fiber.name}'"
    assert fiber.length == 10.0, f"Error: Longitud esperada 10.0, obtenida {fiber.length}"
    assert fiber.attenuation == 0.25, f"Error: Atenuación esperada 0.25, obtenida {fiber.attenuation}"
    
    print("\n✓ VERIFICACIÓN: Todos los valores personalizados son correctos")
    print("✓ TEST PASADO: OpticalFiber custom initialization OK\n")


def test_fiber_calculate_loss():
    """Test del cálculo de pérdida de la fibra"""
    print("\n=== TEST: Cálculo de pérdida de fibra ===")
    print("ENTRADA:")
    print("  - Crear fibra con length=5.0 km, attenuation=0.2 dB/km")
    print("  - Crear fibra con length=10.0 km, attenuation=0.2 dB/km")
    
    print("\nPASO 1: Crear fibra de 5 km")
    fiber = OpticalFiber(length=5.0, attenuation=0.2)
    print(f"  Longitud: {fiber.length} km")
    print(f"  Atenuación: {fiber.attenuation} dB/km")
    
    loss = fiber.calculate_loss()
    expected_loss = 5.0 * 0.2
    print(f"\n  Fórmula: Loss = length * attenuation")
    print(f"  Cálculo: {fiber.length} * {fiber.attenuation} = {expected_loss} dB")
    print(f"  Resultado obtenido: {loss} dB")
    
    print("\nPASO 2: Crear fibra de 10 km")
    fiber2 = OpticalFiber(length=10.0, attenuation=0.2)
    print(f"  Longitud: {fiber2.length} km")
    print(f"  Atenuación: {fiber2.attenuation} dB/km")
    
    loss2 = fiber2.calculate_loss()
    expected_loss2 = 10.0 * 0.2
    print(f"\n  Cálculo: {fiber2.length} * {fiber2.attenuation} = {expected_loss2} dB")
    print(f"  Resultado obtenido: {loss2} dB")
    
    print("\nDATOS DE SALIDA:")
    print(f"  - Fibra 5 km - Loss: {loss} dB (esperado: {expected_loss} dB)")
    print(f"  - Fibra 10 km - Loss: {loss2} dB (esperado: {expected_loss2} dB)")
    
    # Verificaciones
    assert loss == 1.0, f"Error: Loss esperado 1.0, obtenido {loss}"
    assert loss2 == 2.0, f"Error: Loss esperado 2.0, obtenido {loss2}"
    
    print("\n✓ VERIFICACIÓN: Pérdidas calculadas correctamente")
    print("✓ TEST PASADO: OpticalFiber calculate_loss OK\n")


def test_fiber_calculate_total_loss():
    """Test del cálculo de pérdida total (incluyendo empalmes)"""
    print("\n=== TEST: Cálculo de pérdida total (con empalmes) ===")
    print("ENTRADA:")
    print("  - Crear fibra con length=5.0 km, attenuation=0.2 dB/km")
    
    fiber = OpticalFiber(length=5.0, attenuation=0.2)
    print(f"\nPASO 1: Crear fibra (length={fiber.length} km)")
    
    fiber_loss = fiber.calculate_loss()
    print(f"PASO 2: Calcular pérdida de fibra")
    print(f"  Loss fibra: {fiber_loss} dB")
    
    total_loss = fiber.calculate_total_loss()
    # Cálculo manual: empalmes cada 2 km = 0.1 * (floor(5/2) + 1) = 0.1 * 3 = 0.3 dB
    splice_loss = 0.1 * (int(5.0 / 2) + 1)
    expected_total = fiber_loss + splice_loss
    
    print(f"\nPASO 3: Calcular pérdida total (incluyendo empalmes)")
    print(f"  Pérdida fibra: {fiber_loss} dB")
    print(f"  Pérdida empalmes: {splice_loss} dB (0.1 dB cada 2 km)")
    print(f"  Total esperado: {expected_total} dB")
    print(f"  Total obtenido: {total_loss} dB")
    
    print("\nDATOS DE SALIDA:")
    print(f"  - Pérdida fibra: {fiber_loss} dB")
    print(f"  - Pérdida total (con empalmes): {total_loss} dB")
    print(f"  - Diferencia (empalmes): {total_loss - fiber_loss:.2f} dB")
    
    # Verificaciones
    assert total_loss > fiber_loss, "Error: La pérdida total debe ser mayor que la pérdida de fibra"
    assert total_loss >= 1.3, f"Error: Pérdida total esperada >= 1.3, obtenida {total_loss}"
    
    print("\n✓ VERIFICACIÓN: Pérdida total incluye correctamente los empalmes")
    print("✓ TEST PASADO: OpticalFiber calculate_total_loss OK\n")


def test_fiber_connect():
    """Test de conexión de fibra entre elementos"""
    print("\n=== TEST: Conexión de fibra entre elementos ===")
    print("ENTRADA:")
    print("  - Crear OpticalFiber")
    print("  - Crear OLT")
    print("  - Crear ONU")
    print("  - Conectar fibra desde OLT a ONU")
    
    fiber = OpticalFiber()
    olt = OLT(id="OLT-TEST")
    onu = ONU(id="ONU-TEST")
    
    print(f"\nPASO 1: Crear elementos (OLT ID: {olt.id}, ONU ID: {onu.id})")
    print(f"PASO 2: Conectar fibra usando connect(olt, onu)")
    
    fiber.connect(olt, onu)
    
    print("\nDATOS DE SALIDA:")
    print(f"  - fiber.from_element: {fiber.from_element.id if fiber.from_element else 'None'}")
    print(f"  - fiber.to_element: {fiber.to_element.id if fiber.to_element else 'None'}")
    
    # Verificaciones
    assert fiber.from_element == olt, "Error: from_element debería ser el OLT"
    assert fiber.to_element == onu, "Error: to_element debería ser la ONU"
    
    print("\n✓ VERIFICACIÓN: Conexión establecida correctamente")
    print("✓ TEST PASADO: OpticalFiber connect OK\n")


def test_fiber_to_dict():
    """Test de conversión a diccionario"""
    print("\n=== TEST: Conversión OpticalFiber a diccionario ===")
    print("ENTRADA:")
    print("  - Crear fibra con length=3.0 km")
    print("  - Convertir a diccionario")
    
    fiber = OpticalFiber(length=3.0)
    print(f"\nPASO 1: Crear fibra (length={fiber.length} km)")
    print(f"PASO 2: Convertir a diccionario usando to_dict()")
    
    fiber_dict = fiber.to_dict()
    
    print("\nDATOS DE SALIDA (diccionario):")
    for key, value in fiber_dict.items():
        print(f"  - {key}: {value}")
    
    # Verificaciones
    assert fiber_dict['id'] == "FIBER-1", f"Error: ID esperado 'FIBER-1', obtenido '{fiber_dict['id']}'"
    assert fiber_dict['type'] == "FIBER", f"Error: Tipo esperado 'FIBER', obtenido '{fiber_dict['type']}'"
    assert fiber_dict['length'] == 3.0, f"Error: Longitud esperada 3.0, obtenida {fiber_dict['length']}"
    assert fiber_dict['attenuation'] == 0.2, f"Error: Atenuación esperada 0.2, obtenida {fiber_dict['attenuation']}"
    assert 'loss' in fiber_dict, "Error: 'loss' no está en el diccionario"
    assert 'total_loss' in fiber_dict, "Error: 'total_loss' no está en el diccionario"
    assert fiber_dict['from_element'] is None, f"Error: from_element debería ser None, obtenido {fiber_dict['from_element']}"
    assert fiber_dict['to_element'] is None, f"Error: to_element debería ser None, obtenido {fiber_dict['to_element']}"
    
    print("\n✓ VERIFICACIÓN: Todos los campos del diccionario son correctos")
    print("✓ TEST PASADO: OpticalFiber to_dict OK\n")


def test_fiber_to_dict_with_connections():
    """Test de conversión a diccionario con conexiones"""
    print("\n=== TEST: Conversión OpticalFiber a diccionario con conexiones ===")
    print("ENTRADA:")
    print("  - Crear OpticalFiber")
    print("  - Crear OLT con ID='OLT-TEST'")
    print("  - Crear ONU con ID='ONU-TEST'")
    print("  - Conectar fibra desde OLT a ONU")
    print("  - Convertir a diccionario")
    
    fiber = OpticalFiber()
    olt = OLT(id="OLT-TEST")
    onu = ONU(id="ONU-TEST")
    
    print(f"\nPASO 1: Crear elementos (OLT ID: {olt.id}, ONU ID: {onu.id})")
    print(f"PASO 2: Conectar fibra")
    fiber.connect(olt, onu)
    
    print(f"PASO 3: Convertir a diccionario")
    fiber_dict = fiber.to_dict()
    
    print("\nDATOS DE SALIDA:")
    print(f"  - from_element: {fiber_dict['from_element']}")
    print(f"  - to_element: {fiber_dict['to_element']}")
    
    # Verificaciones
    assert fiber_dict['from_element'] == "OLT-TEST", f"Error: from_element esperado 'OLT-TEST', obtenido '{fiber_dict['from_element']}'"
    assert fiber_dict['to_element'] == "ONU-TEST", f"Error: to_element esperado 'ONU-TEST', obtenido '{fiber_dict['to_element']}'"
    
    print("\n✓ VERIFICACIÓN: Conexiones reflejadas correctamente en el diccionario")
    print("✓ TEST PASADO: OpticalFiber to_dict with connections OK\n")


if __name__ == "__main__":
    print("=" * 70)
    print("EJECUTANDO TESTS DE OPTICAL FIBER")
    print("=" * 70)
    test_fiber_initialization()
    test_fiber_custom_initialization()
    test_fiber_calculate_loss()
    test_fiber_calculate_total_loss()
    test_fiber_connect()
    test_fiber_to_dict()
    test_fiber_to_dict_with_connections()
    print("=" * 70)
    print("✓ TODOS LOS TESTS DE OPTICAL FIBER PASARON CORRECTAMENTE")
    print("=" * 70)
