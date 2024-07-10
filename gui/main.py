import json
import os

from PyQt6.QtGui import QColor
from PyQt6 import uic, QtCore
from PyQt6.QtCore import Qt, QDate, QStandardPaths
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QFileDialog

from data.archivos_paciente import ArchivosPacienteData
from data.archivos_profesional import ArchivosProfesionalData
from data.insumos import InsumoData
from data.listados import ListadoData
from data.paciente import PacienteData
from data.paciente_coordinador import PacienteCoordinadorData
from data.paciente_profesionales import PacienteProfesionalesData
from data.profesional import ProfesionalData
from gui.insumos import InsumosWindow
from gui.paciente import PacienteWindow
from gui.profesional import ProfesionalWindow
from model.insumo import Insumo
from model.paciente import Paciente
from model.profesional import Profesional

class MainWindow():

    def __init__(self):
        self.main = uic.loadUi("gui/main.ui")
        self.initGUI()
        self.main.show()
        #self.main.showMaximized()

        self.main.btnRestaurar.hide() #Oculto boton         

        self.main.btnMinimizar.clicked.connect(self.control_btnMinimizar) #Minimizo la pantalla
        self.main.btnRestaurar.clicked.connect(self.control_btnNormal) #Vuelve a la normalidad
        self.main.btnMaximizar.clicked.connect(self.control_btnMaximizar) #Maximizo la pagina
        self.main.btnCerrar.clicked.connect(lambda:self.main.close()) #Cierro

    def initGUI(self):       

        # Eliminar la barra de título
        self.main.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # Configurar la opacidad de la ventana
        self.main.setWindowOpacity(1.0)

        #Interfaz de distintas ventanas
        #Paciente
        paciente = PacienteWindow()
        paciente.initGUI()
        
        #Profesional
        profesional = ProfesionalWindow()
        profesional.initGUI()

        #Insumos
        insumos = InsumosWindow()
        insumos.initGUI()         
        
        #Botones del menú de main
        self.main.btnListado.clicked.connect(lambda: self.main.stackedWidget.setCurrentWidget(self.main.page_datos)) #Abro pagina de listados
        self.main.btnRegistrar.clicked.connect(lambda: self.main.stackedWidget.setCurrentWidget(self.main.page_registrar)) #Abro pagina de registros
        #Listados
        self.main.listPacientes.clicked.connect(lambda: paciente.abrirListado())
        self.main.listProfesionales.clicked.connect(lambda: profesional.abrirListadoProfesionales())
        #Registros
        self.main.btnPaciente.clicked.connect(lambda: paciente.abrirRegistro())
        self.main.btnProfesional.clicked.connect(lambda: profesional.abrirRegistroProf())

#Métodos de controles de botones del main  
    def control_btnMinimizar(self):
        self.main.showMinimized()

    def control_btnMaximizar(self):
        self.main.showMaximized()
        self.main.btnMaximizar.hide()
        self.main.btnRestaurar.show()

    def control_btnNormal(self):
        self.main.showNormal()
        self.main.btnRestaurar.hide()
        self.main.btnMaximizar.show()

############# Pacientes ###############

############## Listado ################
    
############## Profesionales ##########
       
############## Listado ################

############## Insumos ################        

############## Coordinador - Paciente ################  

############### Archivos - Paciente ################

############### Archivos - Profesional ################               
