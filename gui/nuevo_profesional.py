from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

class NuevoProfesionalWindow():
    def __init__(self):
        self.npr = uic.loadUi("gui/nuevo_profesional.ui")
        self.npr.show()