"""
Script principal para el sistema de registro de pesajes
"""
import sys
import os
import logging
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QFile
from src.ui.main_window import MainWindow
from controllers.pesaje_controller import PesajeController
from database.db_connector import DatabaseConnector

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger('main')

def verificar_conexion_bd():
    """Verifica la conexión a la base de datos"""
    db = DatabaseConnector()
    return db.test_connection()

def main():
    """Función principal"""
    # Crear directorios necesarios
    os.makedirs("exports", exist_ok=True)
    
    # Configurar la aplicación
    app = QApplication(sys.argv)
    app.setApplicationName("Sistema de Registro de Pesajes")
    
    # Verificar y preparar la base de datos
    if not verificar_conexion_bd():
        QMessageBox.critical(
            None,
            "Error de conexión",
            "No se pudo conectar a la base de datos MySQL.\n"
            "Verifique la configuración en config/db_config.py",
            QMessageBox.Ok
        )
        return 1
    
    # Inicializar controlador
    controller = PesajeController()
    
    # Crear y mostrar ventana principal
    main_window = MainWindow(controller)
    main_window.setWindowTitle("Sistema de Registro de Pesajes - Carnicería")
    main_window.show()
    
    # Ejecutar la aplicación
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())