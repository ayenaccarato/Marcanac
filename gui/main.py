from datetime import datetime
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from data.paciente import PacienteData
from gui.nuevo_paciente import NuevoPacienteWindow
from model.paciente import Paciente

class MainWindow():
    def __init__(self):
        self.main = uic.loadUi("gui/main.ui")
        self.initGUI()
        self.main.showMaximized()

    def initGUI(self):
        self.main.btn_adir_Paciente.triggered.connect(self.abrirRegistro)
        self.nuevo = uic.loadUi("gui/nuevo_paciente.ui")

    def abrirRegistro(self):   
        self.nuevo.btnRegistrar.clicked.connect(self.registrarPaciente)     
        self.nuevo.show()

                    #### Pacientes ####

    def registrarPaciente(self):
        mBox = QMessageBox()
        if self.nuevo.cbTipo.currentText() == "--Seleccione una opción--":            
            mBox.setText("Debe seleccionar el tipo de documento")
            mBox.exec()
            self.nuevo.cbTipo.setFocus()
        elif len(self.nuevo.txtDocumento.text()) < 6:           
            mBox.setText("Debe completar el campo apellido")
            mBox.exec()
            self.nuevo.txtApellido.setFocus() #Va al campo que debe completar
        else:
            fechaN = self.nuevo.txtFecha.date().toPyDate().strftime("%d/%m/%Y")
            nuevoPaciente = Paciente(
                nombre = self.nuevo.txtNombre.text(),
                apellido = self.nuevo.txtApellido.text(),
                tipo = self.nuevo.cbTipo.currentText(),
                documento = self.nuevo.txtDocumento.text(),
                fechaNacimiento = fechaN,
                sexo = self.nuevo.cbSexo.currentText()
            )

            objData = PacienteData()
            
            mBox = QMessageBox()
            if objData.registrar(paciente=nuevoPaciente):                
                mBox.setText("Paciente registrado")      
                self.limpiarCamposPaciente()          
            else:
                mBox.setText("El paciente no pudo ser registrado")
                
            mBox.exec()

    def limpiarCamposPaciente(self):
        self.nuevo.txtNombre.setText("")
        self.nuevo.txtApellido.setText("")
        self.nuevo.cbTipo.setCurrentIndex(0)
        self.nuevo.txtDocumento.setText("")
        #self.nuevo.txtFecha.setDate("")
        self.nuevo.cbSexo.setCurrentIndex(0)