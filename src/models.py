from datetime import datetime

class Pesaje:
    def __init__(self, id=None, codigo_producto=None, nombre_producto=None, peso=None, 
                 codigo_vendedor=None, nombre_vendedor=None, fecha_hora=None):
        self.id = id
        self.codigo_producto = codigo_producto
        self.nombre_producto = nombre_producto  # Añadido para mostrar el nombre del producto
        self.peso = peso
        self.codigo_vendedor = codigo_vendedor
        self.nombre_vendedor = nombre_vendedor  # Añadido para mostrar el nombre del vendedor
        self.fecha_hora = fecha_hora if fecha_hora else datetime.now().isoformat()
    
    @classmethod
    def from_db_row(cls, row):
        """Crear un objeto Pesaje a partir de una fila de la base de datos"""
        # Adaptar según la estructura real de tu base de datos
        return cls(
            id=row[0], 
            codigo_producto=row[1], 
            nombre_producto=row[2] if len(row) > 2 else "Desconocido",
            peso=row[3] if len(row) > 3 else row[2],  # Adaptado para compatibilidad
            codigo_vendedor=row[4] if len(row) > 4 else row[3], 
            nombre_vendedor=row[5] if len(row) > 5 else "Desconocido",
            fecha_hora=row[6] if len(row) > 6 else row[4]
        )
    
    def to_dict(self):
        """Convertir el objeto a un diccionario"""
        return {
            'id': self.id,
            'codigo_producto': self.codigo_producto,
            'nombre_producto': self.nombre_producto,
            'peso': self.peso,
            'codigo_vendedor': self.codigo_vendedor,
            'nombre_vendedor': self.nombre_vendedor,
            'fecha_hora': self.fecha_hora
        }

class Producto:
    def __init__(self, codigo=None, nombre=None, descripcion=None):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion

class Vendedor:
    def __init__(self, codigo=None, nombre=None, apellido=None):
        self.codigo = codigo
        self.nombre = nombre
        self.apellido = apellido
        
    @property
    def nombre_completo(self):
        if self.nombre and self.apellido:
            return f"{self.nombre} {self.apellido}"
        return self.nombre or self.apellido or "Desconocido"