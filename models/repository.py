"""
Repositorio para acceder a los datos de la base de datos MySQL
"""
from database.db_connector import DatabaseConnector
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('repository')

class Repository:
    """Clase base para el acceso a datos"""
    
    def __init__(self):
        self.db = DatabaseConnector()

class ProductoRepository(Repository):
    """Repositorio para gestionar los datos de productos"""
    
    def get_by_id(self, id):
        """Obtiene un producto por su ID"""
        query = "SELECT * FROM productos WHERE id = %s AND activo = TRUE"
        return self.db.execute_query(query, (id,), fetchall=False)
    
    def get_by_codigo(self, codigo):
        """Obtiene un producto por su código"""
        query = "SELECT * FROM productos WHERE codigo = %s AND activo = TRUE"
        return self.db.execute_query(query, (codigo,), fetchall=False)
    
    def get_all(self):
        """Obtiene todos los productos activos"""
        query = "SELECT * FROM productos WHERE activo = TRUE ORDER BY nombre"
        return self.db.execute_query(query)
    
    def create(self, codigo, nombre, descripcion=None, precio_kg=None):
        """Crea un nuevo producto"""
        query = """
        INSERT INTO productos (codigo, nombre, descripcion, precio_kg)
        VALUES (%s, %s, %s, %s)
        """
        return self.db.execute_query(query, (codigo, nombre, descripcion, precio_kg))
    
    def update(self, id, nombre=None, descripcion=None, precio_kg=None, activo=None):
        """Actualiza un producto existente"""
        # Construir la consulta dinámicamente basado en los campos proporcionados
        update_fields = []
        params = []
        
        if nombre is not None:
            update_fields.append("nombre = %s")
            params.append(nombre)
        
        if descripcion is not None:
            update_fields.append("descripcion = %s")
            params.append(descripcion)
        
        if precio_kg is not None:
            update_fields.append("precio_kg = %s")
            params.append(precio_kg)
        
        if activo is not None:
            update_fields.append("activo = %s")
            params.append(activo)
        
        if not update_fields:
            return None  # No hay campos para actualizar
        
        query = f"UPDATE productos SET {', '.join(update_fields)} WHERE id = %s"
        params.append(id)
        
        return self.db.execute_query(query, tuple(params))
    
    def delete(self, id):
        """Desactiva un producto (no lo elimina físicamente)"""
        query = "UPDATE productos SET activo = FALSE WHERE id = %s"
        return self.db.execute_query(query, (id,))

class VendedorRepository(Repository):
    """Repositorio para gestionar los datos de vendedores"""
    
    def get_by_id(self, id):
        """Obtiene un vendedor por su ID"""
        query = "SELECT * FROM vendedores WHERE id = %s AND activo = TRUE"
        return self.db.execute_query(query, (id,), fetchall=False)
    
    def get_by_codigo(self, codigo):
        """Obtiene un vendedor por su código"""
        query = "SELECT * FROM vendedores WHERE codigo = %s AND activo = TRUE"
        return self.db.execute_query(query, (codigo,), fetchall=False)
    
    def get_all(self):
        """Obtiene todos los vendedores activos"""
        query = "SELECT * FROM vendedores WHERE activo = TRUE ORDER BY apellido, nombre"
        return self.db.execute_query(query)
    
    def create(self, codigo, nombre, apellido, documento=None, telefono=None):
        """Crea un nuevo vendedor"""
        query = """
        INSERT INTO vendedores (codigo, nombre, apellido, documento, telefono)
        VALUES (%s, %s, %s, %s, %s)
        """
        return self.db.execute_query(query, (codigo, nombre, apellido, documento, telefono))
    
    def update(self, id, nombre=None, apellido=None, documento=None, telefono=None, activo=None):
        """Actualiza un vendedor existente"""
        # Construir la consulta dinámicamente basado en los campos proporcionados
        update_fields = []
        params = []
        
        if nombre is not None:
            update_fields.append("nombre = %s")
            params.append(nombre)
        
        if apellido is not None:
            update_fields.append("apellido = %s")
            params.append(apellido)
        
        if documento is not None:
            update_fields.append("documento = %s")
            params.append(documento)
        
        if telefono is not None:
            update_fields.append("telefono = %s")
            params.append(telefono)
        
        if activo is not None:
            update_fields.append("activo = %s")
            params.append(activo)
        
        if not update_fields:
            return None  # No hay campos para actualizar
        
        query = f"UPDATE vendedores SET {', '.join(update_fields)} WHERE id = %s"
        params.append(id)
        
        return self.db.execute_query(query, tuple(params))
    
    def delete(self, id):
        """Desactiva un vendedor (no lo elimina físicamente)"""
        query = "UPDATE vendedores SET activo = FALSE WHERE id = %s"
        return self.db.execute_query(query, (id,))

