# Aplicación de Registro de Pesajes para Carnicería

Esta aplicación de escritorio está diseñada para registrar los pesajes realizados por carniceros en una carnicería de supermercado. Permite leer etiquetas de balanza, registrar vendedores y almacenar los registros en una base de datos local.

## Características

- Interfaz gráfica intuitiva desarrollada con PySide6
- Lectura de etiquetas de balanza (código de producto y peso)
- Registro de vendedor
- Almacenamiento de registros en base de datos SQLite
- Visualización de registros anteriores en forma de tabla
- Filtros por fecha o vendedor
- Exportación de registros a archivo CSV
- Visualización de estadísticas de ventas por vendedor

## Requisitos

- Python 3.6+
- PySide6 6.4.0+

## Instalación

1. Clone este repositorio:
```bash
git clone https://github.com/usuario/carniceria-app.git
cd carniceria-app
```

2. Instale las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecute la aplicación:
```bash
python src/main.py
```

## Estructura del Proyecto

```
carniceria_app/
├── assets/             # Recursos (iconos, estilos)
├── data/               # Base de datos
├── src/                # Código fuente
│   ├── controllers/    # Controladores de la aplicación
│   ├── ui/             # Archivos de interfaz de usuario
│   ├── database.py     # Manejo de base de datos
│   ├── models.py       # Modelos de datos
│   └── main.py         # Punto de entrada
├── requirements.txt    # Dependencias
└── README.md           # Este archivo
```

## Uso

1. Inicie la aplicación
2. Introduzca el código de vendedor y haga clic en "Establecer Vendedor"
3. Para registrar un pesaje, puede:
   - Introducir manualmente el código de producto y peso
   - Leer una etiqueta de balanza con el formato "CODIGO:PESO"
4. Visualice los registros en la pestaña "Historial"
5. Filtre los registros por vendedor o fechas
6. Exporte los datos a CSV cuando sea necesario
7. Consulte estadísticas por vendedor en la pestaña "Estadísticas"

## Compilación de archivos UI

Si modifica los archivos UI, necesitará compilarlos:

```bash
pyside6-uic src/ui/main_window.ui -o src/ui/ui_main_window.py
```

## Licencia

Este proyecto está licenciado bajo la licencia MIT.