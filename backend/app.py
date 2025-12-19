"""
Aplicación Flask principal para el simulador FTTH
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# Importar db antes de cualquier otra cosa
from database import db

app = Flask(__name__)
CORS(app)

# Configuración de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER', 'ftth_user')}:"
    f"{os.getenv('MYSQL_PASSWORD', 'ftth_password')}@"
    f"{os.getenv('MYSQL_HOST', 'mysql')}:"
    f"{os.getenv('MYSQL_PORT', '3306')}/"
    f"{os.getenv('MYSQL_DATABASE', 'ftth_db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar db con la app
db.init_app(app)

# Importar otros módulos (estos no dependen de db directamente)
from models.network_elements import OpticalNetwork, OLT, ONU, Splitter, OpticalFiber
from simulators.traffic_simulator import TrafficSimulator
from simulators.dba_algorithm import DynamicBandwidthAllocation

# Importar modelos de DB - debe estar después de db.init_app()
from models.db_models import NetworkTopology, NetworkElement, Simulation, PerformanceMetric

# Crear tablas dentro del contexto de la aplicación
with app.app_context():
    db.create_all()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de verificación de salud"""
    return jsonify({"status": "ok", "message": "FTTH Simulator API is running"})


@app.route('/api/topologies', methods=['GET'])
def get_topologies():
    """Obtener todas las topologías"""
    try:
        topologies = NetworkTopology.query.all()
        return jsonify({
            "success": True,
            "data": [t.to_dict() for t in topologies]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/topologies', methods=['POST'])
def create_topology():
    """Crear una nueva topología"""
    try:
        data = request.json
        network = OpticalNetwork(name=data.get('name', 'New Network'))
        
        # Crear topología según parámetros
        num_onus = data.get('num_onus', 32)
        split_ratio = data.get('split_ratio', '1:32')
        topology_type = data.get('topology_type', 'star')
        network.create_ftth_topology(
            num_onus=num_onus, 
            split_ratio=split_ratio,
            topology_type=topology_type
        )
        
        # Guardar en base de datos
        topology = NetworkTopology(
            name=network.name,
            description=data.get('description', ''),
            olt_config=json.dumps(network.to_dict())
        )
        db.session.add(topology)
        db.session.flush()
        
        # Guardar elementos
        if network.olt:
            element = NetworkElement(
                topology_id=topology.id,
                element_type='OLT',
                element_id=network.olt.id,
                properties=json.dumps(network.olt.to_dict())
            )
            db.session.add(element)
        
        for splitter in network.splitters:
            element = NetworkElement(
                topology_id=topology.id,
                element_type='SPLITTER',
                element_id=splitter.id,
                properties=json.dumps(splitter.to_dict())
            )
            db.session.add(element)
        
        for onu in network.onus:
            element = NetworkElement(
                topology_id=topology.id,
                element_type='ONU',
                element_id=onu.id,
                properties=json.dumps(onu.to_dict())
            )
            db.session.add(element)
        
        for fiber in network.fibers:
            element = NetworkElement(
                topology_id=topology.id,
                element_type='FIBER',
                element_id=fiber.id,
                properties=json.dumps(fiber.to_dict())
            )
            db.session.add(element)
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": {
                "id": topology.id,
                "network": network.to_dict()
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/topologies/<int:topology_id>', methods=['GET'])
def get_topology(topology_id):
    """Obtener una topología específica"""
    try:
        topology = NetworkTopology.query.get_or_404(topology_id)
        elements = NetworkElement.query.filter_by(topology_id=topology_id).all()
        
        # Reconstruir red desde base de datos
        network_data = json.loads(topology.olt_config)
        return jsonify({
            "success": True,
            "data": {
                "id": topology.id,
                "name": topology.name,
                "network": network_data
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/topologies/<int:topology_id>/power-budget', methods=['GET'])
def calculate_power_budget(topology_id):
    """Calcular power budget para todas las ONUs"""
    try:
        topology = NetworkTopology.query.get_or_404(topology_id)
        network_data = json.loads(topology.olt_config)
        
        # Reconstruir red (versión simplificada)
        network = OpticalNetwork(name=network_data['name'])
        topology_type = network_data.get('topology_type', 'star')
        network.create_ftth_topology(
            num_onus=len(network_data.get('onus', [])),
            split_ratio=network_data.get('splitters', [{}])[0].get('ratio', '1:32') if network_data.get('splitters') else '1:32',
            topology_type=topology_type
        )
        
        results = []
        for onu in network.onus:
            power_budget = network.calculate_power_budget_path(onu)
            if power_budget:
                results.append({
                    "onu_id": onu.id,
                    **power_budget
                })
        
        return jsonify({
            "success": True,
            "data": results
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/simulations', methods=['POST'])
def create_simulation():
    """Crear y ejecutar una simulación"""
    try:
        data = request.json
        topology_id = data.get('topology_id')
        
        if not topology_id:
            return jsonify({"success": False, "error": "topology_id is required"}), 400
        
        topology = NetworkTopology.query.get_or_404(topology_id)
        network_data = json.loads(topology.olt_config)
        
        # Crear simulación
        simulation = Simulation(
            topology_id=topology_id,
            name=data.get('name', 'Simulation'),
            parameters=json.dumps(data.get('parameters', {})),
            status='RUNNING'
        )
        db.session.add(simulation)
        db.session.flush()
        
        # Ejecutar simulación
        simulator = TrafficSimulator(
            num_onus=len(network_data.get('onus', [])),
            simulation_time=data.get('parameters', {}).get('simulation_time', 100)
        )
        
        results = simulator.run()
        
        # Guardar resultados
        simulation.results = json.dumps(results)
        simulation.status = 'COMPLETED'
        
        # Guardar métricas
        for metric in results.get('metrics', []):
            perf_metric = PerformanceMetric(
                simulation_id=simulation.id,
                onu_id=metric.get('onu_id'),
                metric_type=metric.get('type'),
                metric_value=metric.get('value'),
                timestamp=metric.get('timestamp', 0)
            )
            db.session.add(perf_metric)
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "data": {
                "id": simulation.id,
                "name": simulation.name,
                "results": results
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/simulations/<int:simulation_id>', methods=['GET'])
def get_simulation(simulation_id):
    """Obtener resultados de una simulación"""
    try:
        simulation = Simulation.query.get_or_404(simulation_id)
        metrics = PerformanceMetric.query.filter_by(simulation_id=simulation_id).all()
        
        return jsonify({
            "success": True,
            "data": {
                "id": simulation.id,
                "name": simulation.name,
                "status": simulation.status,
                "parameters": json.loads(simulation.parameters),
                "results": json.loads(simulation.results) if simulation.results else None,
                "metrics": [m.to_dict() for m in metrics]
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/dba/allocate', methods=['POST'])
def allocate_bandwidth():
    """Calcular asignación de ancho de banda con DBA"""
    try:
        data = request.json
        requests = data.get('onu_requests', {})
        total_capacity = data.get('total_capacity', 2500)
        
        dba = DynamicBandwidthAllocation()
        allocation = dba.allocate_bandwidth(requests, total_capacity)
        
        return jsonify({
            "success": True,
            "data": allocation
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

