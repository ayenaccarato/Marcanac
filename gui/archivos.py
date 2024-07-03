from PyQt6 import uic
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox

class ArchivosWindow():
    def __init__(self):
        self.arc = uic.loadUi("gui/archivos.ui")
        self.arc.show()

    