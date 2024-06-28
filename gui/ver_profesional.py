from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

class VerProfesionalWindow():
    def __init__(self):
        self.npr = uic.loadUi("gui/ver_profesional.ui")
        self.npr.show()