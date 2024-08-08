import os

from PyQt6 import uic
from PyQt6.QtCore import Qt, QStandardPaths
from PyQt6.QtWidgets import QFileDialog, QListWidgetItem, QMessageBox, QMenu
from PyQt6.QtGui import QIcon, QAction
from data.historia_clinica import HistoriaClinicaData

class HistoriaClinicaWindow():

    def __init__(self):
        HistoriaClinicaData()
        ui_file = os.path.join(os.path.dirname(__file__), '..', 'pacientes', 'historia_clinica.ui')
        ui_file = os.path.abspath(ui_file)
        if not os.path.isfile(ui_file):
            print(f"Error: el archivo {ui_file} no se encuentra.")
            return
        self.hc = uic.loadUi(ui_file)

        self.hc.listWidget.itemDoubleClicked.connect(self.manejarDobleClic)

    def cargarArchivos(self, id_paciente):
        # Obtener la lista de archivos relacionados con el paciente desde la base de datos
        lis = HistoriaClinicaData()
        archivos = lis.obtener_hc_por_paciente(id_paciente)
        
        if archivos:
            self.hc.swArchivos.setCurrentIndex(0)
            # Limpiar el QListWidget antes de agregar nuevos ítems
            self.hc.listWidget.clear()
            
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
                self.hc.listWidget.addItem(item)
                
            self.hc.show()
        else:
            self.hc.swArchivos.setCurrentIndex(1)
            self.hc.show()
        
         # Conectar el menú contextual con el id_paciente
        self.hc.listWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.hc.listWidget.customContextMenuRequested.connect(lambda pos: self.mostrarMenuContextual(pos, id_paciente))

        self.hc.btnAgregar.clicked.connect(lambda: self.abrirArchivo(id_paciente))

    def abrirArchivo(self, id_paciente):
        '''Abre el buscador de archivos para poder cargar un archivo'''
        
        dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        file_types = "All files(*)"
        data_file, _ = QFileDialog.getOpenFileName(self.hc, "Abrir Archivo", dir, file_types)
        if data_file:
            print(f"Archivo seleccionado: {data_file}")
            with open(data_file, 'rb') as file:
                contenido = file.read()
                nombre_archivo = os.path.basename(data_file)
                # Guardar el archivo en la base de datos
                lis = HistoriaClinicaData()
                lis.guardar_archivo(nombre_archivo, contenido, id_paciente)


                # Recargar la tabla de archivos
                self.cargarArchivos(id_paciente)

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

    def mostrarMenuContextual(self, pos, id_paciente):
        '''Muestra el menú contextual para eliminar archivos'''
        item = self.hc.listWidget.itemAt(pos)
        if item:
            menu = QMenu(self.hc.listWidget)
            
            eliminar_action = QAction('Eliminar', self.hc.listWidget)
            eliminar_action.triggered.connect(lambda: self.eliminarArchivo(item, id_paciente))
            menu.addAction(eliminar_action)
            
            menu.exec(self.hc.listWidget.viewport().mapToGlobal(pos))

    def eliminarArchivo(self, item, id_paciente):
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
                lis = HistoriaClinicaData()
                if lis.eliminar_hc(nombre_archivo, id_paciente):
                    self.hc.listWidget.takeItem(self.hc.listWidget.row(item))  # Eliminar el ítem del QListWidget
                else:
                    QMessageBox.critical(self.hc, "Error", "No se pudo eliminar el archivo.")
        else:
            print("Eliminación cancelada")
