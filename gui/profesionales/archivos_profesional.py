import os

from PyQt6 import uic
from PyQt6.QtCore import Qt, QStandardPaths
from PyQt6.QtWidgets import QFileDialog, QListWidgetItem, QMessageBox, QMenu
from PyQt6.QtGui import QIcon, QAction

from data.archivos_profesional import ArchivosProfesionalData

class ArchivosProfesionalWindow():

    def __init__(self):
        ArchivosProfesionalData()
        #self.arcP = uic.loadUi("gui/profesionales/archivos_profesional.ui")
        ui_file = os.path.join(os.path.dirname(__file__), '..', 'profesionales', 'archivos_profesional_2.ui')
        ui_file = os.path.abspath(ui_file)
        if not os.path.isfile(ui_file):
            print(f"Error: el archivo {ui_file} no se encuentra.")
            return
        self.arcP = uic.loadUi(ui_file)

        self.arcP.listWidget.itemDoubleClicked.connect(self.manejarDobleClic)

    def cargarArchivosProfesional(self, id_profesional):
        # Obtener la lista de archivos relacionados con el paciente desde la base de datos
        lis = ArchivosProfesionalData()
        archivos = lis.obtener_archivos_por_profesional(id_profesional)
        
        if archivos:
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
                    item.setIcon(QIcon('gui/imagenes/pdf.png'))
                elif ext in ['.doc', '.docx']:
                    item.setIcon(QIcon('gui/imagenes/word.png'))
                elif ext in ['.jpg', '.jpeg', '.png']:
                    item.setIcon(QIcon('gui/imagenes/imagen.png'))
                elif ext in ['.txt']:
                    item.setIcon(QIcon('gui/imagenes/txt.png'))
                else:
                    item.setIcon(QIcon('gui/imagenes/por_defecto.png'))  # Ícono por defecto para otros tipos
                
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