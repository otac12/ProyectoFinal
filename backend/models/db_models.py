"""
Modelos de base de datos SQLAlchemy
"""
from database import db
import json


class NetworkTopology(db.Model):
    """Modelo para topologías de red"""
    __tablename__ = 'network_topologies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    olt_config = db.Column(db.JSON)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "olt_config": self.olt_config,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class NetworkElement(db.Model):
    """Modelo para elementos de red"""
    __tablename__ = 'network_elements'
    
    id = db.Column(db.Integer, primary_key=True)
    topology_id = db.Column(db.Integer, db.ForeignKey('network_topologies.id', ondelete='CASCADE'), nullable=False)
    element_type = db.Column(db.Enum('OLT', 'ONU', 'SPLITTER', 'FIBER'), nullable=False)
    element_id = db.Column(db.String(100), nullable=False)
    properties = db.Column(db.JSON)
    position_x = db.Column(db.Float)
    position_y = db.Column(db.Float)
    
    topology = db.relationship('NetworkTopology', backref=db.backref('elements', lazy=True, cascade='all, delete-orphan'))
    
    def to_dict(self):
        return {
            "id": self.id,
            "topology_id": self.topology_id,
            "element_type": self.element_type,
            "element_id": self.element_id,
            "properties": self.properties,
            "position_x": self.position_x,
            "position_y": self.position_y
        }


class Simulation(db.Model):
    """Modelo para simulaciones"""
    __tablename__ = 'simulations'
    
    id = db.Column(db.Integer, primary_key=True)
    topology_id = db.Column(db.Integer, db.ForeignKey('network_topologies.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    parameters = db.Column(db.JSON)
    results = db.Column(db.JSON)
    status = db.Column(db.Enum('PENDING', 'RUNNING', 'COMPLETED', 'FAILED'), default='PENDING')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    completed_at = db.Column(db.TIMESTAMP)
    
    topology = db.relationship('NetworkTopology', backref=db.backref('simulations', lazy=True))
    
    def to_dict(self):
        return {
            "id": self.id,
            "topology_id": self.topology_id,
            "name": self.name,
            "parameters": self.parameters,
            "results": self.results,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


class PerformanceMetric(db.Model):
    """Modelo para métricas de rendimiento"""
    __tablename__ = 'performance_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    simulation_id = db.Column(db.Integer, db.ForeignKey('simulations.id', ondelete='CASCADE'), nullable=False)
    onu_id = db.Column(db.String(100))
    metric_type = db.Column(db.String(100), nullable=False)
    metric_value = db.Column(db.Float)
    timestamp = db.Column(db.Float)
    
    simulation = db.relationship('Simulation', backref=db.backref('metrics', lazy=True))
    
    def to_dict(self):
        return {
            "id": self.id,
            "simulation_id": self.simulation_id,
            "onu_id": self.onu_id,
            "metric_type": self.metric_type,
            "metric_value": self.metric_value,
            "timestamp": self.timestamp
        }

