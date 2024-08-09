from datetime import datetime
import os

from PyQt6 import uic
from PyQt6.QtCore import Qt, QStandardPaths, QSize
from PyQt6.QtWidgets import QFileDialog, QListWidgetItem, QMessageBox, QMenu, QListView
from PyQt6.QtGui import QIcon, QAction

from data.archivos_profesional import ArchivosProfesionalData
from data.mes_pago import MesPagoData


class ArchivosProfesionalWindow():

    def __init__(self):
        ArchivosProfesionalData()
        #self.arcP = uic.loadUi("gui/profesionales/archivos_profesional.ui")
        ui_file = os.path.join(os.path.dirname(__file__), '..', 'profesionales', 'archivos_profesional.ui')
        ui_file = os.path.abspath(ui_file)
        if not os.path.isfile(ui_file):
            print(f"Error: el archivo {ui_file} no se encuentra.")
            return
        self.arcP = uic.loadUi(ui_file)

        self.arcP.listWidget.itemDoubleClicked.connect(self.manejarDobleClic)

        ui_file_pago= os.path.join(os.path.dirname(__file__), '..', 'profesionales' ,'archivos_de_pagos.ui')
        ui_file_pago = os.path.abspath(ui_file_pago)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file_pago):
            print(f"Error: el archivo {ui_file_pago} no se encuentra.")
            return
        self.lisPago = uic.loadUi(ui_file_pago)

        ui_file_mes= os.path.join(os.path.dirname(__file__), '..', 'profesionales' ,'archivos_de_mes.ui')
        ui_file_mes = os.path.abspath(ui_file_mes)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file_mes):
            print(f"Error: el archivo {ui_file_mes} no se encuentra.")
            return
        self.mes = uic.loadUi(ui_file_mes)

        self.mes.listWidget.itemDoubleClicked.connect(self.manejarDobleClicMes)

    def cargarArchivosProfesional(self, id_profesional):
        # Obtener la lista de archivos relacionados con el paciente desde la base de datos
        lis = ArchivosProfesionalData()
        archivos = lis.obtener_archivos_por_profesional(id_profesional)
        
        if archivos:
            self.arcP.swArchivos.setCurrentIndex(0)
            # Limpiar el QListWidget antes de agregar nuevos ítems
            self.arcP.listWidget.clear()
            
            for archivo in archivos:
                nombre_archivo = archivo[1]  # Nombre del archivo
                contenido_archivo = archivo[2]  # Contenido del archivo
                
                # Crear el QListWidgetItem
                item = QListWidgetItem(nombre_archivo)
                
                # Asignar el contenido del archivo al ítem
                item.setData(Qt.ItemDataRole.UserRole, contenido_archivo)
                
                # Asignar el ícono según la extensión del archivo
                ext = os.path.splitext(nombre_archivo)[1].lower()
                if ext in ['.pdf']:
                    ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'pdf.png')
                    ui_file = os.path.abspath(ui_file)
                    item.setIcon(QIcon(ui_file))
                elif ext in ['.doc', '.docx']:
                    ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'word.png')
                    ui_file = os.path.abspath(ui_file)
                    item.setIcon(QIcon(ui_file))
                elif ext in ['.jpg', '.jpeg', '.png']:
                    ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'imagen.png')
                    ui_file = os.path.abspath(ui_file)
                    item.setIcon(QIcon(ui_file))
                elif ext in ['.txt']:
                    ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'txt.png')
                    ui_file = os.path.abspath(ui_file)
                    item.setIcon(QIcon(ui_file))
                else:
                    ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'por_defecto.png')
                    ui_file = os.path.abspath(ui_file)
                    item.setIcon(QIcon(ui_file))  # Ícono por defecto para otros tipos
                
                # Añadir el ítem al QListWidget
                self.arcP.listWidget.addItem(item)
                
            self.arcP.show()
        else:
            self.arcP.swArchivos.setCurrentIndex(1)
            self.arcP.show()

         # Conectar el menú contextual con el id_profesional
        self.arcP.listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.arcP.listWidget.customContextMenuRequested.connect(lambda pos: self.mostrarMenuContextual(pos, id_profesional))
            
        self.arcP.btnAgregar.clicked.connect(lambda: self.abrirArchivo(id_profesional))

    def abrirArchivo(self, id_profesional):
        '''Abre el buscador de archivos para poder cargar un archivo'''
        
        dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        file_types = "All files(*)"
        data_file, _ = QFileDialog.getOpenFileName(self.arcP, "Abrir Archivo", dir, file_types)
        if data_file:
            print(f"Archivo seleccionado: {data_file}")
            with open(data_file, 'rb') as file:
                contenido = file.read()
                nombre_archivo = os.path.basename(data_file)
                # Guardar el archivo en la base de datos
                lis = ArchivosProfesionalData()
                lis.guardar_archivo(nombre_archivo, contenido, id_profesional)


                # Recargar la tabla de archivos
                self.cargarArchivosProfesional(id_profesional)

    def manejarDobleClic(self, item):
        '''Maneja el doble clic en un ítem del QListWidget'''
        if item:
            contenido_archivo = item.data(Qt.ItemDataRole.UserRole)
            if contenido_archivo:
                temp_file_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.TempLocation), item.text())
                
                try:
                    with open(temp_file_path, 'wb') as temp_file:
                        temp_file.write(contenido_archivo)
                    
                    if os.name == 'nt':  # Windows
                        os.startfile(temp_file_path)
                    elif os.name == 'posix':  # macOS, Linux
                        subprocess.call(['xdg-open', temp_file_path])
                    else:
                        QMessageBox.warning(None, "Error", "Sistema operativo no soportado para abrir archivos.")
                except Exception as e:
                    QMessageBox.critical(None, "Error", f"Error al abrir el archivo: {e}")
            else:
                QMessageBox.warning(None, "Error", "No se pudo encontrar el contenido del archivo.")

    def mostrarMenuContextual(self, pos, id_profesional):
        '''Muestra el menú contextual para eliminar archivos'''
        item = self.arcP.listWidget.itemAt(pos)
        if item:
            menu = QMenu(self.arcP.listWidget)
            
            eliminar_action = QAction('Eliminar', self.arcP.listWidget)
            eliminar_action.triggered.connect(lambda: self.eliminarArchivo(item, id_profesional))
            menu.addAction(eliminar_action)
            
            menu.exec(self.arcP.listWidget.viewport().mapToGlobal(pos))

    def eliminarArchivo(self, item, id_profesional):
        '''Elimina el archivo seleccionado del QListWidget'''
        nombre_archivo = item.text()
        mBox = QMessageBox()
        mBox.setWindowTitle('Confirmar eliminación')
        mBox.setText(f"¿Estás seguro de que quieres eliminar '{nombre_archivo}'?")

        # Añadir botones personalizados
        si_btn = mBox.addButton("Sí", QMessageBox.ButtonRole.YesRole)
        no_btn = mBox.addButton("No", QMessageBox.ButtonRole.NoRole)
        
        mBox.setDefaultButton(no_btn)
        mBox.exec()

        if mBox.clickedButton() == si_btn:
            contenido_archivo = item.data(Qt.ItemDataRole.UserRole)
            if contenido_archivo:
                # Eliminar el archivo de la base de datos
                lis = ArchivosProfesionalData()
                if lis.eliminar_archivo(nombre_archivo, id_profesional):
                    self.arcP.listWidget.takeItem(self.arcP.listWidget.row(item))  # Eliminar el ítem del QListWidget
                else:
                    QMessageBox.critical(self.arc, "Error", "No se pudo eliminar el archivo.")
        else:
            print("Eliminación cancelada")

