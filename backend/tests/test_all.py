"""
Script para ejecutar todos los tests con información detallada
"""
import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == "__main__":
    print("=" * 70)
    print("EJECUTANDO TODOS LOS TESTS DEL PROYECTO")
    print("=" * 70)
    print()
    
    # Ejecutar tests de OLT
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "TESTS DE OLT" + " " * 37 + "║")
    print("╚" + "═" * 68 + "╝")
    from tests.test_olt import *
    test_olt_initialization()
    test_olt_custom_initialization()
    test_olt_power_budget()
    test_olt_to_dict()
    print()
    
    # Ejecutar tests de ONU
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "TESTS DE ONU" + " " * 37 + "║")
    print("╚" + "═" * 68 + "╝")
    from tests.test_onu import *
    test_onu_initialization()
    test_onu_set_traffic_rate()
    test_onu_connect_splitter()
    test_onu_to_dict()
    test_onu_to_dict_with_splitter()
    print()
    
    # Ejecutar tests de Splitter
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 18 + "TESTS DE SPLITTER" + " " * 33 + "║")
    print("╚" + "═" * 68 + "╝")
    from tests.test_splitter import *
    test_splitter_initialization()
    test_splitter_split_loss_calculation()
    test_splitter_connect_olt()
    test_splitter_connect_onu()
    test_splitter_to_dict()
    test_splitter_to_dict_with_connections()
    print()
    
    # Ejecutar tests de OpticalFiber
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 16 + "TESTS DE OPTICAL FIBER" + " " * 31 + "║")
    print("╚" + "═" * 68 + "╝")
    from tests.test_optical_fiber import *
    test_fiber_initialization()
    test_fiber_custom_initialization()
    test_fiber_calculate_loss()
    test_fiber_calculate_total_loss()
    test_fiber_connect()
    test_fiber_to_dict()
    test_fiber_to_dict_with_connections()
    print()
    
    # Ejecutar tests de OpticalNetwork
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 16 + "TESTS DE OPTICAL NETWORK" + " " * 29 + "║")
    print("╚" + "═" * 68 + "╝")
    from tests.test_optical_network import *
    test_network_initialization()
    test_network_custom_initialization()
    test_network_create_star_topology()
    test_network_create_star_topology_32_onus()
    test_network_connections()
    test_network_power_budget_calculation()
    test_network_to_dict()
    test_network_add_elements()
    print()
    
    print("=" * 70)
    print("✓✓✓ TODOS LOS TESTS PASARON CORRECTAMENTE ✓✓✓")
    print("=" * 70)
    print("\nResumen:")
    print("  - Tests de OLT: 4 tests")
    print("  - Tests de ONU: 5 tests")
    print("  - Tests de Splitter: 6 tests")
    print("  - Tests de OpticalFiber: 7 tests")
    print("  - Tests de OpticalNetwork: 8 tests")
    print("  - TOTAL: 30 tests ejecutados exitosamente")
    print("=" * 70)
