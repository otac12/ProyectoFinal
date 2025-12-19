-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS ftth_db;

USE ftth_db;

-- Tabla para guardar topologías de red
CREATE TABLE IF NOT EXISTS network_topologies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    olt_config JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla para guardar elementos de red
CREATE TABLE IF NOT EXISTS network_elements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topology_id INT NOT NULL,
    element_type ENUM('OLT', 'ONU', 'SPLITTER', 'FIBER') NOT NULL,
    element_id VARCHAR(100) NOT NULL,
    properties JSON,
    position_x FLOAT,
    position_y FLOAT,
    FOREIGN KEY (topology_id) REFERENCES network_topologies(id) ON DELETE CASCADE,
    INDEX idx_topology (topology_id),
    INDEX idx_element_type (element_type)
);

-- Tabla para guardar simulaciones
CREATE TABLE IF NOT EXISTS simulations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topology_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    parameters JSON,
    results JSON,
    status ENUM('PENDING', 'RUNNING', 'COMPLETED', 'FAILED') DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (topology_id) REFERENCES network_topologies(id) ON DELETE CASCADE,
    INDEX idx_topology (topology_id),
    INDEX idx_status (status)
);

-- Tabla para guardar métricas de rendimiento
CREATE TABLE IF NOT EXISTS performance_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    simulation_id INT NOT NULL,
    onu_id VARCHAR(100),
    metric_type VARCHAR(100) NOT NULL,
    metric_value FLOAT,
    timestamp FLOAT,
    FOREIGN KEY (simulation_id) REFERENCES simulations(id) ON DELETE CASCADE,
    INDEX idx_simulation (simulation_id),
    INDEX idx_metric_type (metric_type)
);