############# Archivos de pagos ###############

    def mostrar_listWidget_meses(self):
        # Limpiar el listWidget antes de agregar nuevos elementos
        self.lisPago.listWidget.clear()

        # Configurar el listWidget en modo de íconos y organizar en cuadrícula
        self.lisPago.listWidget.setViewMode(QListView.ViewMode.IconMode)
        self.lisPago.listWidget.setIconSize(QSize(64, 64))  # Ajustar el tamaño del ícono según sea necesario
        self.lisPago.listWidget.setResizeMode(QListView.ResizeMode.Adjust)  # Ajuste automático de tamaño
        self.lisPago.listWidget.setSpacing(10)  # Espacio entre ítems

        # Crear las carpetas de los meses
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        # Ruta al ícono de la carpeta
        ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'carpeta.png')
        ui_file = os.path.abspath(ui_file)
        icono_carpeta = QIcon(ui_file)

        for mes in meses:
            item = QListWidgetItem(icono_carpeta, mes)
            item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)  # Centrar el texto debajo del ícono
            self.lisPago.listWidget.addItem(item)

        # Conectar el evento de clic a un método que manejará la selección
        self.lisPago.listWidget.itemDoubleClicked.connect(self.mostrar_archivos_del_mes)

        # Mostrar el listWidget
        self.lisPago.show()

    # def mostrar_archivos_del_mes(self, item):
    #     mes_seleccionado = item.text()
    #     # Aquí deberías obtener los archivos correspondientes al mes seleccionado
    #     archivos = self.obtener_archivos_del_mes(mes_seleccionado)

    #     # Aquí puedes mostrar los archivos, por ejemplo, en otro listWidget o en una vista de lista
    #     print(f"Archivos en la carpeta {mes_seleccionado}: {archivos}")

    # def mostrar_archivos_del_mes(self, item):
    #     mes_seleccionado = item.text()
    #     self.ruta_carpeta_mes = os.path.join(os.path.dirname(__file__),'..', 'pagos', mes_seleccionado)  # Ajusta la ruta base según sea necesario
        
    #     # Aquí deberías obtener los archivos correspondientes al mes seleccionado
    #     archivos = self.obtener_archivos_del_mes(mes_seleccionado)
        
    #     # Aquí puedes mostrar los archivos, por ejemplo, en otro listWidget o en una vista de lista
    #     if archivos:
    #         self.mes.listWidget.clear()
    #         for archivo in archivos:
    #             nombre_archivo = archivo[0]  # Ajusta según la estructura de los datos
    #             item = QListWidgetItem(nombre_archivo)
    #             self.mes.listWidget.addItem(item)
    #     else:
    #         self.mes.listWidget.clear()
    #         self.mes.listWidget.addItem('No hay archivos cargados')
        
    #     # Mostrar el listWidget
    #     self.mes.show()

    def mostrar_archivos_del_mes(self, item):
        mes_seleccionado = item.text()
        
        # Obtener la ruta de la carpeta del mes
        ruta_carpeta_mes = os.path.join(os.path.dirname(__file__),'..', 'pagos', mes_seleccionado)
        
        # Verificar si la carpeta existe
        if os.path.exists(ruta_carpeta_mes):
            # Obtener los archivos de la carpeta
            archivos = os.listdir(ruta_carpeta_mes)
            
            # Limpiar el listWidget antes de agregar nuevos elementos
            self.mes.listWidget.clear()
            
            # Configurar el listWidget en modo de íconos y organizar en cuadrícula
            self.mes.listWidget.setViewMode(QListView.ViewMode.IconMode)
            self.mes.listWidget.setIconSize(QSize(64, 64))
            self.mes.listWidget.setResizeMode(QListView.ResizeMode.Adjust)
            self.mes.listWidget.setSpacing(10)
            
            for archivo in archivos:
                archivo_path = os.path.join(ruta_carpeta_mes, archivo)
                item = QListWidgetItem(archivo)
                
                # Asignar el ícono según la extensión del archivo
                ext = os.path.splitext(archivo)[1].lower()
                if ext in ['.pdf']:
                    ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'pdf.png')
                elif ext in ['.doc', '.docx']:
                    ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'word.png')
                elif ext in ['.jpg', '.jpeg', '.png']:
                    ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'imagen.png')
                elif ext in ['.txt']:
                    ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'txt.png')
                else:
                    ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'por_defecto.png')
                
                item.setIcon(QIcon(ui_file))
                item.setData(Qt.ItemDataRole.UserRole, archivo_path)
                
                # Añadir el ítem al QListWidget
                self.mes.listWidget.addItem(item)
            
            # Mostrar el listWidget
            self.mes.show()
        else:
            self.mes.listWidget.clear()
            self.mes.listWidget.addItem('No hay archivos cargados')
            self.mes.show()

    def obtener_archivos_del_mes(self, mes):
        lis = MesPagoData()
        data = lis.obtener_archivos_por_mes(mes)

        if data:
            self.mes.listWidget.clear()
            
            for archivo in data:
                nombre_archivo = archivo[1]  # Nombre del archivo
                contenido_archivo = archivo[2]  # Contenido del archivo
                
                # Crear el QListWidgetItem
                item = QListWidgetItem(nombre_archivo)
                
                # Asignar el contenido del archivo al ítem
                item.setData(Qt.ItemDataRole.UserRole, contenido_archivo)
                
                # Asignar el ícono según la extensión del archivo
                ext = os.path.splitext(nombre_archivo)[1].lower()
                if ext in ['.pdf']:
                    ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'pdf.png')
                    ui_file = os.path.abspath(ui_file)
                    item.setIcon(QIcon(ui_file))
                elif ext in ['.doc', '.docx']:
                    ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'word.png')
                    ui_file = os.path.abspath(ui_file)
                    item.setIcon(QIcon(ui_file))
                elif ext in ['.jpg', '.jpeg', '.png']:
                    ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'imagen.png')
                    ui_file = os.path.abspath(ui_file)
                    item.setIcon(QIcon(ui_file))
                elif ext in ['.txt']:
                    ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'txt.png')
                    ui_file = os.path.abspath(ui_file)
                    item.setIcon(QIcon(ui_file))
                else:
                    ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'por_defecto.png')
                    ui_file = os.path.abspath(ui_file)
                    item.setIcon(QIcon(ui_file))  # Ícono por defecto para otros tipos
                
                # Añadir el ítem al QListWidget
                self.mes.listWidget.addItem(item)
                
            self.mes.show()
        else:
            self.mes.listWidget.addItem('No hay archivos cargados')
            self.mes.show()

         # Conectar el menú contextual con el id_profesional
        # self.arcP.listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.arcP.listWidget.customContextMenuRequested.connect(lambda pos: self.mostrarMenuContextual(pos, id_profesional))
            
        # self.arcP.btnAgregar.clicked.connect(lambda: self.abrirArchivo(id_profesional))

    def obtener_nombre_mes(self):
        # Obtener el número del mes actual (01 a 12)
        mes_numero = int(datetime.now().strftime("%m"))  # Convertir el mes a entero para usar en calendar.month_name

        # Diccionario para traducir nombres de meses a castellano
        meses_castellano = {
            1: 'Enero',
            2: 'Febrero',
            3: 'Marzo',
            4: 'Abril',
            5: 'Mayo',
            6: 'Junio',
            7: 'Julio',
            8: 'Agosto',
            9: 'Septiembre',
            10: 'Octubre',
            11: 'Noviembre',
            12: 'Diciembre'
        }
        
        # Obtener el nombre del mes en castellano
        mes_nombre = meses_castellano.get(mes_numero)
        
        # Verificar si el nombre del mes es None, lo que indica un mes no válido
        if mes_nombre is None:
            raise ValueError("Número de mes inválido")
        
        return mes_nombre

    def manejarDobleClicMes(self, item):
        '''Maneja el doble clic en un ítem del QListWidget'''
        if item:
            nombre_archivo = item.text()
            mes = self.obtener_nombre_mes()  # Obtén el mes actual de la vista o del contexto adecuado
            ruta_carpeta_mes = os.path.join(os.path.dirname(__file__),'..', 'pagos', mes)
            ruta_archivo = os.path.join(ruta_carpeta_mes, nombre_archivo)

            if os.path.exists(ruta_archivo):
                try:
                    if os.name == 'nt':  # Windows
                        os.startfile(ruta_archivo)
                    elif os.name == 'posix':  # macOS, Linux
                        subprocess.call(['xdg-open', ruta_archivo])
                    else:
                        QMessageBox.warning(None, "Error", "Sistema operativo no soportado para abrir archivos.")
                except Exception as e:
                    QMessageBox.critical(None, "Error", f"Error al abrir el archivo: {e}")
            else:
                QMessageBox.warning(None, "Error", "El archivo no existe en la ruta especificada.")