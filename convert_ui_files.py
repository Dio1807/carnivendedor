#!/usr/bin/env python
import os
import subprocess
import sys

def convert_ui_files():
    """
    Convierte archivos .ui generados con Qt Designer a archivos Python
    """
    ui_dir = os.path.join(os.path.dirname(__file__), "src", "ui")
    
    # Buscar todos los archivos .ui
    ui_files = [f for f in os.listdir(ui_dir) if f.endswith('.ui')]
    
    for ui_file in ui_files:
        ui_path = os.path.join(ui_dir, ui_file)
        output_path = os.path.join(ui_dir, f"ui_{os.path.splitext(ui_file)[0]}.py")
        
        try:
            # Ejecutar el comando pyside6-uic
            subprocess.run(
                ["pyside6-uic", ui_path, "-o", output_path], 
                check=True
            )
            print(f"Convertido con éxito: {ui_file} -> {os.path.basename(output_path)}")
        except subprocess.CalledProcessError as e:
            print(f"Error al convertir {ui_file}: {e}")
            sys.exit(1)
        except FileNotFoundError:
            print("Error: pyside6-uic no encontrado. Asegúrese de tener PySide6 instalado.")
            sys.exit(1)

if __name__ == "__main__":
    convert_ui_files()