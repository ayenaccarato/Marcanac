from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

class VerPacienteWindow():
    def __init__(self):
        self.npr = uic.loadUi("gui/ver_paciente.ui")
        self.npr.show()

