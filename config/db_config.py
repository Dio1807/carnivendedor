"""
Configuración de conexión a MySQL para el sistema de pesaje
"""

# Configuración por defecto para la conexión a MySQL
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '1234',
    'database': 'chaquecarne',
    'charset': 'utf8mb4'
}

# Función para obtener los parámetros de conexión
def get_db_config():
    """Retorna la configuración actual de la base de datos"""
    return DB_CONFIG

# Función para modificar los parámetros de conexión
def set_db_config(host=None, port=None, user=None, password=None, database=None, charset=None):
    """Actualiza la configuración de conexión a la base de datos"""
    global DB_CONFIG
    
    if host is not None:
        DB_CONFIG['host'] = host
    if port is not None:
        DB_CONFIG['port'] = port
    if user is not None:
        DB_CONFIG['user'] = user
    if password is not None:
        DB_CONFIG['password'] = password
    if database is not None:
        DB_CONFIG['database'] = database
    if charset is not None:
        DB_CONFIG['charset'] = charset
    
    return DB_CONFIG

# Función para construir una cadena de conexión para MySQL
def get_connection_string():
    """Construye y retorna la cadena de conexión a MySQL"""
    config = get_db_config()
    conn_str = (
        f"mysql+pymysql://{config['user']}:{config['password']}@"
        f"{config['host']}:{config['port']}/{config['database']}?"
        f"charset={config['charset']}"
    )
    return conn_str