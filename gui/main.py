from ast import Lambda
from datetime import datetime
import json
import sqlite3
from PyQt6 import uic, QtCore
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout
from data.insumos import InsumoData
from data.listados import ListadoData
from data.paciente import PacienteData
from data.paciente_insumo import PacienteInsumoData
from data.profesional import ProfesionalData
from gui.nuevo_paciente import NuevoPacienteWindow
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

        #Botones del menú de main
        self.main.btnListado.clicked.connect(lambda: self.main.stackedWidget.setCurrentWidget(self.main.page_datos)) #Abro pagina de listados
        self.main.btnRegistrar.clicked.connect(lambda: self.main.stackedWidget.setCurrentWidget(self.main.page_registrar)) #Abro pagina de registros
        self.main.btnInsumos.clicked.connect(lambda: self.main.stackedWidget.setCurrentWidget(self.main.page_insumos)) #Actualizo
        #self.main.btnEliminar.clicked.connect(lambda: self.main.stackedWidget.setCurrentWidget(self.main.page_eliminar)) #Elimino
        #Listados
        self.main.listPacientes.clicked.connect(self.abrirListado)
        self.main.listProfesionales.clicked.connect(self.abrirListadoProfesionales)
        #Registros
        self.main.btnPaciente.clicked.connect(self.abrirRegistro)
        self.main.btnProfesional.clicked.connect(self.abrirRegistroProf)
        #Interfaz de distintas ventanas
        #Paciente
        self.nuevo = uic.loadUi("gui/nuevo_paciente.ui") #Abre la interfaz de agregar paciente
        self.listado = uic.loadUi("gui/listado_pacientes.ui") #Abre la interafz del listado
        self.ver = uic.loadUi("gui/ver_paciente.ui")
        self.actPac = uic.loadUi("gui/modificar_paciente.ui")
        #Profesional
        self.prof = uic.loadUi("gui/nuevo_profesional.ui")
        self.listadoProf = uic.loadUi("gui/listado_profesionales.ui")
        self.verProf = uic.loadUi("gui/ver_profesional.ui")
        self.actProf = uic.loadUi("gui/modificar_profesional.ui")
        #Insumos
        self.nInsumo = uic.loadUi("gui/cargar_insumo.ui")
        self.lInsumo = uic.loadUi("gui/listado_insumos.ui")

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


                    #### Pacientes ####
    def abrirRegistro(self):   
        self.nuevo.btnRegistrar.clicked.connect(self.registrarPaciente)     
        self.nuevo.show()

    def agruparSubm(self, ventana):
        if ventana == 'nuevo':
            fono = self.nuevo.fono.isChecked()
            to = self.nuevo.to.isChecked()
            psico = self.nuevo.psico.isChecked()
        else:
            fono = self.actPac.fono.isChecked()
            to = self.actPac.to.isChecked()
            psico = self.actPac.psico.isChecked()
        dic = {'Fono': fono, 'TO': to, 'Psico': psico}
        return dic
    
    def agruparEquip(self, ventana):
        if ventana == 'nuevo':
            cama = self.nuevo.cama.isChecked()
            colchon = self.nuevo.colchon.isChecked()
            silla = self.nuevo.silla.isChecked()
        else:
            cama = self.actPac.cama.isChecked()
            colchon = self.actPac.colchon.isChecked()
            silla = self.actPac.silla.isChecked()
        dic = {'Cama': cama, 'Colchon': colchon, 'Silla': silla}
        return dic
    
    def agruparAsisR(self, ventana):
        if ventana == 'nuevo':
            a = self.nuevo.arA.isChecked()
            b = self.nuevo.arB.isChecked()
            c = self.nuevo.arC.isChecked()
        else:
            a = self.actPac.arA.isChecked()
            b = self.actPac.arB.isChecked()
            c = self.actPac.arC.isChecked()
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
            
            subm =json.dumps(self.agruparSubm('nuevo')) #Serializo el diccionario
            print(subm)
            equi = json.dumps(self.agruparEquip('nuevo'))
            asisR = json.dumps(self.agruparAsisR('nuevo'))
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
        self.listado.btnBuscar.clicked.connect(self.buscarPac)  
        self.listado.tblListado.setColumnWidth(2,150)
        self.listado.tblListado.setColumnWidth(4,150)
        self.listado.tblListado.setColumnWidth(5,150)   
        self.listado.show()

    def buscarPac(self):
        lis = ListadoData() 
        data = lis.buscarPaciente(self.listado.txtDocumento.text(), self.listado.txtApellido.text())
        print(data)
        fila = 0
        self.listado.tblListado.setRowCount(len(data)) #Cuantas filas traen los datos
        for item in data:
            self.listado.tblListado.setItem(fila, 0, QTableWidgetItem(str(item[2]))) #Apellido
            self.listado.tblListado.setItem(fila, 1, QTableWidgetItem(str(item[1]))) #Nombre
            self.listado.tblListado.setItem(fila, 2, QTableWidgetItem(str(item[10]))) #Fecha de ingreso
            
            if item[11] == '':
                self.listado.tblListado.setItem(fila, 3, QTableWidgetItem("Activo"))
            else:
               self.listado.tblListado.setItem(fila, 3, QTableWidgetItem("Inactivo"))
            
            id_valor = item[0]
            
            # Crear el botón y añadirlo a la columna 7
            # Crear el botón "Ver más" y conectarlo
            btn = QPushButton("Ver más")
            btn.clicked.connect(lambda _, id_valor=id_valor: self.mostrarPaciente(id_valor))
            # Agregar estilo al botón
            btn.setStyleSheet("background-color: rgb(71, 40, 37); color: rgb(255, 255, 255);")
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.addWidget(btn)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.listado.tblListado.setCellWidget(fila, 4, widget)

            fila += 1
        
    def mostrarPaciente(self, id):
        objData = PacienteData()
        paciente = objData.mostrar(id)

        #self.ver.btnInsumos.clicked.connect(self.mostrarInsumos(id))

        self.ver.txtNombre.setText(paciente[1])
        self.ver.txtApellido.setText(paciente[2])
        self.ver.txtDomicilio.setText(paciente[3])
        self.ver.txtLocalidad.setText(paciente[4])
        self.ver.txtDocumento.setText(paciente[5])

        day, month, year = map(int, paciente[6].split("/"))
        date_qt = QDate(year, month, day)
        self.ver.txtFechaN.setDate(date_qt)
        
        self.ver.cbObraSocial.setCurrentText(paciente[7])
        self.ver.txtNroAfi.setText(paciente[8])
        self.ver.txtTelefono.setText(paciente[9])

        day, month, year = map(int, paciente[10].split("/"))
        date_qt = QDate(year, month, day)
        self.ver.txtFechaI.setDate(date_qt)

        if paciente[11] != '':
            day, month, year = map(int, paciente[11].split("/"))
            date_qt = QDate(year, month, day)
            self.ver.txtFechaE.setDate(date_qt)
        else:
            date_qt = QDate(2000, 1, 1)
            self.ver.txtFechaE.setDate(date_qt)

        
        self.ver.txtMotivo.setText(paciente[12])   
        self.ver.txtFamiliar.setText(paciente[14])
        self.ver.cbModulo.setCurrentText(paciente[15])

        dic = json.loads(paciente[16])
        
        #Submodulo
        self.ver.fono.setChecked(dic['Fono'])
        print(dic['Fono'])
        self.ver.to.setChecked(dic['TO'])
        print(dic['TO'])
        self.ver.psico.setChecked(dic['Psico'])
        print(dic['Psico'])
        dicE = json.loads(paciente[17])
        #Equipamiento
        self.ver.cama.setChecked(dicE['Cama'])
        self.ver.colchon.setChecked(dicE['Colchon'])
        self.ver.silla.setChecked(dicE['Silla'])

        self.ver.cbSN.setCurrentText(paciente[18])
        dicA = json.loads(paciente[19])
        #Asistencia Respiratoria
        self.ver.arA.setChecked(dicA['A'])
        self.ver.arB.setChecked(dicA['B'])
        self.ver.arC.setChecked(dicA['C'])

        self.ver.btnModificar.clicked.connect(lambda: self.abrirVentanaModificarP(id))
        self.ver.btnInsumos.clicked.connect(lambda: self.mostrarInsumos(id))        
        
        self.ver.show()

    def abrirVentanaModificarP(self, id):
        self.actualizarPaciente(id)
        self.actPac.show()

    def actualizarPaciente(self, id):
        objData = PacienteData()
        paciente = objData.mostrar(id)

        self.actPac.txtNombre.setText(paciente[1])
        self.actPac.txtApellido.setText(paciente[2])
        self.actPac.txtDomicilio.setText(paciente[3])
        self.actPac.txtLocalidad.setText(paciente[4])
        self.actPac.txtDocumento.setText(paciente[5])

        day, month, year = map(int, paciente[6].split("/"))
        date_qt = QDate(year, month, day)
        self.actPac.txtFechaN.setDate(date_qt)
        
        self.actPac.cbObraSocial.setCurrentText(paciente[7])
        self.actPac.txtNroAfi.setText(paciente[8])
        self.actPac.txtTelefono.setText(paciente[9])

        day, month, year = map(int, paciente[10].split("/"))
        date_qt = QDate(year, month, day)
        self.actPac.txtFechaI.setDate(date_qt)

        if paciente[11] != '':
            day, month, year = map(int, paciente[11].split("/"))
            date_qt = QDate(year, month, day)
            self.actPac.txtFechaE.setDate(date_qt)
        else:
            date_qt = QDate(2000, 1, 1)
            self.actPac.txtFechaE.setDate(date_qt)

        
        self.actPac.txtMotivo.setText(paciente[12])   
        self.actPac.txtFamiliar.setText(paciente[14])
        self.actPac.cbModulo.setCurrentText(paciente[15])

        dic = json.loads(paciente[16])
        
        #Submodulo
        self.actPac.fono.setChecked(dic['Fono'])
        self.actPac.to.setChecked(dic['TO'])
        self.actPac.psico.setChecked(dic['Psico'])
        dicE = json.loads(paciente[17])
        #Equipamiento
        self.actPac.cama.setChecked(dicE['Cama'])
        self.actPac.colchon.setChecked(dicE['Colchon'])
        self.actPac.silla.setChecked(dicE['Silla'])

        self.actPac.cbSN.setCurrentText(paciente[18])
        dicA = json.loads(paciente[19])
        #Asistencia Respiratoria
        self.actPac.arA.setChecked(dicA['A'])
        self.actPac.arB.setChecked(dicA['B'])
        self.actPac.arC.setChecked(dicA['C'])

        # Conectar el botón btnGuardar a guardarCambiosProfesional
        self.actPac.btnGuardar.clicked.connect(lambda: self.guardarCambiosPaciente(id))

    def guardarCambiosPaciente(self, id):
        fechaN = self.actPac.txtFechaN.date().toPyDate().strftime("%d/%m/%Y")
        fechaI = self.actPac.txtFechaI.date().toPyDate().strftime("%d/%m/%Y")
        fecha = self.actPac.txtFechaE.date().toPyDate().strftime("%d/%m/%Y")
        
        act = True
        if fecha != "01/01/2000": 
            fechaE = fecha
            act = False
        else:
            fechaE = ""

        subm =json.dumps(self.agruparSubm('act')) #Serializo el diccionario
        equi = json.dumps(self.agruparEquip('act'))
        asisR = json.dumps(self.agruparAsisR('act'))
        
        pacActualizado = Paciente(
            nombre = self.actPac.txtNombre.text(),
                apellido = self.actPac.txtApellido.text(),
                domicilio = self.actPac.txtDomicilio.text(),
                localidad = self.actPac.txtLocalidad.text(),
                documento = int(self.actPac.txtDocumento.text()),
                fechaNacimiento = fechaN,
                obraSocial = self.actPac.cbObraSocial.currentText(),
                numAfiliado = int(self.actPac.txtNroAfi.text()),
                telefono = self.actPac.txtTelefono.text(),
                fechaIngreso = fechaI,
                fechaEgreso = fechaE,
                motivo = self.actPac.txtMotivo.text(),
                activo = act,
                familiar = self.actPac.txtFamiliar.text(),
                modulo = self.actPac.cbModulo.currentText(),
                submodulo = subm,
                equip = equi,
                sopNutri = self.actPac.cbSN.currentText(),
                asisRespi = asisR,
        )
        
        objData = PacienteData()
        success, error_message = objData.modificar(id, pacActualizado)
        mBox = QMessageBox()
        if success:
            mBox.setText("Paciente actualizado correctamente")
        else:
            mBox.setText(f"El paciente no pudo ser actualizado: {error_message}")
        mBox.exec()

    
        
        


