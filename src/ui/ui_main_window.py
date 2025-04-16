# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDateEdit, QFormLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTabWidget, QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionSalir = QAction(MainWindow)
        self.actionSalir.setObjectName(u"actionSalir")
        self.actionAcerca_de = QAction(MainWindow)
        self.actionAcerca_de.setObjectName(u"actionAcerca_de")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_registro = QWidget()
        self.tab_registro.setObjectName(u"tab_registro")
        self.verticalLayout_2 = QVBoxLayout(self.tab_registro)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_formulario = QGroupBox(self.tab_registro)
        self.groupBox_formulario.setObjectName(u"groupBox_formulario")
        self.verticalLayout_formulario = QVBoxLayout(self.groupBox_formulario)
        self.verticalLayout_formulario.setObjectName(u"verticalLayout_formulario")
        self.horizontalLayout_codigo_barra = QHBoxLayout()
        self.horizontalLayout_codigo_barra.setObjectName(u"horizontalLayout_codigo_barra")
        self.label_codigo_barra = QLabel(self.groupBox_formulario)
        self.label_codigo_barra.setObjectName(u"label_codigo_barra")

        self.horizontalLayout_codigo_barra.addWidget(self.label_codigo_barra)

        self.lineEdit_codigo_barra = QLineEdit(self.groupBox_formulario)
        self.lineEdit_codigo_barra.setObjectName(u"lineEdit_codigo_barra")

        self.horizontalLayout_codigo_barra.addWidget(self.lineEdit_codigo_barra)


        self.verticalLayout_formulario.addLayout(self.horizontalLayout_codigo_barra)

        self.horizontalLayout_datos = QHBoxLayout()
        self.horizontalLayout_datos.setObjectName(u"horizontalLayout_datos")
        self.formLayout_datos = QFormLayout()
        self.formLayout_datos.setObjectName(u"formLayout_datos")
        self.label_producto = QLabel(self.groupBox_formulario)
        self.label_producto.setObjectName(u"label_producto")

        self.formLayout_datos.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_producto)

        self.lineEdit_producto = QLineEdit(self.groupBox_formulario)
        self.lineEdit_producto.setObjectName(u"lineEdit_producto")
        self.lineEdit_producto.setReadOnly(True)

        self.formLayout_datos.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEdit_producto)

        self.label_peso = QLabel(self.groupBox_formulario)
        self.label_peso.setObjectName(u"label_peso")

        self.formLayout_datos.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_peso)

        self.lineEdit_peso = QLineEdit(self.groupBox_formulario)
        self.lineEdit_peso.setObjectName(u"lineEdit_peso")
        self.lineEdit_peso.setReadOnly(True)

        self.formLayout_datos.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lineEdit_peso)

        self.label_codigo_vendedor = QLabel(self.groupBox_formulario)
        self.label_codigo_vendedor.setObjectName(u"label_codigo_vendedor")

        self.formLayout_datos.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_codigo_vendedor)

        self.lineEdit_codigo_vendedor = QLineEdit(self.groupBox_formulario)
        self.lineEdit_codigo_vendedor.setObjectName(u"lineEdit_codigo_vendedor")

        self.formLayout_datos.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lineEdit_codigo_vendedor)

        self.label_vendedor = QLabel(self.groupBox_formulario)
        self.label_vendedor.setObjectName(u"label_vendedor")

        self.formLayout_datos.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_vendedor)

        self.lineEdit_vendedor = QLineEdit(self.groupBox_formulario)
        self.lineEdit_vendedor.setObjectName(u"lineEdit_vendedor")
        self.lineEdit_vendedor.setReadOnly(True)

        self.formLayout_datos.setWidget(3, QFormLayout.ItemRole.FieldRole, self.lineEdit_vendedor)


        self.horizontalLayout_datos.addLayout(self.formLayout_datos)

        self.verticalLayout_botones = QVBoxLayout()
        self.verticalLayout_botones.setObjectName(u"verticalLayout_botones")
        self.pushButton_limpiar = QPushButton(self.groupBox_formulario)
        self.pushButton_limpiar.setObjectName(u"pushButton_limpiar")
        self.pushButton_limpiar.setMinimumSize(QSize(100, 40))
        self.pushButton_limpiar.setStyleSheet(u"background-color: rgb(255, 200, 150);")

        self.verticalLayout_botones.addWidget(self.pushButton_limpiar)

        self.pushButton_guardar = QPushButton(self.groupBox_formulario)
        self.pushButton_guardar.setObjectName(u"pushButton_guardar")
        self.pushButton_guardar.setMinimumSize(QSize(100, 40))
        self.pushButton_guardar.setStyleSheet(u"background-color: rgb(150, 255, 150);")

        self.verticalLayout_botones.addWidget(self.pushButton_guardar)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_botones.addItem(self.verticalSpacer)


        self.horizontalLayout_datos.addLayout(self.verticalLayout_botones)


        self.verticalLayout_formulario.addLayout(self.horizontalLayout_datos)


        self.verticalLayout_2.addWidget(self.groupBox_formulario)

        self.groupBox_tabla = QGroupBox(self.tab_registro)
        self.groupBox_tabla.setObjectName(u"groupBox_tabla")
        self.verticalLayout_tabla = QVBoxLayout(self.groupBox_tabla)
        self.verticalLayout_tabla.setObjectName(u"verticalLayout_tabla")
        self.tableView_registros = QTableView(self.groupBox_tabla)
        self.tableView_registros.setObjectName(u"tableView_registros")
        self.tableView_registros.setAlternatingRowColors(True)
        self.tableView_registros.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView_registros.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_tabla.addWidget(self.tableView_registros)


        self.verticalLayout_2.addWidget(self.groupBox_tabla)

        self.tabWidget.addTab(self.tab_registro, "")
        self.tab_historial = QWidget()
        self.tab_historial.setObjectName(u"tab_historial")
        self.verticalLayout_4 = QVBoxLayout(self.tab_historial)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_4 = QGroupBox(self.tab_historial)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_5 = QLabel(self.groupBox_4)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)

        self.lineEdit_filtro_vendedor = QLineEdit(self.groupBox_4)
        self.lineEdit_filtro_vendedor.setObjectName(u"lineEdit_filtro_vendedor")

        self.horizontalLayout_2.addWidget(self.lineEdit_filtro_vendedor)

        self.label_6 = QLabel(self.groupBox_4)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_2.addWidget(self.label_6)

        self.dateEdit_desde = QDateEdit(self.groupBox_4)
        self.dateEdit_desde.setObjectName(u"dateEdit_desde")

        self.horizontalLayout_2.addWidget(self.dateEdit_desde)

        self.label_7 = QLabel(self.groupBox_4)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_2.addWidget(self.label_7)

        self.dateEdit_hasta = QDateEdit(self.groupBox_4)
        self.dateEdit_hasta.setObjectName(u"dateEdit_hasta")

        self.horizontalLayout_2.addWidget(self.dateEdit_hasta)

        self.pushButton_filtrar = QPushButton(self.groupBox_4)
        self.pushButton_filtrar.setObjectName(u"pushButton_filtrar")

        self.horizontalLayout_2.addWidget(self.pushButton_filtrar)


        self.verticalLayout_4.addWidget(self.groupBox_4)

        self.tableView_pesajes = QTableView(self.tab_historial)
        self.tableView_pesajes.setObjectName(u"tableView_pesajes")

        self.verticalLayout_4.addWidget(self.tableView_pesajes)

        self.pushButton_exportar = QPushButton(self.tab_historial)
        self.pushButton_exportar.setObjectName(u"pushButton_exportar")

        self.verticalLayout_4.addWidget(self.pushButton_exportar)

        self.tabWidget.addTab(self.tab_historial, "")
        self.tab_estadisticas = QWidget()
        self.tab_estadisticas.setObjectName(u"tab_estadisticas")
        self.verticalLayout_5 = QVBoxLayout(self.tab_estadisticas)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_8 = QLabel(self.tab_estadisticas)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_5.addWidget(self.label_8)

        self.tableView_estadisticas = QTableView(self.tab_estadisticas)
        self.tableView_estadisticas.setObjectName(u"tableView_estadisticas")

        self.verticalLayout_5.addWidget(self.tableView_estadisticas)

        self.pushButton_actualizar_estadisticas = QPushButton(self.tab_estadisticas)
        self.pushButton_actualizar_estadisticas.setObjectName(u"pushButton_actualizar_estadisticas")

        self.verticalLayout_5.addWidget(self.pushButton_actualizar_estadisticas)

        self.tabWidget.addTab(self.tab_estadisticas, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuArchivo = QMenu(self.menubar)
        self.menuArchivo.setObjectName(u"menuArchivo")
        self.menuAyuda = QMenu(self.menubar)
        self.menuAyuda.setObjectName(u"menuAyuda")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())
        self.menuArchivo.addAction(self.actionSalir)
        self.menuAyuda.addAction(self.actionAcerca_de)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Registro de Pesajes - Carnicer\u00eda", None))
        self.actionSalir.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
        self.actionAcerca_de.setText(QCoreApplication.translate("MainWindow", u"Acerca de", None))
        self.groupBox_formulario.setTitle(QCoreApplication.translate("MainWindow", u"Datos de Pesaje", None))
        self.label_codigo_barra.setText(QCoreApplication.translate("MainWindow", u"C\u00f3digo de Barra:", None))
        self.lineEdit_codigo_barra.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Escanee o ingrese el c\u00f3digo de barra...", None))
        self.label_producto.setText(QCoreApplication.translate("MainWindow", u"Producto:", None))
        self.lineEdit_producto.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nombre del producto...", None))
        self.label_peso.setText(QCoreApplication.translate("MainWindow", u"Peso:", None))
        self.lineEdit_peso.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Peso del producto...", None))
        self.label_codigo_vendedor.setText(QCoreApplication.translate("MainWindow", u"C\u00f3digo V:", None))
        self.lineEdit_codigo_vendedor.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Ingrese c\u00f3digo de vendedor...", None))
        self.label_vendedor.setText(QCoreApplication.translate("MainWindow", u"Vendedor:", None))
        self.lineEdit_vendedor.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nombre del vendedor...", None))
        self.pushButton_limpiar.setText(QCoreApplication.translate("MainWindow", u"Limpiar", None))
        self.pushButton_guardar.setText(QCoreApplication.translate("MainWindow", u"Guardar", None))
        self.groupBox_tabla.setTitle(QCoreApplication.translate("MainWindow", u"Registros Recientes", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_registro), QCoreApplication.translate("MainWindow", u"Registro de Pesaje", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Filtros", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Vendedor:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Desde:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Hasta:", None))
        self.pushButton_filtrar.setText(QCoreApplication.translate("MainWindow", u"Filtrar", None))
        self.pushButton_exportar.setText(QCoreApplication.translate("MainWindow", u"Exportar a CSV", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_historial), QCoreApplication.translate("MainWindow", u"Historial", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Estad\u00edsticas por Vendedor:", None))
        self.pushButton_actualizar_estadisticas.setText(QCoreApplication.translate("MainWindow", u"Actualizar Estad\u00edsticas", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_estadisticas), QCoreApplication.translate("MainWindow", u"Estad\u00edsticas", None))
        self.menuArchivo.setTitle(QCoreApplication.translate("MainWindow", u"Archivo", None))
        self.menuAyuda.setTitle(QCoreApplication.translate("MainWindow", u"Ayuda", None))
    # retranslateUi

