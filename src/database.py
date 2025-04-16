import sqlite3
import os
from datetime import datetime
from pathlib import Path

class Database:
    def __init__(self, db_path="data/pesajes.db"):
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Crear las tablas necesarias si no existen"""
        # Tabla de vendedores
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendedores (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT
        )
        ''')
        
        # Tabla de productos
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            descripcion TEXT
        )
        ''')
        
        # Tabla de pesajes
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS pesajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_producto TEXT NOT NULL,
            peso REAL NOT NULL,
            codigo_vendedor TEXT NOT NULL,
            fecha_hora TIMESTAMP NOT NULL,
            FOREIGN KEY (codigo_producto) REFERENCES productos(codigo),
            FOREIGN KEY (codigo_vendedor) REFERENCES vendedores(codigo)
        )
        ''')
        
        # Insertar algunos datos de ejemplo si las tablas están vacías
        self.cursor.execute("SELECT COUNT(*) FROM vendedores")
        if self.cursor.fetchone()[0] == 0:
            self.insertar_datos_ejemplo()
            
        self.conn.commit()
    
    def insertar_datos_ejemplo(self):
        """Insertar algunos datos de ejemplo para vendedores y productos"""
        # Vendedores de ejemplo
        vendedores = [
            ('V001', 'Juan', 'Pérez'),
            ('V002', 'María', 'González'),
            ('V003', 'Carlos', 'Rodríguez')
        ]
        self.cursor.executemany(
            "INSERT INTO vendedores (codigo, nombre, apellido) VALUES (?, ?, ?)",
            vendedores
        )
        
        # Productos de ejemplo
        productos = [
            ('P001', 'Filete de Res', 'Corte premium de res'),
            ('P002', 'Chuleta de Cerdo', 'Chuleta ahumada'),
            ('P003', 'Pollo Entero', 'Pollo limpio sin vísceras'),
            ('P004', 'Costillas BBQ', 'Costillas marinadas para BBQ'),
            ('P005', 'Chorizo', 'Chorizo casero')
        ]
        self.cursor.executemany(
            "INSERT INTO productos (codigo, nombre, descripcion) VALUES (?, ?, ?)",
            productos
        )
        
        self.conn.commit()
    
    def registrar_pesaje(self, codigo_producto, peso, codigo_vendedor):
        """Registrar un nuevo pesaje en la base de datos"""
        fecha_hora = datetime.now().isoformat()
        
        # Verificamos que exista el producto
        self.cursor.execute("SELECT codigo FROM productos WHERE codigo = ?", (codigo_producto,))
        if not self.cursor.fetchone():
            raise ValueError(f"El producto con código {codigo_producto} no existe")
        
        # Verificamos que exista el vendedor
        self.cursor.execute("SELECT codigo FROM vendedores WHERE codigo = ?", (codigo_vendedor,))
        if not self.cursor.fetchone():
            raise ValueError(f"El vendedor con código {codigo_vendedor} no existe")
        
        # Registramos el pesaje
        self.cursor.execute(
            "INSERT INTO pesajes (codigo_producto, peso, codigo_vendedor, fecha_hora) VALUES (?, ?, ?, ?)",
            (codigo_producto, peso, codigo_vendedor, fecha_hora)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def buscar_producto_por_codigo(self, codigo):
        """Buscar un producto por su código"""
        self.cursor.execute(
            "SELECT codigo, nombre, descripcion FROM productos WHERE codigo = ?", 
            (codigo,)
        )
        producto = self.cursor.fetchone()
        if producto:
            return dict(producto)
        return None
    
    def buscar_vendedor_por_codigo(self, codigo):
        """Buscar un vendedor por su código"""
        self.cursor.execute(
            "SELECT codigo, nombre, apellido FROM vendedores WHERE codigo = ?", 
            (codigo,)
        )
        vendedor = self.cursor.fetchone()
        if vendedor:
            return dict(vendedor)
        return None
    
    def obtener_pesajes_recientes(self, limit=10):
        """Obtener los pesajes más recientes con información detallada"""
        self.cursor.execute("""
            SELECT 
                p.id, p.codigo_producto, prod.nombre AS nombre_producto, 
                p.peso, p.codigo_vendedor, 
                (v.nombre || ' ' || v.apellido) AS nombre_vendedor,
                p.fecha_hora
            FROM 
                pesajes p
                JOIN productos prod ON p.codigo_producto = prod.codigo
                JOIN vendedores v ON p.codigo_vendedor = v.codigo
            ORDER BY 
                p.fecha_hora DESC
            LIMIT ?
        """, (limit,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def obtener_pesajes(self, limit=100, offset=0):
        """Obtener los últimos pesajes registrados con información detallada"""
        self.cursor.execute("""
            SELECT 
                p.id, p.codigo_producto, prod.nombre AS nombre_producto, 
                p.peso, p.codigo_vendedor, 
                (v.nombre || ' ' || v.apellido) AS nombre_vendedor,
                p.fecha_hora
            FROM 
                pesajes p
                JOIN productos prod ON p.codigo_producto = prod.codigo
                JOIN vendedores v ON p.codigo_vendedor = v.codigo
            ORDER BY 
                p.fecha_hora DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def obtener_pesajes_por_vendedor(self, codigo_vendedor, limit=100):
        """Obtener los pesajes de un vendedor específico"""
        self.cursor.execute("""
            SELECT 
                p.id, p.codigo_producto, prod.nombre AS nombre_producto, 
                p.peso, p.codigo_vendedor, 
                (v.nombre || ' ' || v.apellido) AS nombre_vendedor,
                p.fecha_hora
            FROM 
                pesajes p
                JOIN productos prod ON p.codigo_producto = prod.codigo
                JOIN vendedores v ON p.codigo_vendedor = v.codigo
            WHERE 
                p.codigo_vendedor = ?
            ORDER BY 
                p.fecha_hora DESC
            LIMIT ?
        """, (codigo_vendedor, limit))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def obtener_pesajes_por_fecha(self, fecha_inicio, fecha_fin):
        """Obtener los pesajes entre dos fechas"""
        self.cursor.execute("""
            SELECT 
                p.id, p.codigo_producto, prod.nombre AS nombre_producto, 
                p.peso, p.codigo_vendedor, 
                (v.nombre || ' ' || v.apellido) AS nombre_vendedor,
                p.fecha_hora
            FROM 
                pesajes p
                JOIN productos prod ON p.codigo_producto = prod.codigo
                JOIN vendedores v ON p.codigo_vendedor = v.codigo
            WHERE 
                p.fecha_hora BETWEEN ? AND ?
            ORDER BY 
                p.fecha_hora DESC
        """, (fecha_inicio, fecha_fin))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def obtener_estadisticas_vendedor(self):
        """Obtener estadísticas de pesajes por vendedor"""
        self.cursor.execute("""
            SELECT 
                v.codigo as codigo_vendedor, 
                (v.nombre || ' ' || v.apellido) AS nombre_vendedor,
                COUNT(*) as total_pesajes, 
                SUM(p.peso) as peso_total,
                AVG(p.peso) as peso_promedio
            FROM 
                pesajes p
                JOIN vendedores v ON p.codigo_vendedor = v.codigo
            GROUP BY 
                p.codigo_vendedor
            ORDER BY 
                total_pesajes DESC
        """)
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def close(self):
        """Cerrar la conexión a la base de datos"""
        if self.conn:
            self.conn.close()