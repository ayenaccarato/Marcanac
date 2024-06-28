from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

class ModificarPacienteWindow():
    def __init__(self):
        self.np = uic.loadUi("gui/modificar_paciente.ui")
        self.np.show()