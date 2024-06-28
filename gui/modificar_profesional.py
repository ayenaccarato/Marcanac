from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

class ModificarProfesionalWindow():
    def __init__(self):
        self.np = uic.loadUi("gui/modificar_profesional.ui")
        self.np.show()