"""
Módulo para gestionar la conexión a la base de datos MySQL
"""
import mysql.connector
from mysql.connector import Error
import logging
from config.db_config import get_db_config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('db_connector')

class DatabaseConnector:
    """Clase para gestionar la conexión a la base de datos MySQL"""
    
    _instance = None
    
    def __new__(cls):
        """Implementación de patrón Singleton para asegurar una única instancia"""
        if cls._instance is None:
            cls._instance = super(DatabaseConnector, cls).__new__(cls)
            cls._instance._connection = None
        return cls._instance
    
    def connect(self):
        """Establece la conexión con la base de datos MySQL"""
        if self._connection is not None and self._connection.is_connected():
            return self._connection
        
        try:
            # Obtener configuración actual
            config = get_db_config()
            
            # Establecer conexión
            self._connection = mysql.connector.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password'],
                database=config['database'],
                charset=config['charset']
            )
            
            if self._connection.is_connected():
                logger.info("Conexión a MySQL establecida correctamente")
                return self._connection
            
        except Error as e:
            logger.error(f"Error al conectar a MySQL: {e}")
            self._connection = None
            raise
    
    def disconnect(self):
        """Cierra la conexión a la base de datos"""
        if self._connection is not None and self._connection.is_connected():
            self._connection.close()
            logger.info("Conexión a MySQL cerrada")
            self._connection = None
    
    def execute_query(self, query, params=None, fetchall=True):
        """Ejecuta una consulta SQL y retorna los resultados"""
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)
        
        try:
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith(('SELECT', 'SHOW')):
                if fetchall:
                    return cursor.fetchall()
                else:
                    return cursor.fetchone()
            else:
                connection.commit()
                return cursor.lastrowid
                
        except Error as e:
            logger.error(f"Error al ejecutar consulta: {e}")
            if not query.strip().upper().startswith(('SELECT', 'SHOW')):
                connection.rollback()
            raise
        finally:
            cursor.close()
    
    def execute_many(self, query, params_list):
        """Ejecuta una consulta SQL múltiples veces con diferentes parámetros"""
        connection = self.connect()
        cursor = connection.cursor()
        
        try:
            cursor.executemany(query, params_list)
            connection.commit()
            return cursor.lastrowid
        except Error as e:
            logger.error(f"Error al ejecutar consulta múltiple: {e}")
            connection.rollback()
            raise
        finally:
            cursor.close()
    
    def test_connection(self):
        """Prueba la conexión a la base de datos"""
        try:
            connection = self.connect()
            if connection.is_connected():
                return True
            return False
        except:
            return False