"""
Script para crear la estructura de tablas en la base de datos MySQL
"""
import logging
from database.db_connector import DatabaseConnector

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('db_schema')

# SQL para crear la tabla de productos
CREATE_PRODUCTOS_TABLE = """
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio_kg DECIMAL(10, 2),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# SQL para crear la tabla de vendedores
CREATE_VENDEDORES_TABLE = """
CREATE TABLE IF NOT EXISTS vendedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    documento VARCHAR(20),
    telefono VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# SQL para crear la tabla de pesajes
CREATE_PESAJES_TABLE = """
CREATE TABLE IF NOT EXISTS pesajes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_producto VARCHAR(20) NOT NULL,
    peso DECIMAL(10, 2) NOT NULL,
    codigo_vendedor VARCHAR(20) NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    precio_kg DECIMAL(10, 2),
    total DECIMAL(10, 2) GENERATED ALWAYS AS (peso * precio_kg) STORED,
    observaciones TEXT,
    FOREIGN KEY (codigo_producto) REFERENCES productos(codigo) ON DELETE RESTRICT,
    FOREIGN KEY (codigo_vendedor) REFERENCES vendedores(codigo) ON DELETE RESTRICT,
    INDEX idx_fecha_hora (fecha_hora),
    INDEX idx_codigo_vendedor (codigo_vendedor),
    INDEX idx_codigo_producto (codigo_producto)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# SQL para insertar datos de ejemplo en la tabla de productos
INSERT_SAMPLE_PRODUCTOS = """
INSERT IGNORE INTO productos (codigo, nombre, descripcion, precio_kg) VALUES
    ('P001', 'Carne molida', 'Carne molida de res', 8.50),
    ('P002', 'Lomo fino', 'Lomo fino de res', 12.75),
    ('P003', 'Costilla', 'Costilla de cerdo', 7.25),
    ('P004', 'Pollo entero', 'Pollo entero sin menudencias', 5.99),
    ('P005', 'Pechuga de pollo', 'Pechuga de pollo sin hueso', 9.25);
"""

# SQL para insertar datos de ejemplo en la tabla de vendedores
INSERT_SAMPLE_VENDEDORES = """
INSERT IGNORE INTO vendedores (codigo, nombre, apellido, documento, telefono) VALUES
    ('V001', 'Juan', 'Pérez', '12345678', '555-123-4567'),
    ('V002', 'María', 'González', '23456789', '555-234-5678'),
    ('V003', 'Carlos', 'Rodríguez', '34567890', '555-345-6789'),
    ('V004', 'Ana', 'Martínez', '45678901', '555-456-7890'),
    ('V005', 'Luis', 'Hernández', '56789012', '555-567-8901');
"""

def create_database():
    """Crea la base de datos si no existe"""
    from mysql.connector import connect
    from config.db_config import get_db_config
    
    config = get_db_config()
    
    try:
        # Conectar sin especificar la base de datos
        connection = connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password']
        )
        
        cursor = connection.cursor()
        
        # Crear la base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        logger.info(f"Base de datos '{config['database']}' creada o verificada correctamente")
        
        # Cerrar conexión
        cursor.close()
        connection.close()
        
    except Exception as e:
        logger.error(f"Error al crear la base de datos: {e}")
        raise

def initialize_schema():
    """Inicializa el esquema de la base de datos"""
    try:
        # Crear la base de datos primero
        create_database()
        
        # Conectar a la base de datos
        db = DatabaseConnector()
        
        # Crear tablas
        logger.info("Creando tabla de productos...")
        db.execute_query(CREATE_PRODUCTOS_TABLE)
        
        logger.info("Creando tabla de vendedores...")
        db.execute_query(CREATE_VENDEDORES_TABLE)
        
        logger.info("Creando tabla de pesajes...")
        db.execute_query(CREATE_PESAJES_TABLE)
        
        # Insertar datos de ejemplo
        logger.info("Insertando datos de ejemplo en la tabla de productos...")
        db.execute_query(INSERT_SAMPLE_PRODUCTOS)
        
        logger.info("Insertando datos de ejemplo en la tabla de vendedores...")
        db.execute_query(INSERT_SAMPLE_VENDEDORES)
        
        logger.info("Esquema de base de datos inicializado correctamente")
        return True
    
    except Exception as e:
        logger.error(f"Error al inicializar el esquema de la base de datos: {e}")
        return False

if __name__ == "__main__":
    # Si este script se ejecuta directamente, inicializar el esquema
    initialize_schema()