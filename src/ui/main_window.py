import os
from datetime import datetime
from PySide6.QtWidgets import (
    QMainWindow, QMessageBox, QFileDialog, 
    QTableView, QPushButton, QLineEdit, 
    QDoubleSpinBox, QDateEdit, QLabel
)
from PySide6.QtCore import Qt, QDate, Slot, QSortFilterProxyModel
from PySide6.QtGui import QStandardItemModel, QStandardItem
from .ui_main_window import Ui_MainWindow  # Este archivo se generará automáticamente desde el .ui

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.controller = controller
        
        # Modelos para las tablas
        self.modelo_registros = QStandardItemModel(0, 4, self)
        self.modelo_registros.setHorizontalHeaderLabels(["Fecha", "Producto", "Peso", "Vendedor"])
        self.ui.tableView_registros.setModel(self.modelo_registros)
        
        self.modelo_historial = QStandardItemModel(0, 6, self)
        self.modelo_historial.setHorizontalHeaderLabels(["ID", "Fecha", "Producto", "Peso", "Código V", "Vendedor"])
        self.ui.tableView_pesajes.setModel(self.modelo_historial)
        
        self.modelo_estadisticas = QStandardItemModel(0, 4, self)
        self.modelo_estadisticas.setHorizontalHeaderLabels(["Código", "Vendedor", "Total Pesajes", "Peso Total", "Peso Promedio"])
        self.ui.tableView_estadisticas.setModel(self.modelo_estadisticas)
        
        # Configurar fechas por defecto
        hoy = QDate.currentDate()
        self.ui.dateEdit_desde.setDate(hoy.addDays(-30))  # 30 días atrás
        self.ui.dateEdit_hasta.setDate(hoy)
        
        # Conectar señales del controlador
        self.controller.pesaje_guardado.connect(self.on_pesaje_guardado)
        self.controller.pesajes_actualizados.connect(self.on_pesajes_actualizados)
        self.controller.estadisticas_actualizadas.connect(self.on_estadisticas_actualizadas)
        self.controller.exportacion_completada.connect(self.on_exportacion_completada)
        self.controller.producto_encontrado.connect(self.on_producto_encontrado)
        self.controller.vendedor_encontrado.connect(self.on_vendedor_encontrado)
        self.controller.error_ocurrido.connect(self.on_error_ocurrido)
        
        # Conectar señales de la UI
        self.ui.lineEdit_codigo_barra.returnPressed.connect(self.on_codigo_barra_entered)
        self.ui.lineEdit_codigo_vendedor.returnPressed.connect(self.on_codigo_vendedor_entered)
        self.ui.pushButton_guardar.clicked.connect(self.on_guardar_clicked)
        self.ui.pushButton_limpiar.clicked.connect(self.on_limpiar_clicked)
        self.ui.pushButton_filtrar.clicked.connect(self.on_filtrar_clicked)
        self.ui.pushButton_exportar.clicked.connect(self.on_exportar_clicked)
        self.ui.pushButton_actualizar_estadisticas.clicked.connect(self.on_actualizar_estadisticas_clicked)
        self.ui.actionSalir.triggered.connect(self.close)
        self.ui.actionAcerca_de.triggered.connect(self.on_acerca_de)

        # Conectar señal de filtrado prueba
        self.ui.tabWidget.currentChanged.connect(self.on_tab_changed)

        
        # Configuraciones iniciales de la UI
        self.ui.tabWidget.setCurrentIndex(0)  # Comenzar en la pestaña de registro
        
        # Cargar datos iniciales
        self.cargar_datos_iniciales()
    
    def cargar_datos_iniciales(self):
        """Cargar datos iniciales en la UI"""
        # Cargar pesajes recientes en la tabla de registros
        self.controller.cargar_pesajes_recientes()
        
        # Preparar la fecha de hoy
        self.ui.lineEdit_codigo_barra.setFocus()  # Poner el foco en el campo de código de barra
    
    # ===== SLOTS PARA EVENTOS DE LA UI =====
    
    @Slot()
    def on_codigo_barra_entered(self):
        """Manejar evento cuando se presiona Enter en el campo de código de barra"""
        codigo_completo = self.ui.lineEdit_codigo_barra.text().strip()
    
    # Verificar si el código tiene exactamente 13 dígitos
        if len(codigo_completo) == 13 and codigo_completo.isdigit():
        # Extraer código de producto (primeros 7 dígitos)
            codigo_producto = codigo_completo[:7]
        # Extraer información de peso (últimos 6 dígitos)
            info_peso = codigo_completo[7:]
        # Los primeros 2 dígitos son kg (parte entera)
        # Los últimos 4 dígitos son gramos (parte decimal)
            kg = int(info_peso[:2])
            g = int(info_peso[2:])
        # Calcular el peso en kg (kg + g/10000)
            peso = kg + (g / 10000)
        # Buscar el producto y establecer el peso automáticamente
            self.controller.buscar_producto_por_codigo(codigo_producto)
        # Establecer el peso calculado en el campo de peso
            self.ui.lineEdit_peso.setText(f"{peso:.4f}")
        else:
            self.mostrar_error("El código de barras debe tener exactamente 13 dígitos numéricos")
    
    @Slot()
    def on_codigo_vendedor_entered(self):
        """Manejar evento cuando se presiona Enter en el campo de código de vendedor"""
        codigo = self.ui.lineEdit_codigo_vendedor.text().strip()
        if codigo:
            self.controller.buscar_vendedor_por_codigo(codigo)
        else:
            self.mostrar_error("Debe ingresar un código de vendedor válido")
    
    @Slot()
    def on_guardar_clicked(self):
        """Manejar evento para guardar el registro actual"""
        codigo_completo = self.ui.lineEdit_codigo_barra.text().strip()
        nombre_producto = self.ui.lineEdit_producto.text().strip()
        peso_str = self.ui.lineEdit_peso.text().strip()
        codigo_vendedor = self.ui.lineEdit_codigo_vendedor.text().strip()
        nombre_vendedor = self.ui.lineEdit_vendedor.text().strip()
    
    # Validaciones
        if not codigo_completo:
            self.mostrar_error("Debe escanear o ingresar un código de producto")
            return
    
    # Extraer solo los primeros 7 dígitos como código de producto
        if len(codigo_completo) == 13 and codigo_completo.isdigit():
            codigo_producto = codigo_completo[:7]
        else:
            codigo_producto = codigo_completo  # Si no tiene 13 dígitos, usar el código completo
    
        if not nombre_producto:
            self.mostrar_error("El producto no es válido")
            return
    
        try:
            peso = float(peso_str)
        except ValueError:
            self.mostrar_error("El peso no es válido")
            return
    
        if not codigo_vendedor:
            self.mostrar_error("Debe ingresar un código de vendedor")
            return
    
        if not nombre_vendedor:
            self.mostrar_error("El vendedor no es válido")
            return
    
    # Mostrar confirmación
        confirmacion = QMessageBox.question(
            self,
            "Confirmar registro",
            f"¿Desea guardar el siguiente registro?\n\n"
            f"Producto: {nombre_producto}\n"
            f"Peso: {peso} kg\n"
            f"Vendedor: {nombre_vendedor}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
    
        if confirmacion == QMessageBox.Yes:
            # Registrar el pesaje con el código de producto correcto (7 dígitos)
            self.controller.registrar_pesaje(codigo_producto, peso, codigo_vendedor)
    
    @Slot()
    def on_limpiar_clicked(self):
        """Limpiar todos los campos del formulario"""
        self.ui.lineEdit_codigo_barra.clear()
        self.ui.lineEdit_producto.clear()
        self.ui.lineEdit_peso.clear()
        self.ui.lineEdit_codigo_vendedor.clear()
        self.ui.lineEdit_vendedor.clear()
        self.ui.lineEdit_codigo_barra.setFocus()
    
    @Slot()
    def on_filtrar_clicked(self):
        """Aplicar filtros en la pestaña de historial"""
        codigo_vendedor = self.ui.lineEdit_filtro_vendedor.text().strip()
        fecha_desde = self.ui.dateEdit_desde.date().toString("yyyy-MM-dd")
        fecha_hasta = self.ui.dateEdit_hasta.date().toString("yyyy-MM-dd")
        
        # Si hay código de vendedor, filtramos por vendedor
        if codigo_vendedor:
            self.controller.cargar_pesajes_por_vendedor(codigo_vendedor)
        else:
            # Filtrar por fechas
            self.controller.cargar_pesajes_por_fecha(fecha_desde, fecha_hasta + " 23:59:59")
    
    @Slot()
    def on_tab_changed(self, index):
    # Compara si la pestaña activa es tab_historial
        if self.ui.tabWidget.widget(index) == self.ui.tab_historial:
            self.on_filtrar_clicked()

    @Slot()
    def on_exportar_clicked(self):
        """Exportar datos a un archivo CSV"""
        ruta_archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar a CSV",
            os.path.expanduser("~/pesajes_export.csv"),
            "Archivos CSV (*.csv)"
        )
        
        if ruta_archivo:
            self.controller.exportar_a_csv(ruta_archivo)
    
    @Slot()
    def on_actualizar_estadisticas_clicked(self):
        """Actualizar las estadísticas de vendedores"""
        self.controller.cargar_estadisticas()
    
    @Slot()
    def on_acerca_de(self):
        """Mostrar información acerca del programa"""
        QMessageBox.about(
            self,
            "Acerca de Registro de Pesajes",
            "Sistema de Registro de Pesajes para Carnicería\n\n"
            "Versión 1.0\n\n"
            "© 2025 - Todos los derechos reservados"
        )
    
    # ===== SLOTS PARA SEÑALES DEL CONTROLADOR =====
    
    @Slot(int)
    def on_pesaje_guardado(self, pesaje_id):
        """Manejar evento cuando se guarda un pesaje correctamente"""
        QMessageBox.information(
            self,
            "Registro guardado",
            f"Registro de pesaje guardado correctamente con ID: {pesaje_id}",
            QMessageBox.Ok
        )
        # Limpiar el formulario después de guardar
        self.on_limpiar_clicked()
    
    @Slot(list)
    def on_pesajes_actualizados(self, pesajes):
        """Actualizar la tabla con los pesajes cargados"""
        # Determinar qué tabla actualizar según la pestaña activa
        if self.ui.tabWidget.currentIndex() == 0:  # Pestaña Registro
            self.actualizar_tabla_registros(pesajes)
        else:  # Pestaña Historial
            self.actualizar_tabla_historial(pesajes)
    
    @Slot(list)
    def on_estadisticas_actualizadas(self, estadisticas):
        """Actualizar la tabla con las estadísticas de vendedores"""
        self.modelo_estadisticas.setRowCount(0)  # Limpiar la tabla
        
        for row, est in enumerate(estadisticas):
            self.modelo_estadisticas.insertRow(row)
            self.modelo_estadisticas.setItem(row, 0, QStandardItem(est["codigo_vendedor"]))
            self.modelo_estadisticas.setItem(row, 1, QStandardItem(est["nombre_vendedor"]))
            self.modelo_estadisticas.setItem(row, 2, QStandardItem(str(est["total_pesajes"])))
            self.modelo_estadisticas.setItem(row, 3, QStandardItem(f"{est['peso_total']:.2f} kg"))
            self.modelo_estadisticas.setItem(row, 4, QStandardItem(f"{est['peso_promedio']:.2f} kg"))
    
    @Slot(str)
    def on_exportacion_completada(self, ruta_archivo):
        """Manejar evento cuando se completa la exportación"""
        QMessageBox.information(
            self,
            "Exportación completada",
            f"Los datos se han exportado correctamente a:\n{ruta_archivo}",
            QMessageBox.Ok
        )
    
    @Slot(object)
    def on_producto_encontrado(self, producto):
        """Actualizar los campos con la información del producto encontrado"""
        if producto:
            self.ui.lineEdit_producto.setText(producto["nombre"])
                
        # Mover el foco al campo de código de vendedor
            self.ui.lineEdit_codigo_vendedor.setFocus()
    
    @Slot(object)
    def on_vendedor_encontrado(self, vendedor):
        """Actualizar los campos con la información del vendedor encontrado"""
        if vendedor:
            nombre_completo = f"{vendedor['nombre']} {vendedor['apellido']}".strip()
            self.ui.lineEdit_vendedor.setText(nombre_completo)
            self.ui.pushButton_guardar.setDefault(True)
            self.ui.pushButton_guardar.setFocus()
    
    @Slot(str)
    def on_error_ocurrido(self, mensaje):
        """Mostrar mensaje de error"""
        self.mostrar_error(mensaje)
    
    # ===== MÉTODOS AUXILIARES =====
    
    def actualizar_tabla_registros(self, pesajes):
        """Actualizar la tabla de registros recientes"""
        self.modelo_registros.setRowCount(0)  # Limpiar la tabla
        
        for row, pesaje in enumerate(pesajes):
            self.modelo_registros.insertRow(row)
            
            # Formatear la fecha/hora
            fecha_hora = datetime.fromisoformat(str(pesaje['fecha_hora']))
            fecha_formateada = fecha_hora.strftime("%d/%m/%Y %H:%M")
            
            # Poblar la tabla
            self.modelo_registros.setItem(row, 0, QStandardItem(fecha_formateada))
            self.modelo_registros.setItem(row, 1, QStandardItem(pesaje['nombre_producto']))
            self.modelo_registros.setItem(row, 2, QStandardItem(f"{pesaje['peso']:.2f} kg"))
            self.modelo_registros.setItem(row, 3, QStandardItem(pesaje['nombre_vendedor']))
    
    def actualizar_tabla_historial(self, pesajes):
        """Actualizar la tabla de historial completo"""
        self.modelo_historial.setRowCount(0)  # Limpiar la tabla
        
        for row, pesaje in enumerate(pesajes):
            self.modelo_historial.insertRow(row)
            
            # Formatear la fecha/hora
            fecha_hora = datetime.fromisoformat(str(pesaje['fecha_hora']))
            fecha_formateada = fecha_hora.strftime("%d/%m/%Y %H:%M")
            
            # Poblar la tabla
            self.modelo_historial.setItem(row, 0, QStandardItem(str(pesaje['id'])))
            self.modelo_historial.setItem(row, 1, QStandardItem(fecha_formateada))
            self.modelo_historial.setItem(row, 2, QStandardItem(pesaje['nombre_producto']))
            self.modelo_historial.setItem(row, 3, QStandardItem(f"{pesaje['peso']:.2f} kg"))
            self.modelo_historial.setItem(row, 4, QStandardItem(pesaje['codigo_vendedor']))
            self.modelo_historial.setItem(row, 5, QStandardItem(pesaje['nombre_vendedor']))
    
    def mostrar_error(self, mensaje):
        """Mostrar un diálogo de error"""
        QMessageBox.critical(
            self,
            "Error",
            mensaje,
            QMessageBox.Ok
        )