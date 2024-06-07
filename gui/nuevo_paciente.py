from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

class NuevoPacienteWindow():
    def __init__(self):
        self.np = uic.loadUi("gui/nuevo_paciente.ui")
        self.np.show()

    
