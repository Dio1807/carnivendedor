import csv
from datetime import datetime
from PySide6.QtCore import QObject, Signal, Slot
from database import Database
from models import Pesaje, Producto, Vendedor

class PesajeController(QObject):
    # Señales para comunicar con la UI
    pesaje_guardado = Signal(int)  # ID del pesaje guardado
    pesajes_actualizados = Signal(list)  # Lista de pesajes
    estadisticas_actualizadas = Signal(list)  # Estadísticas por vendedor
    exportacion_completada = Signal(str)  # Ruta del archivo exportado
    producto_encontrado = Signal(object)  # Información del producto encontrado
    vendedor_encontrado = Signal(object)  # Información del vendedor encontrado
    error_ocurrido = Signal(str)  # Mensaje de error
    
    def __init__(self):
        super().__init__()
        self.db = Database()
    
    @Slot(str)
    def buscar_producto_por_codigo(self, codigo_producto):
        """Buscar un producto por su código y emitir señal con resultado"""
        try:
            producto = self.db.buscar_producto_por_codigo(codigo_producto)
            if producto:
                self.producto_encontrado.emit(producto)
            else:
                self.error_ocurrido.emit(f"Producto con código {codigo_producto} no encontrado")
        except Exception as e:
            self.error_ocurrido.emit(f"Error al buscar producto: {str(e)}")
    
    @Slot(str)
    def buscar_vendedor_por_codigo(self, codigo_vendedor):
        """Buscar un vendedor por su código y emitir señal con resultado"""
        try:
            vendedor = self.db.buscar_vendedor_por_codigo(codigo_vendedor)
            if vendedor:
                self.vendedor_encontrado.emit(vendedor)
            else:
                self.error_ocurrido.emit(f"Vendedor con código {codigo_vendedor} no encontrado")
        except Exception as e:
            self.error_ocurrido.emit(f"Error al buscar vendedor: {str(e)}")
    
    @Slot(str, float, str)
    def registrar_pesaje(self, codigo_producto, peso, codigo_vendedor):
        """Registrar un nuevo pesaje"""
        try:
            pesaje_id = self.db.registrar_pesaje(
                codigo_producto=codigo_producto,
                peso=peso,
                codigo_vendedor=codigo_vendedor
            )
            
            self.pesaje_guardado.emit(pesaje_id)
            
            # Actualizar la lista de pesajes recientes
            self.cargar_pesajes_recientes()
            
        except Exception as e:
            self.error_ocurrido.emit(f"Error al registrar pesaje: {str(e)}")
    
    @Slot()
    def cargar_pesajes_recientes(self, limit=10):
        """Cargar los pesajes más recientes"""
        try:
            pesajes = self.db.obtener_pesajes_recientes(limit)
            self.pesajes_actualizados.emit(pesajes)
        except Exception as e:
            self.error_ocurrido.emit(f"Error al cargar pesajes recientes: {str(e)}")
    
    @Slot()
    def cargar_pesajes(self, limit=100, offset=0):
        """Cargar pesajes desde la base de datos"""
        try:
            pesajes = self.db.obtener_pesajes(limit, offset)
            self.pesajes_actualizados.emit(pesajes)
        except Exception as e:
            self.error_ocurrido.emit(f"Error al cargar pesajes: {str(e)}")
    
    @Slot(str)
    def cargar_pesajes_por_vendedor(self, codigo_vendedor, limit=100):
        """Cargar pesajes de un vendedor específico"""
        try:
            pesajes = self.db.obtener_pesajes_por_vendedor(codigo_vendedor, limit)
            self.pesajes_actualizados.emit(pesajes)
        except Exception as e:
            self.error_ocurrido.emit(f"Error al cargar pesajes por vendedor: {str(e)}")
    
    @Slot(str, str)
    def cargar_pesajes_por_fecha(self, fecha_inicio, fecha_fin):
        """Cargar pesajes entre dos fechas"""
        try:
            pesajes = self.db.obtener_pesajes_por_fecha(fecha_inicio, fecha_fin)
            self.pesajes_actualizados.emit(pesajes)
        except Exception as e:
            self.error_ocurrido.emit(f"Error al cargar pesajes por fecha: {str(e)}")
    
    @Slot()
    def cargar_estadisticas(self):
        """Cargar estadísticas de vendedores"""
        try:
            estadisticas = self.db.obtener_estadisticas_vendedor()
            self.estadisticas_actualizadas.emit(estadisticas)
        except Exception as e:
            self.error_ocurrido.emit(f"Error al cargar estadísticas: {str(e)}")
    
    @Slot(str)
    def exportar_a_csv(self, ruta_archivo):
        """Exportar los pesajes a un archivo CSV"""
        try:
            pesajes = self.db.obtener_pesajes(limit=10000)  # Obtener un gran número de pesajes
            
            with open(ruta_archivo, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Código Producto', 'Producto', 'Peso', 'Código Vendedor', 'Vendedor', 'Fecha y Hora'])
                
                for pesaje in pesajes:
                    writer.writerow([
                        pesaje['id'], 
                        pesaje['codigo_producto'], 
                        pesaje['nombre_producto'],
                        pesaje['peso'], 
                        pesaje['codigo_vendedor'], 
                        pesaje['nombre_vendedor'],
                        pesaje['fecha_hora']
                    ])
            
            self.exportacion_completada.emit(ruta_archivo)
        except Exception as e:
            self.error_ocurrido.emit(f"Error al exportar a CSV: {str(e)}")
    
    def __del__(self):
        """Asegurarse de cerrar la conexión a la base de datos"""
        self.db.close()