"""
Controlador para la lógica de negocio relacionada con los pesajes
"""
import csv
import logging
from datetime import datetime
from PySide6.QtCore import QObject, Signal
from models.repository import ProductoRepository, VendedorRepository, PesajeRepository

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('pesaje_controller')

class PesajeController(QObject):
    """Controlador para la gestión de pesajes"""
    
    # Señales para comunicación con la UI
    pesaje_guardado = Signal(int)  # Emite el ID del pesaje guardado
    pesajes_actualizados = Signal(list)  # Emite lista de pesajes
    estadisticas_actualizadas = Signal(list)  # Emite lista de estadísticas
    exportacion_completada = Signal(str)  # Emite la ruta del archivo exportado
    producto_encontrado = Signal(object)  # Emite datos del producto encontrado
    vendedor_encontrado = Signal(object)  # Emite datos del vendedor encontrado
    error_ocurrido = Signal(str)  # Emite mensaje de error
    
    def __init__(self):
        super().__init__()
        self.producto_repo = ProductoRepository()
        self.vendedor_repo = VendedorRepository()
        self.pesaje_repo = PesajeRepository()
    
    def buscar_producto_por_codigo(self, codigo):
        """Busca un producto por su código de barra"""
        try:
            producto = self.producto_repo.get_by_codigo(codigo)
            if producto:
                self.producto_encontrado.emit(producto)
            else:
                self.error_ocurrido.emit(f"No se encontró un producto con el código: {codigo}")
        except Exception as e:
            logger.error(f"Error al buscar producto: {e}")
            self.error_ocurrido.emit(f"Error al buscar producto: {str(e)}")
    
    def buscar_vendedor_por_codigo(self, codigo):
        """Busca un vendedor por su código"""
        try:
            vendedor = self.vendedor_repo.get_by_codigo(codigo)
            if vendedor:
                self.vendedor_encontrado.emit(vendedor)
            else:
                self.error_ocurrido.emit(f"No se encontró un vendedor con el código: {codigo}")
        except Exception as e:
            logger.error(f"Error al buscar vendedor: {e}")
            self.error_ocurrido.emit(f"Error al buscar vendedor: {str(e)}")
    
    def registrar_pesaje(self, codigo_producto, peso, codigo_vendedor, observaciones=None):
        """Registra un nuevo pesaje"""
        try:
            # Verificar que el producto exista
            producto = self.producto_repo.get_by_codigo(codigo_producto)
            if not producto:
                self.error_ocurrido.emit(f"No se encontró un producto con el código: {codigo_producto}")
                return
            
            # Verificar que el vendedor exista
            vendedor = self.vendedor_repo.get_by_codigo(codigo_vendedor)
            if not vendedor:
                self.error_ocurrido.emit(f"No se encontró un vendedor con el código: {codigo_vendedor}")
                return
            
            # Registrar el pesaje
            pesaje_id = self.pesaje_repo.create(
                codigo_producto, 
                peso, 
                codigo_vendedor, 
                precio_kg=producto.get('precio_kg'),
                observaciones=observaciones
            )
            
            # Emitir señal de éxito
            self.pesaje_guardado.emit(pesaje_id)
            
            # Actualizar la lista de pesajes recientes
            self.cargar_pesajes_recientes()
            
        except Exception as e:
            logger.error(f"Error al registrar pesaje: {e}")
            self.error_ocurrido.emit(f"Error al registrar pesaje: {str(e)}")
    
    def cargar_pesajes_recientes(self, limit=10):
        """Carga los pesajes más recientes"""
        try:
            pesajes = self.pesaje_repo.get_all(limit=limit)
            self.pesajes_actualizados.emit(pesajes)
        except Exception as e:
            logger.error(f"Error al cargar pesajes recientes: {e}")
            self.error_ocurrido.emit(f"Error al cargar pesajes recientes: {str(e)}")
    
    def cargar_pesajes_por_fecha(self, fecha_desde, fecha_hasta):
        """Carga pesajes en un rango de fechas"""
        try:
            pesajes = self.pesaje_repo.get_by_fechas(fecha_desde, fecha_hasta)
            self.pesajes_actualizados.emit(pesajes)
        except Exception as e:
            logger.error(f"Error al cargar pesajes por fecha: {e}")
            self.error_ocurrido.emit(f"Error al cargar pesajes por fecha: {str(e)}")
    
    def cargar_pesajes_por_vendedor(self, codigo_vendedor, limit=100):
        """Carga pesajes de un vendedor específico"""
        try:
            pesajes = self.pesaje_repo.get_by_vendedor(codigo_vendedor, limit=limit)
            self.pesajes_actualizados.emit(pesajes)
        except Exception as e:
            logger.error(f"Error al cargar pesajes por vendedor: {e}")
            self.error_ocurrido.emit(f"Error al cargar pesajes por vendedor: {str(e)}")
    
    def cargar_estadisticas(self, fecha_desde=None, fecha_hasta=None):
        """Carga estadísticas de pesajes por vendedor"""
        try:
            estadisticas = self.pesaje_repo.get_estadisticas_vendedores(
                fecha_desde=fecha_desde, 
                fecha_hasta=fecha_hasta
            )
            self.estadisticas_actualizadas.emit(estadisticas)
        except Exception as e:
            logger.error(f"Error al cargar estadísticas: {e}")
            self.error_ocurrido.emit(f"Error al cargar estadísticas: {str(e)}")
    
    def exportar_a_csv(self, ruta_archivo, fecha_desde=None, fecha_hasta=None):
        """Exporta los pesajes a un archivo CSV"""
        try:
            # Obtener los datos a exportar
            if fecha_desde and fecha_hasta:
                pesajes = self.pesaje_repo.get_by_fechas(fecha_desde, fecha_hasta)
            else:
                pesajes = self.pesaje_repo.get_all(limit=1000)  # Limitar a 1000 registros por defecto
            
            if not pesajes:
                self.error_ocurrido.emit("No hay datos para exportar")
                return
            
            # Escribir al archivo CSV
            with open(ruta_archivo, 'w', newline='', encoding='utf-8') as csvfile:
                # Definir las columnas
                fieldnames = [
                    'ID', 'Fecha', 'Código Producto', 'Producto', 
                    'Peso (kg)', 'Código Vendedor', 'Vendedor', 
                    'Precio/kg', 'Total', 'Observaciones'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for pesaje in pesajes:
                    # Formatear fecha
                    fecha_hora = datetime.fromisoformat(str(pesaje['fecha_hora']))
                    fecha_formateada = fecha_hora.strftime("%d/%m/%Y %H:%M")
                    
                    # Escribir fila
                    writer.writerow({
                        'ID': pesaje['id'],
                        'Fecha': fecha_formateada,
                        'Código Producto': pesaje['codigo_producto'],
                        'Producto': pesaje['nombre_producto'],
                        'Peso (kg)': f"{pesaje['peso']:.2f}",
                        'Código Vendedor': pesaje['codigo_vendedor'],
                        'Vendedor': pesaje['nombre_vendedor'],
                        'Precio/kg': f"{pesaje['precio_kg']:.2f}" if pesaje['precio_kg'] else '',
                        'Total': f"{pesaje['total']:.2f}" if pesaje['total'] else '',
                        'Observaciones': pesaje['observaciones'] or ''
                    })
            
            # Emitir señal de éxito
            self.exportacion_completada.emit(ruta_archivo)
            
        except Exception as e:
            logger.error(f"Error al exportar a CSV: {e}")
            self.error_ocurrido.emit(f"Error al exportar a CSV: {str(e)}")