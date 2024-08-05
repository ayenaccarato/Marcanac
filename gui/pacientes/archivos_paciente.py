import os

from PyQt6 import uic
from PyQt6.QtCore import Qt, QStandardPaths, QSize
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem, QListWidget, QListWidgetItem, QMessageBox
from PyQt6.QtGui import QIcon
from data.archivos_paciente import ArchivosPacienteData

class ArchivosPacienteWindow():

    def __init__(self):
        ArchivosPacienteData()
        #self.arc = uic.loadUi("gui/pacientes/archivos_paciente.ui")
        #self.arc.show()
        ui_file = os.path.join(os.path.dirname(__file__), '..', 'pacientes', 'archivos_paciente_2.ui')
        ui_file = os.path.abspath(ui_file)
        if not os.path.isfile(ui_file):
            print(f"Error: el archivo {ui_file} no se encuentra.")
            return
        self.arc = uic.loadUi(ui_file)

        self.arc.listWidget.itemDoubleClicked.connect(self.manejarDobleClic)

    def cargarArchivos(self, id_paciente):
        # Obtener la lista de archivos relacionados con el paciente desde la base de datos
        lis = ArchivosPacienteData()
        archivos = lis.obtener_archivos_por_paciente(id_paciente)
        
        if archivos:
            # Limpiar el QListWidget antes de agregar nuevos ítems
            self.arc.listWidget.clear()
            
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
                self.arc.listWidget.addItem(item)
                
            self.arc.show()
        else:
            self.arc.swArchivos.setCurrentIndex(1)
            self.arc.show()
            
        self.arc.btnAgregar.clicked.connect(lambda: self.abrirArchivo(id_paciente))

    def abrirArchivo(self, id_paciente):
        '''Abre el buscador de archivos para poder cargar un archivo'''
        
        dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        file_types = "All files(*)"
        data_file, _ = QFileDialog.getOpenFileName(self.arc, "Abrir Archivo", dir, file_types)
        if data_file:
            print(f"Archivo seleccionado: {data_file}")
            with open(data_file, 'rb') as file:
                contenido = file.read()
                nombre_archivo = os.path.basename(data_file)
                # Guardar el archivo en la base de datos
                lis = ArchivosPacienteData()
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

    # def mostrarMenuContextual(self, pos):
    #     '''Muestra el menú contextual para eliminar archivos'''
    #     item = self.arc.listWidget.itemAt(pos)
    #     if item:
    #         menu = QMenu(self.arc.listWidget)
            
    #         eliminar_action = QAction('Eliminar', self.arc.listWidget)
    #         eliminar_action.triggered.connect(lambda: self.eliminarArchivo(item))
    #         menu.addAction(eliminar_action)
            
    #         menu.exec(self.arc.listWidget.viewport().mapToGlobal(pos))

    # def eliminarArchivo(self, item):
    #     '''Elimina el archivo seleccionado del QListWidget y de la base de datos'''
    #     nombre_archivo = item.text()
    #     if QMessageBox.question(self.arc, "Confirmar eliminación", f"¿Estás seguro de que quieres eliminar '{nombre_archivo}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
    #         contenido_archivo = item.data(Qt.ItemDataRole.UserRole)
    #         if contenido_archivo:
    #             # Obtener el id del paciente si es necesario
    #             id_paciente = ...  # Debes manejar cómo obtener el id_paciente

    #             # Eliminar el archivo de la base de datos
    #             lis = ArchivosPacienteData()
    #             if lis.eliminar_archivo(nombre_archivo, id_paciente):
    #                 self.arc.listWidget.takeItem(self.arc.listWidget.row(item))  # Eliminar el ítem del QListWidget
    #             else:
    #                 QMessageBox.critical(self.arc, "Error", "No se pudo eliminar el archivo de la base de datos.")