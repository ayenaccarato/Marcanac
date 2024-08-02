import os

from PyQt6 import uic
from PyQt6.QtCore import Qt, QStandardPaths
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem

from data.archivos_paciente import ArchivosPacienteData

class ArchivosPacienteWindow():

    def __init__(self):
        ArchivosPacienteData()
        #self.arc = uic.loadUi("gui/pacientes/archivos_paciente.ui")
        #self.arc.show()
        ui_file = os.path.join(os.path.dirname(__file__), '..', 'pacientes', 'archivos_paciente.ui')
        ui_file = os.path.abspath(ui_file)
        if not os.path.isfile(ui_file):
            print(f"Error: el archivo {ui_file} no se encuentra.")
            return
        self.arc = uic.loadUi(ui_file)

    def cargarArchivos(self, id_paciente):
        # Obtener la lista de archivos relacionados con el paciente desde la base de datos
        lis = ArchivosPacienteData()
        archivos = lis.obtener_archivos_por_paciente(id_paciente)
        
        if archivos:
            self.arc.swArchivos.setCurrentIndex(0)
            # Configura la tabla
            self.arc.tableWidget.setRowCount(len(archivos))
            self.arc.tableWidget.setColumnCount(1)
            self.arc.tableWidget.setHorizontalHeaderLabels(["Archivo"])

            # Añade los archivos a la tabla
            for fila, archivo in enumerate(archivos):
                # Añade los archivos a la tabla
                nombre_archivo = archivo[1]  # Accede al primer elemento de la tupla (nombre_archivo)
                contenido_archivo = archivo[2]  # Accede al segundo elemento de la tupla (contenido)

                # Agregar el nombre del archivo a la celda
                item_nombre = QTableWidgetItem(nombre_archivo)
                self.arc.tableWidget.setItem(fila, 0, item_nombre)
               
                # Guardar el contenido del archivo en el QTableWidgetItem
                item_nombre.setData(Qt.ItemDataRole.UserRole, contenido_archivo)
                self.arc.tableWidget.cellDoubleClicked.connect(lambda: self.manejarDobleClic(fila))
            self.arc.show()
        else:
            self.arc.swArchivos.setCurrentIndex(1)
            self.arc.show()
        
        self.arc.btnAgregar.clicked.connect(lambda: self.abrirArchivo(id_paciente))

    def manejarCeldaClic(self, item):
        '''Maneja el clic en una celda de la tabla de archivos'''
        # Verificar si el ítem tiene datos de usuario (UserRole)
        contenido_archivo = item.data(Qt.ItemDataRole.UserRole)
        if contenido_archivo:
            # Aquí puedes manejar la apertura o visualización del archivo según sea necesario
            print(f"Contenido del archivo seleccionado: {contenido_archivo}")

    def abrirArchivo(self, id_paciente):
        '''Abre el buscador de archivos para poder cargar un archivo'''
        options = QFileDialog.Option
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

    def manejarDobleClic(self, fila):
        item = self.arc.tableWidget.item(fila, 0)
        contenido_archivo = item.data(Qt.ItemDataRole.UserRole)
        if contenido_archivo:
            # Crear un archivo temporal para abrirlo con la aplicación predeterminada
            temp_file_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.TempLocation), item.text())
            with open(temp_file_path, 'wb') as temp_file:
                temp_file.write(contenido_archivo)

            # Abrir el archivo con la aplicación predeterminada del sistema
            if os.name == 'nt':  # Windows
               os.startfile(temp_file_path) 
            # elif os.name == 'posix':  # macOS, Linux
            #     subprocess.call(('xdg-open', temp_file_path))