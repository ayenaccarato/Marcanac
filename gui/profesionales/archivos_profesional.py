import os

from PyQt6 import uic
from PyQt6.QtCore import Qt, QStandardPaths
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem

from data.archivos_profesional import ArchivosProfesionalData

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

    def cargarArchivosProfesional(self, id_profesional):
        # Obtener la lista de archivos relacionados con el paciente desde la base de datos
        lis = ArchivosProfesionalData()
        archivos = lis.obtener_archivos_por_profesional(id_profesional)
        
        if archivos:
            self.arcP.swArchivos.setCurrentIndex(0)
            # Configura la tabla
            self.arcP.tblArchivos.setRowCount(len(archivos))
            self.arcP.tblArchivos.setColumnCount(1)
            self.arcP.tblArchivos.setHorizontalHeaderLabels(["Archivo"])

            # Añade los archivos a la tabla
            for fila, archivo in enumerate(archivos):
                # Añade los archivos a la tabla
                nombre_archivo = archivo[1]  # Accede al primer elemento de la tupla (nombre_archivo)
                contenido_archivo = archivo[2]  # Accede al segundo elemento de la tupla (contenido)

                # Agregar el nombre del archivo a la celda
                item_nombre = QTableWidgetItem(nombre_archivo)
                self.arcP.tblArchivos.setItem(fila, 0, item_nombre)
               
                # Guardar el contenido del archivo en el QTableWidgetItem
                item_nombre.setData(Qt.ItemDataRole.UserRole, contenido_archivo)
                self.arcP.tblArchivos.cellDoubleClicked.connect(lambda: self.manejarDobleClicP(fila))
            self.arcP.show()
        else:
            self.arcP.swArchivos.setCurrentIndex(1)
            self.arcP.show()
        
        self.arcP.btnAgregar.clicked.connect(lambda: self.abrirArchivoProfesional(id_profesional))

    def abrirArchivoProfesional(self, id_profesional):
        '''Abre el buscador de archivos para poder cargar un archivo'''
        options = QFileDialog.Option
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

    def manejarDobleClicP(self, fila):
        item = self.arcP.tblArchivos.item(fila, 0)
        contenido_archivo = item.data(Qt.ItemDataRole.UserRole)
        if contenido_archivo:
            # Crear un archivo temporal para abrirlo con la aplicación predeterminada
            temp_file_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.TempLocation), item.text())
            with open(temp_file_path, 'wb') as temp_file:
                temp_file.write(contenido_archivo)

            # Abrir el archivo con la aplicación predeterminada del sistema
            if os.name == 'nt':  # Windows
               os.startfile(temp_file_path) 
            elif os.name == 'posix':  # macOS, Linux
                subprocess.call(('xdg-open', temp_file_path))