from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

from data.insumos import InsumoData
from model.insumo import Insumo

class NuevoInsumoWindow():

    def __init__(self):
        self.nInsumo = uic.loadUi("gui/insumos/cargar_insumo.ui")

    