############### Profesionales ##################

    def abrirRegistroProf(self):   
        self.prof.btnRegistrar.clicked.connect(self.registrarProfesional)     
        self.prof.show()

    def registrarProfesional(self):
        mBox = QMessageBox()
        if self.prof.cbProfesional.currentText() == "--Seleccione--":            
            mBox.setText("Seleccione una profesión")
            mBox.exec()
            #self.nuevo.cbTipo.setFocus()
        elif len(self.prof.txtCbu1.text()) < 22 or len(self.prof.txtCbu2.text()) < 22:           
            mBox.setText("El CBU ingresado es inválido. Debe contener 22 números")
            mBox.exec()
            #self.nuevo.txtApellido.setFocus() #Va al campo que debe completar
        else:
            fechaN = self.nuevo.txtFechaN.date().toPyDate().strftime("%d/%m/%Y") #formateo la fecha
                        
            nuevoProfesional = Profesional(
                nombre = self.prof.txtNombre.text(),
                apellido = self.prof.txtApellido.text(),
                domicilio = self.prof.txtDomicilio.text(),
                localidad = self.prof.txtLocalidad.text(),
                CUIT = int(self.prof.txtCuit.text()),
                fechaNacimiento = fechaN,
                codPostal = self.prof.txtCP.text(),
                matricula = self.prof.txtMatricula.text(),
                telefono = self.prof.txtTelefono.text(),
                cbu1 = self.prof.txtCbu1.text(),
                cbu2 = self.prof.txtCbu2.text(),
                alias = self.prof.txtAlias.text(),
                mail = self.prof.txtMail.text(),
                monotributo = self.prof.monotributo.isChecked(),
                coord = self.prof.coordinador.isChecked(),
                profesional = self.prof.cbProfesional.currentText(),
                codTransf = self.prof.txtCodigo.text(),                
            )

            objData = ProfesionalData()
            
            mBox = QMessageBox()
            success, error_message = objData.registrar(profesional=nuevoProfesional)
            if success:                
                mBox.setText("Profesional registrado")      
                #self.limpiarCamposPaciente()         
            else:
                mBox.setText(f"El profesional no pudo ser registrado: {error_message}")
                  
            mBox.exec()