class PesajeRepository(Repository):
    """Repositorio para gestionar los datos de pesajes"""
    
    def get_by_id(self, id):
        """Obtiene un pesaje por su ID"""
        query = """
        SELECT 
            p.id, p.codigo_producto, prod.nombre AS nombre_producto,
            p.peso, p.codigo_vendedor, CONCAT(v.nombre, ' ', v.apellido) AS nombre_vendedor,
            p.fecha_hora, p.precio_kg, p.total, p.observaciones
        FROM 
            pesajes p
            JOIN productos prod ON p.codigo_producto = prod.codigo
            JOIN vendedores v ON p.codigo_vendedor = v.codigo
        WHERE 
            p.id = %s
        """
        return self.db.execute_query(query, (id,), fetchall=False)
    
    def get_all(self, limit=100):
        """Obtiene todos los pesajes con límite opcional"""
        query = """
        SELECT 
            p.id, p.codigo_producto, prod.nombre AS nombre_producto,
            p.peso, p.codigo_vendedor, CONCAT(v.nombre, ' ', v.apellido) AS nombre_vendedor,
            p.fecha_hora, p.precio_kg, p.total, p.observaciones
        FROM 
            pesajes p
            JOIN productos prod ON p.codigo_producto = prod.codigo
            JOIN vendedores v ON p.codigo_vendedor = v.codigo
        ORDER BY 
            p.fecha_hora DESC
        LIMIT %s
        """
        return self.db.execute_query(query, (limit,))
    
    # Colocar boton para cambiar de ASC A DESC EN ESTA Y LA SENTENCIA DE GET_BY_VENDEDOR
    def get_by_fechas(self, fecha_desde, fecha_hasta):
        """Obtiene pesajes entre dos fechas"""
        query = """
        SELECT 
            p.id, p.codigo_producto, prod.nombre AS nombre_producto,
            p.peso, p.codigo_vendedor, CONCAT(v.nombre, ' ', v.apellido) AS nombre_vendedor,
            p.fecha_hora, p.precio_kg, p.total, p.observaciones
        FROM 
            pesajes p
            JOIN productos prod ON p.codigo_producto = prod.codigo
            JOIN vendedores v ON p.codigo_vendedor = v.codigo
        WHERE 
            p.fecha_hora BETWEEN %s AND %s
        ORDER BY 
            p.fecha_hora ASC
        """
        return self.db.execute_query(query, (fecha_desde, fecha_hasta))
    
    def get_by_vendedor(self, codigo_vendedor, limit=100):
        """Obtiene pesajes de un vendedor específico"""
        query = """
        SELECT 
            p.id, p.codigo_producto, prod.nombre AS nombre_producto,
            p.peso, p.codigo_vendedor, CONCAT(v.nombre, ' ', v.apellido) AS nombre_vendedor,
            p.fecha_hora, p.precio_kg, p.total, p.observaciones
        FROM 
            pesajes p
            JOIN productos prod ON p.codigo_producto = prod.codigo
            JOIN vendedores v ON p.codigo_vendedor = v.codigo
        WHERE 
            p.codigo_vendedor = %s
        ORDER BY 
            p.fecha_hora ASC
        LIMIT %s
        """
        return self.db.execute_query(query, (codigo_vendedor, limit))
    
    def create(self, codigo_producto, peso, codigo_vendedor, precio_kg=None, observaciones=None):
        """Crea un nuevo registro de pesaje"""
        
        # Si no se proporciona el precio_kg, obtenerlo del producto
        if precio_kg is None:
            prod_repo = ProductoRepository()
            producto = prod_repo.get_by_codigo(codigo_producto)
            if producto:
                precio_kg = producto.get('precio_kg')
        
        query = """
        INSERT INTO pesajes (codigo_producto, peso, codigo_vendedor, precio_kg, observaciones)
        VALUES (%s, %s, %s, %s, %s)
        """
        return self.db.execute_query(query, (codigo_producto, peso, codigo_vendedor, precio_kg, observaciones))
    
    def get_estadisticas_vendedores(self, fecha_desde=None, fecha_hasta=None):
        """Obtiene estadísticas de pesajes por vendedor"""
        
        where_clause = ""
        params = []
        
        if fecha_desde and fecha_hasta:
            where_clause = "WHERE p.fecha_hora BETWEEN %s AND %s"
            params = [fecha_desde, fecha_hasta]
        
        query = f"""
        SELECT 
            v.codigo AS codigo_vendedor,
            CONCAT(v.nombre, ' ', v.apellido) AS nombre_vendedor,
            COUNT(p.id) AS total_pesajes,
            SUM(p.peso) AS peso_total,
            AVG(p.peso) AS peso_promedio,
            SUM(p.total) AS monto_total
        FROM 
            pesajes p
            JOIN vendedores v ON p.codigo_vendedor = v.codigo
        {where_clause}
        GROUP BY 
            v.codigo, v.nombre, v.apellido
        ORDER BY 
            SUM(p.peso) DESC
        """
        
        return self.db.execute_query(query, tuple(params))