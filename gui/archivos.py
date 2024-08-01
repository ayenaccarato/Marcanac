import os
from PyQt6 import uic
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox

class ArchivosWindow():

    def __init__(self):
        #self.arc = uic.loadUi("gui/archivos.ui")
        ui_file = os.path.join(os.path.dirname(__file__), '..', 'gui', 'archivos.ui')
        ui_file = os.path.abspath(ui_file)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file):
            print(f"Error: el archivo {ui_file} no se encuentra.")
            return
        self.arc = uic.loadUi(ui_file)

    