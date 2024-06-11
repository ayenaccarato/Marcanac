from datetime import datetime
import json
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from data.listado_pacientes import ListadoData
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
        self.main.btnListado_Pacientes.triggered.connect(self.abrirListado) #Le agrego la funcionalidad al boton del main
        self.nuevo = uic.loadUi("gui/nuevo_paciente.ui") #Abre la interfaz de agregar paciente
        self.listado = uic.loadUi("gui/listado_pacientes.ui") #Abre la interafz del listado

    def abrirRegistro(self):   
        self.nuevo.btnRegistrar.clicked.connect(self.registrarPaciente)     
        self.nuevo.show()

                    #### Pacientes ####

    def agruparSubm(self):
        fono = self.nuevo.fono.isChecked()
        to = self.nuevo.to.isChecked()
        psico = self.nuevo.psico.isChecked()
        dic = {'Fono': fono, 'TO': to, 'Psico': psico}
        return dic
    
    def agruparEquip(self):
        cama = self.nuevo.cama.isChecked()
        colchon = self.nuevo.colchon.isChecked()
        silla = self.nuevo.silla.isChecked()
        dic = {'Cama': cama, 'Colchon': colchon, 'Silla': silla}
        return dic
    
    def agruparAsisR(self):
        a = self.nuevo.arA.isChecked()
        b = self.nuevo.arB.isChecked()
        c = self.nuevo.arC.isChecked()
        dic = {'A': a, 'B': b, 'C': c}
        return dic

    def registrarPaciente(self):
        mBox = QMessageBox()
        if self.nuevo.cbObraSocial.currentText() == "--Seleccione--" or self.nuevo.cbModulo.currentText() == "--Seleccione--":            
            mBox.setText("Seleccione")
            mBox.exec()
            #self.nuevo.cbTipo.setFocus()
        elif len(self.nuevo.txtDocumento.text()) < 8:           
            mBox.setText("El número de documento ingresado es inválido")
            mBox.exec()
            #self.nuevo.txtApellido.setFocus() #Va al campo que debe completar
        else:
            fechaN = self.nuevo.txtFechaN.date().toPyDate().strftime("%d/%m/%Y") #formateo la fecha
            fechaI = self.nuevo.txtFechaI.date().toPyDate().strftime("%d/%m/%Y")
            
            subm =json.dumps(self.agruparSubm()) #Serializo el diccionario
            print(subm)
            equi = json.dumps(self.agruparEquip())
            asisR = json.dumps(self.agruparAsisR())
            nuevoPaciente = Paciente(
                nombre = self.nuevo.txtNombre.text(),
                apellido = self.nuevo.txtApellido.text(),
                domicilio = self.nuevo.txtDomicilio.text(),
                localidad = self.nuevo.txtLocalidad.text(),
                documento = int(self.nuevo.txtDocumento.text()),
                fechaNacimiento = fechaN,
                obraSocial = self.nuevo.cbObraSocial.currentText(),
                numAfiliado = int(self.nuevo.txtNroAfi.text()),
                telefono = self.nuevo.txtTelefono.text(),
                fechaIngreso = fechaI,
                fechaEgreso = "",
                motivo = "",
                activo = True,
                familiar = self.nuevo.txtFamiliar.text(),
                modulo = self.nuevo.cbModulo.currentText(),
                submodulo = subm,
                equip = equi,
                sopNutri = self.nuevo.cbSN.currentText(),
                asisRespi = asisR,
            )

            objData = PacienteData()
            
            mBox = QMessageBox()
            if objData.registrar(paciente=nuevoPaciente):                
                mBox.setText("Paciente registrado")      
                #self.limpiarCamposPaciente()          
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

############# Listado ################

    def abrirListado(self):           
        self.listado.btnBuscar.clicked.connect(self.buscar)  
        self.listado.tblListado.setColumnWidth(2,150)
        self.listado.tblListado.setColumnWidth(3,150)
        self.listado.tblListado.setColumnWidth(4,150)   
        self.listado.show()
        self.llenarTablaListado()

    def buscar(self):
        lis = ListadoData() 
        data = lis.buscarPorFecha(self.listado.txtFechaD.date().toPyDate().strftime("%d/%m/%Y"))
        print(data)
        fila = 0
        self.listado.tblListado.setRowCount(len(data)) #Cuantas filas traen los datos


    def llenarTablaListado(self):
        pass 