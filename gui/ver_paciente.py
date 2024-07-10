from PyQt6 import uic

class VerPacienteWindow():
    def __init__(self):
        self.npr = uic.loadUi("gui/ver_paciente.ui")
        self.npr.show()