################## Listado ################

    def abrirListadoProfesionales(self):           
        self.listadoProf.btnBuscar.clicked.connect(self.buscar)  
        self.listadoProf.tblListadoProf.setColumnWidth(2,150)
        self.listadoProf.tblListadoProf.setColumnWidth(3,150)
        #self.listadoProf.tblListadoProf.setColumnWidth(5,150)   
        self.listadoProf.show()
    
    def buscar(self):
        lis = ListadoData() 
        data = lis.buscarProfesional(self.listadoProf.txtCuit.text(), self.listadoProf.txtApellido.text(), self.listadoProf.cbProfesion.currentText())
        print(data)
        fila = 0
        self.listadoProf.tblListadoProf.setRowCount(len(data)) #Cuantas filas traen los datos
        for item in data:
            self.listadoProf.tblListadoProf.setItem(fila, 0, QTableWidgetItem(str(item[2]))) #Apellido
            self.listadoProf.tblListadoProf.setItem(fila, 1, QTableWidgetItem(str(item[1]))) #Nombre
            self.listadoProf.tblListadoProf.setItem(fila, 2, QTableWidgetItem(str(item[10]))) #CBU
            if item[11] == '': #CBU2
                self.listadoProf.tblListadoProf.setItem(fila, 3, QTableWidgetItem("---"))
            else:
               self.listadoProf.tblListadoProf.setItem(fila, 3, QTableWidgetItem(str(item[11]))) 
           
            self.listadoProf.tblListadoProf.setItem(fila, 4, QTableWidgetItem(str(item[12]))) #Alias
            self.listadoProf.tblListadoProf.setItem(fila, 5, QTableWidgetItem(str(item[17]))) #Codigo
            self.listadoProf.tblListadoProf.setItem(fila, 6, QTableWidgetItem(str(item[16]))) #Profesion
            
            
            
            id_valor = item[0]
            
            # Crear el botón y añadirlo a la columna 7
            # Crear el botón "Ver más" y conectarlo
            btn = QPushButton("Ver más")
            btn.clicked.connect(lambda _, id_valor=id_valor: self.mostrarProfesional(id_valor))
            # Agregar estilo al botón
            btn.setStyleSheet("background-color: rgb(71, 40, 37); color: rgb(255, 255, 255);")
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.addWidget(btn)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.listadoProf.tblListadoProf.setCellWidget(fila, 7, widget)
        
            
            fila += 1

    def mostrarProfesional(self, id):
        objData = ProfesionalData()
        profesional = objData.mostrar(id)

        self.verProf.txtNombre.setText(profesional[1])
        self.verProf.txtApellido.setText(profesional[2])
        self.verProf.txtDomicilio.setText(profesional[3])
        self.verProf.txtLocalidad.setText(profesional[4])
        self.verProf.txtCuit.setText(profesional[5])

        day, month, year = map(int, profesional[6].split("/"))
        date_qt = QDate(year, month, day)
        self.verProf.txtFechaN.setDate(date_qt)
        
        self.verProf.txtCP.setText(profesional[7])
        self.verProf.txtMatricula.setText(profesional[8])
        self.verProf.txtTelefono.setText(profesional[9])
        self.verProf.txtCbu1.setText(profesional[10])
        self.verProf.txtCbu2.setText(profesional[11])
        self.verProf.txtAlias.setText(profesional[12])
        self.verProf.txtMail.setText(profesional[13])
        
        self.verProf.monotributo.setChecked(profesional[14] == 'True')
        self.verProf.coordinador.setChecked(profesional[15] == 'True')
        
        self.verProf.cbProfesional.setCurrentText(profesional[16])
        self.verProf.txtCodigo.setText(profesional[17])
        
        self.verProf.btnModificar.clicked.connect(lambda: self.abrirVentanaModificar(id))
        self.verProf.show()

    def abrirVentanaModificar(self, id):
        self.actualizarProfesional(id)
        self.actProf.show()

    def actualizarProfesional(self, id):
        objData = ProfesionalData()
        profesional = objData.mostrar(id)

        self.actProf.txtNombre.setText(profesional[1])
        self.actProf.txtApellido.setText(profesional[2])
        self.actProf.txtDomicilio.setText(profesional[3])
        self.actProf.txtLocalidad.setText(profesional[4])
        self.actProf.txtCuit.setText(profesional[5])

        day, month, year = map(int, profesional[6].split("/"))
        date_qt = QDate(year, month, day)
        self.actProf.txtFechaN.setDate(date_qt)
        
        self.actProf.txtCP.setText(profesional[7])
        self.actProf.txtMatricula.setText(profesional[8])
        self.actProf.txtTelefono.setText(profesional[9])
        self.actProf.txtCbu1.setText(profesional[10])
        self.actProf.txtCbu2.setText(profesional[11])
        self.actProf.txtAlias.setText(profesional[12])
        self.actProf.txtMail.setText(profesional[13])
        
        self.actProf.monotributo.setChecked(profesional[14] == 'True')
        self.actProf.coordinador.setChecked(profesional[15] == 'True')
        
        self.actProf.cbProfesional.setCurrentText(profesional[16])
        self.actProf.txtCodigo.setText(profesional[17])

        # Conectar el botón btnGuardar a guardarCambiosProfesional
        self.actProf.btnGuardar.clicked.connect(lambda: self.guardarCambiosProfesional(id))

    def guardarCambiosProfesional(self, id):
        fechaN = self.actProf.txtFechaN.date().toPyDate().strftime("%d/%m/%Y")
        profActualizado = Profesional(
            nombre=self.actProf.txtNombre.text(),
            apellido=self.actProf.txtApellido.text(),
            domicilio=self.actProf.txtDomicilio.text(),
            localidad=self.actProf.txtLocalidad.text(),
            CUIT=int(self.actProf.txtCuit.text()),
            fechaNacimiento=fechaN,
            codPostal=self.actProf.txtCP.text(),
            matricula=self.actProf.txtMatricula.text(),
            telefono=self.actProf.txtTelefono.text(),
            cbu1=self.actProf.txtCbu1.text(),
            cbu2=self.actProf.txtCbu2.text(),
            alias=self.actProf.txtAlias.text(),
            mail=self.actProf.txtMail.text(),
            monotributo=self.actProf.monotributo.isChecked(),
            coord=self.actProf.coordinador.isChecked(),
            profesional=self.actProf.cbProfesional.currentText(),
            codTransf=self.actProf.txtCodigo.text()
        )
        
        objData = ProfesionalData()
        success, error_message = objData.modificar(id, profActualizado)
        mBox = QMessageBox()
        if success:
            mBox.setText("Profesional actualizado correctamente")
        else:
            mBox.setText(f"El profesional no pudo ser actualizado: {error_message}")
        mBox.exec()
   
   ######## Insumos #########        

    def abrirRegistroInsumo(self, id):   
        self.nInsumo.btnRegistrar.clicked.connect(lambda: self.registrarInsumo(id))          
        self.nInsumo.show()

    def registrarInsumo(self, id_paciente):
        mBox = QMessageBox()
        if self.nInsumo.cbInsumo.currentText() == "--Seleccione--" and self.nInsumo.txtOtro.text() == '':            
            mBox.setText("Seleccione o escriba un insumo")
            mBox.exec()
        else:
            fechaE = self.nInsumo.txtFechaEnt.date().toPyDate().strftime("%d/%m/%Y") #formateo la fecha
            if self.nInsumo.txtOtro.text() == '':
                nuevoInsumo = Insumo(
                    fechaEntrega = fechaE,
                    nombre = self.nInsumo.cbInsumo.currentText(),
                    cantidad = self.nInsumo.txtCantI.text(),
                    paciente = id_paciente,     
                )
            else:
                nuevoInsumo = Insumo(
                    fechaEntrega = fechaE,
                    nombre = self.nInsumo.txtOtro.text(),
                    cantidad = self.nInsumo.txtCantO.text(), 
                    paciente = id_paciente,    
                )

            objData = InsumoData()
            
            mBox = QMessageBox()
            success, error_message = objData.registrar(insumo=nuevoInsumo)
            if success:             
                mBox.setText("Insumo agregado")      
                #self.limpiarCamposPaciente()         
            else:
                mBox.setText(f"El insumo no pudo ser agregado: {error_message}")
                  
            mBox.exec()
            self.nInsumo.close() #Cierro la ventana
            

    def mostrarInsumos(self, id_paciente):

        lis = InsumoData()
        insumos = lis.mostrar(id_paciente)        
        
        if insumos:
            self.lInsumo.tblListadoI.setRowCount(len(insumos))  # Configurar el número de filas
            print('entro')
            fila = 0
            for item in insumos:
                print(item)
                self.lInsumo.tblListadoI.setItem(fila, 0, QTableWidgetItem(str(item[1])))
                self.lInsumo.tblListadoI.setItem(fila, 1, QTableWidgetItem(str(item[2])))
                self.lInsumo.tblListadoI.setItem(fila, 2, QTableWidgetItem(str(item[3])))

                fila += 1
        
        self.lInsumo.btnInsumo.clicked.connect(lambda: self.abrirRegistroInsumo(id_paciente))
        self.lInsumo.btnRefrescar.clicked.connect(lambda: self.mostrarInsumos(id_paciente))
        self.lInsumo.show()
        