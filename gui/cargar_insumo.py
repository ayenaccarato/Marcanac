from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

class NuevoInsumoWindow():
    def __init__(self):
        self.ni = uic.loadUi("gui/cargar_insumo.ui")
        self.ni.show()