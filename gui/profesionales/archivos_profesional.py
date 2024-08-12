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

        ui_file_meses= os.path.join(os.path.dirname(__file__), '..', 'profesionales' ,'archivos_de_meses.ui')
        ui_file_meses = os.path.abspath(ui_file_meses)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file_meses):
            print(f"Error: el archivo {ui_file_meses} no se encuentra.")
            return
        self.meses = uic.loadUi(ui_file_meses)

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

    def mostrar_listWidget_años(self):
        # Limpiar el listWidget antes de agregar nuevos elementos
        self.lisPago.listWidget.clear()

        # Configurar el listWidget en modo de íconos y organizar en cuadrícula
        self.lisPago.listWidget.setViewMode(QListView.ViewMode.IconMode)
        self.lisPago.listWidget.setIconSize(QSize(64, 64))  # Ajustar el tamaño del ícono según sea necesario
        self.lisPago.listWidget.setResizeMode(QListView.ResizeMode.Adjust)  # Ajuste automático de tamaño
        self.lisPago.listWidget.setSpacing(10)  # Espacio entre ítems

        anos = []
        ano_actual = datetime.now().year
        
        # Agregar el año actual si no está ya en la lista
        if ano_actual not in anos:
            anos.append(ano_actual)
        
        # Ruta al ícono de la carpeta
        ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'carpeta.png')
        ui_file = os.path.abspath(ui_file)
        icono_carpeta = QIcon(ui_file)

        # Agregar los años al listWidget
        for ano in anos:
            item = QListWidgetItem(icono_carpeta, str(ano))  # Convertir el año a cadena
            item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)  # Centrar el texto debajo del ícono
            print('año seleccionado ', ano)
            item.setData(Qt.ItemDataRole.UserRole, ano)  # Guardar el año en el item
            self.lisPago.listWidget.addItem(item)

        # Conectar el evento de clic a un método que manejará la selección
        self.lisPago.listWidget.itemDoubleClicked.connect(self.mostrar_listWidget_meses)

        # Mostrar el listWidget
        self.lisPago.show()

    def mostrar_listWidget_meses(self, item):
        if item is None:
            return  # Salir si no se pasa un item válido

        # Obtener el año seleccionado del item (se debe almacenar en self.año_seleccionado)
        self.año_seleccionado = self.lisPago.listWidget.currentItem().data(Qt.ItemDataRole.UserRole)
        print('Año mostrado:', self.año_seleccionado)
        
        # Limpiar el listWidget antes de agregar nuevos elementos
        self.meses.listWidget.clear()

        # Configurar el listWidget en modo de íconos y organizar en cuadrícula
        self.meses.listWidget.setViewMode(QListView.ViewMode.IconMode)
        self.meses.listWidget.setIconSize(QSize(64, 64))
        self.meses.listWidget.setResizeMode(QListView.ResizeMode.Adjust)
        self.meses.listWidget.setSpacing(10)

        # Crear las carpetas de los meses
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        # Ruta al ícono de la carpeta
        ui_file = os.path.join(os.path.dirname(__file__), '..', 'imagenes', 'carpeta.png')
        ui_file = os.path.abspath(ui_file)
        icono_carpeta = QIcon(ui_file)

        for mes in meses:
            item = QListWidgetItem(icono_carpeta, mes)
            item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)  # Centrar el texto debajo del ícono
            item.setData(Qt.ItemDataRole.UserRole, mes)  # Guardar el mes en el item
            self.meses.listWidget.addItem(item)

        # Conectar el evento de clic a un método que manejará la selección
        self.meses.listWidget.itemDoubleClicked.connect(self.mostrar_archivos_del_mes)

        # Mostrar el listWidget
        self.meses.show()

    def mostrar_archivos_del_mes(self, item):
        mes_seleccionado = item.text()
        print('Año:', self.año_seleccionado, 'Mes:', mes_seleccionado)

        # Usar el año seleccionado para construir la ruta del mes
        ruta_carpeta_mes = os.path.join(os.path.dirname(__file__), '..', 'pagos', str(self.año_seleccionado), mes_seleccionado)

        # Verificar si la carpeta existe
        if os.path.exists(ruta_carpeta_mes):
            # Obtener los archivos de la carpeta
            archivos = os.listdir(ruta_carpeta_mes)

            # Limpiar el listWidget antes de agregar nuevos elementos
            self.mes.listWidget.clear()

            # Configurar el listWidget en modo de lista para ajuste del texto
            self.mes.listWidget.setViewMode(QListView.ViewMode.ListMode)  # Cambiar a modo de lista
            self.mes.listWidget.setIconSize(QSize(64, 64))  # Tamaño del ícono
            self.mes.listWidget.setResizeMode(QListView.ResizeMode.Adjust)  # Ajuste automático de tamaño
            self.mes.listWidget.setSpacing(10)  # Espacio entre ítems

            for archivo in archivos:
                archivo_path = os.path.join(ruta_carpeta_mes, archivo)
                item = QListWidgetItem()
                
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
                item.setText(archivo)  # Establecer el texto del archivo
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

                 # Crear el widget personalizado para el ítem
                widget_item = CustomListWidgetItem(icon_path, archivo)
                list_widget_item = QListWidgetItem()
                list_widget_item.setSizeHint(widget_item.sizeHint())  # Establecer el tamaño del ítem

                self.mes.listWidget.addItem(list_widget_item)
                self.mes.listWidget.setItemWidget(list_widget_item, widget_item)
                
                # # Añadir el ítem al QListWidget
                # self.mes.listWidget.addItem(item)
                
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
            # Obtener el mes actual de la vista o del contexto adecuado
            mes = self.obtener_nombre_mes() 
            
            # Construir la ruta completa al archivo
            ruta_carpeta_mes = os.path.join(os.path.dirname(__file__), '..', 'pagos', str(self.año_seleccionado), mes)
            ruta_archivo = os.path.join(ruta_carpeta_mes, nombre_archivo)
            
            print('Ruta del archivo:', ruta_archivo)  # Imprimir la ruta para depuración

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