import json
import os
import sqlite3
import tempfile
from PyQt6.QtGui import QIcon
from PyQt6 import uic, QtCore, QtWidgets
from PyQt6.QtCore import Qt, QDate, QStandardPaths, QByteArray, QMimeType
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QFileDialog
from data.archivos import ArchivosData
from data.insumos import InsumoData
from data.listados import ListadoData
from data.paciente import PacienteData
from data.paciente_coordinador import PacienteCoordinadorData
from data.paciente_insumo import PacienteInsumoData
from data.paciente_profesionales import PacienteProfesionalesData
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
        self.lisProfPac = uic.loadUi("gui/listado_profesionales_paciente.ui")
        self.asocProf = uic.loadUi("gui/asociar_profesional.ui")
        #Insumos
        self.nInsumo = uic.loadUi("gui/cargar_insumo.ui")
        self.lInsumo = uic.loadUi("gui/listado_insumos.ui")
        #Coordinador
        self.nCoord = uic.loadUi("gui/asociar_coordinador.ui")
        #Archivos
        self.arc = uic.loadUi("gui/archivos.ui")

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
            mBox.setWindowTitle('Mensaje')
            mBox.setText("Seleccione una obra social o módulo")
            mBox.exec()
            #self.nuevo.cbTipo.setFocus()
        elif len(self.nuevo.txtDocumento.text()) < 8:  
            mBox.setWindowTitle('Error')         
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
                mBox.setWindowTitle('Mensaje')             
                mBox.setText("Paciente registrado")      
                self.limpiarCamposPaciente()          
            else:
                mBox.setWindowTitle('Error')
                mBox.setText("El paciente no pudo ser registrado")
                
            mBox.exec()
            self.nuevo.close() #Cierro la ventana

    def limpiarCamposPaciente(self):        
        self.nuevo.txtNombre.clear()
        self.nuevo.txtApellido.clear()
        self.nuevo.txtDomicilio.clear()
        self.nuevo.txtLocalidad.clear()
        self.nuevo.txtDocumento.clear()
        self.nuevo.txtFechaNacimiento.setDate(QtCore.QDate.currentDate())  # Restablece la fecha de nacimiento a la fecha actual
        self.nuevo.cbObraSocial.setCurrentIndex(0)  # Restablece el combobox a su estado inicial
        self.nuevo.txtNroAfi.clear()
        self.nuevo.txtTelefono.clear()
        self.nuevo.txtFechaIngreso.setDate(QtCore.QDate.currentDate())  # Restablece la fecha de ingreso a la fecha actual
        self.nuevo.txtFamiliar.clear()
        self.nuevo.cbModulo.setCurrentIndex(0)  # Restablece el combobox a su estado inicial
        self.nuevo.cbSN.setCurrentIndex(0)  # Restablece el combobox a su estado inicial
        # Limpiar checkboxes de submodulo
        self.nuevo.fono.setChecked(False)
        self.nuevo.to.setChecked(False)
        self.nuevo.psico.setChecked(False)
        # Limpiar checkboxes de Equipamiento
        self.nuevo.cama.setChecked(False)
        self.nuevo.colchon.setChecked(False)
        self.nuevo.silla.setChecked(False)
        # Limpiar checkboxes de Asistencia Respiratoria
        self.nuevo.arA.setChecked(False)
        self.nuevo.arB.setChecked(False)
        self.nuevo.arC.setChecked(False)
   
############# Listado ################
    def boton_listado(self, id_valor, fila, lista):
        # Crear el botón y añadirlo a la columna 7
        # Crear el botón "Ver más" y conectarlo
        btn = QPushButton("Ver más")
        if lista == 'paciente':
            btn.clicked.connect(lambda _, id_valor=id_valor: self.mostrarPaciente(id_valor))
        else:
            btn.clicked.connect(lambda _, id_valor=id_valor: self.mostrarProfesional(id_valor))
        # Agregar estilo al botón
        btn.setStyleSheet("background-color: rgb(71, 40, 37); color: rgb(255, 255, 255);")
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(btn)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if lista == 'paciente':
            self.listado.tblListado.setCellWidget(fila, 4, widget)
        else:
            self.listadoProf.tblListadoProf.setCellWidget(fila, 7, widget)

    def abrirListado(self):    
        lis = ListadoData() 
        data = lis.obtenerPacientes()    
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
            
            self.boton_listado(id_valor, fila, 'paciente')

            fila += 1

        self.listado.tblListado.setColumnWidth(2,150)
        self.listado.tblListado.setColumnWidth(4,150)
        self.listado.tblListado.setColumnWidth(5,150) 
        self.listado.btnBuscar.clicked.connect(lambda: self.buscarPac())
        self.listado.btnLista.setVisible(False)
        self.limpiar_campos_busqueda('paciente')
        self.listado.show()

    def buscarPac(self):
        if self.listado.txtApellido.text() == '' and self.listado.txtDocumento.text() == '':
            mBox = QMessageBox()
            mBox.setWindowTitle('Mensaje')
            mBox.setText('Ingrese datos a buscar')
            mBox.exec()
        else:
            self.listado.tblListado.clearContents()  # Limpiar contenido actual de la tabla
            self.listado.tblListado.setRowCount(0)
            lis = ListadoData() 
            data = lis.buscarPaciente(self.listado.txtDocumento.text(), self.listado.txtApellido.text())
            if data:
                # Reiniciar número de filas
                
                fila = 0
                for item in data:
                    self.listado.tblListado.insertRow(fila)
                    self.listado.tblListado.setItem(fila, 0, QTableWidgetItem(str(item[2]))) # Apellido
                    self.listado.tblListado.setItem(fila, 1, QTableWidgetItem(str(item[1]))) # Nombre
                    self.listado.tblListado.setItem(fila, 2, QTableWidgetItem(str(item[10]))) # Fecha de ingreso
                    
                    estado = "Activo" if item[11] == '' else "Inactivo"
                    self.listado.tblListado.setItem(fila, 3, QTableWidgetItem(estado))
                    
                    id_valor = item[0]
                    
                    self.boton_listado(id_valor, fila, 'paciente')
                    
                    fila += 1
            else:
                # Limpiar la tabla si no se encontraron resultados
                self.listado.tblListado.clearContents()
                self.listado.tblListado.setRowCount(0)
            self.listado.btnLista.setVisible(True)
            self.listado.btnLista.clicked.connect(lambda: self.abrirListado())

    def limpiar_campos_busqueda(self, lista):
        if lista == 'paciente':
            self.listado.txtDocumento.clear()  # Limpia el contenido del primer QLineEdit
            self.listado.txtApellido.clear()  # Limpia el contenido del segundo QLineEdit
        else:
            self.listadoProf.txtCuit.clear()  # Limpia el contenido del primer QLineEdit
            self.listadoProf.txtApellido.clear()
            self.listadoProf.cbProfesion.setCurrentIndex(0)

    def mostrarPaciente(self, id):
        data = PacienteCoordinadorData()
        coordinador = data.obtener_coordinador_de_paciente(id)
        if coordinador:
            nombre_completo = f"{coordinador[1]} {coordinador[2]}"
            self.ver.txtCoordinador.setText(nombre_completo)
            self.ver.swCoordinador.setCurrentIndex(0)
        else:
            self.ver.swCoordinador.setCurrentIndex(1)
            self.ver.btnAsignar.clicked.connect(lambda: self.cargar_nombres_coordinadores(id))
        
        objData = PacienteData()
        paciente = objData.mostrar(id)

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
        self.ver.btnProfesionales.clicked.connect(lambda: self.mostrarProfesionales(id))
        self.ver.btnCarpeta.clicked.connect(lambda: self.cargarArchivos(id))

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
            mBox.setWindowTitle('Mensaje')
            mBox.setText("Paciente actualizado correctamente")
        else:
            mBox.setWindowTitle('Error')
            mBox.setText(f"El paciente no pudo ser actualizado: {error_message}")
        mBox.exec()
        self.actPac.close() #Cierro la ventana

############### Profesionales ##################

    def abrirRegistroProf(self):   
        self.prof.btnRegistrar.clicked.connect(self.registrarProfesional)     
        self.prof.show()

    def registrarProfesional(self):
        mBox = QMessageBox()
        if self.prof.cbProfesional.currentText() == "--Seleccione--":    
            mBox.setWindowTitle('Mensaje')        
            mBox.setText("Seleccione una profesión")
            mBox.exec()
            #self.nuevo.cbTipo.setFocus()
        elif len(self.prof.txtCbu1.text()) < 22 or len(self.prof.txtCbu2.text()) < 22:           
            mBox.setWindowTitle('Error')
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
                mBox.setWindowTitle('Mensaje')             
                mBox.setText("Profesional registrado")      
                self.limpiarCamposProfesional()         
            else:
                mBox.setWindowTitle('Error')
                mBox.setText(f"El profesional no pudo ser registrado: {error_message}")
                  
            mBox.exec()
            self.prof.close() #Cierro la ventana

    def limpiarCamposProfesional(self):  
        self.prof.txtNombre.clear()
        self.prof.txtApellido.clear()
        self.prof.txtDomicilio.clear()
        self.prof.txtLocalidad.clear()
        self.prof.txtCuit.clear()
        self.prof.txtFechaNacimiento.setDate(QtCore.QDate.currentDate())  # Restablece la fecha de nacimiento a la fecha actual
        self.prof.txtCP.clear()  
        self.prof.txtMatricula.clear()
        self.prof.txtTelefono.clear()       
        self.prof.txtCbu1.clear()
        self.prof.txtCbu2clear() 
        self.prof.txtAlias.clear()
        self.prof.txtMail.clear()
        self.prof.cbProfesional.setCurrentIndex(0)
        self.prof.txtCodigo.clear()
        # Limpiar checkbox de monotributo
        self.prof.monotributo.setChecked(False)        
        # Limpiar checkbox de coordinador
        self.prof.coordinador.setChecked(False)
        
################## Listado ################

    def abrirListadoProfesionales(self): 
        lis = ListadoData() 
        data = lis.obtenerProfesionales()    
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
            
            self.boton_listado(id_valor, fila, 'prof')

            fila += 1
 
        self.listadoProf.tblListadoProf.setColumnWidth(2,150)
        self.listadoProf.tblListadoProf.setColumnWidth(3,150)
        
        self.listadoProf.btnBuscar.clicked.connect(lambda: self.buscar())
        self.listadoProf.btnLista.setVisible(False)
        self.limpiar_campos_busqueda('prof')   
        self.listadoProf.show()
    
    def buscar(self):
        self.listadoProf.tblListadoProf.clearContents()  # Limpiar contenido actual de la tabla
        self.listadoProf.tblListadoProf.setRowCount(0)
        lis = ListadoData() 
        data = lis.buscarProfesional(self.listadoProf.txtCuit.text(), self.listadoProf.txtApellido.text(), self.listadoProf.cbProfesion.currentText())
        if data:
              # Reiniciar número de filas
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
                
                self.boton_listado(id_valor, fila, 'prof')
                        
                fila += 1
        else:
            # Limpiar la tabla si no se encontraron resultados
            self.listadoProf.tblListadoProf.clearContents()
            self.listadoProf.tblListadoProf.setRowCount(0)
        self.listadoProf.btnLista.setVisible(True)
        self.listadoProf.btnLista.clicked.connect(lambda: self.abrirListadoProfesionales())
       
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
            mBox.setWindowTitle('Mensaje')
            mBox.setText("Profesional actualizado correctamente")
        else:
            mBox.setWindowTitle('Error')
            mBox.setText(f"El profesional no pudo ser actualizado: {error_message}")
        mBox.exec()
        self.actProf.close() #Cierro la ventana

    def cargar_nombres_profesionales(self, id_paciente):
        objData = ProfesionalData()
        profesionales = objData.obtener_profesionales()
        self.asocProf.cbProfesionales.clear()  # Limpiar ComboBox antes de agregar nuevos items

        if profesionales:
            self.asocProf.cbProfesionales.addItem('--Seleccione--')
            for id_profesional, nombre, apellido in profesionales:
                item = f"{nombre} {apellido}"
                self.asocProf.cbProfesionales.addItem(item, userData=id_profesional)
        else:
            self.asocProf.cbProfesionales.addItem("No hay profesionales cargados")

        # Conectar señal para actualizar ID del profesional seleccionado
        self.asocProf.cbProfesionales.currentIndexChanged.connect(lambda index: self.actualizar_id_profesional(index, id_paciente))

        # Conectar botón Registrar
        self.asocProf.btnRegistrar.clicked.connect(lambda: self.asociarProfesionalAPaciente(id_paciente, id_profesional))
        self.asocProf.show()

    def actualizar_id_profesional(self, index, id_paciente):
        id_profesional = None
        if index >= 0:
            item_data = self.asocProf.cbProfesionales.itemData(index)
            if item_data is not None:
                id_profesional = item_data
                print(f"ID del profesional seleccionado: {id_profesional}")
                #self.asociarProfesionalAPaciente(id_paciente, id_profesional)
            else:
                print("No se encontró el ID del profesional seleccionado.")
        else:
            print("No se seleccionó ningún profesional.")
        return id_profesional

    def asociarProfesionalAPaciente(self, id_paciente, id_profesional):
        try:
            if id_profesional != None:
                objData = PacienteProfesionalesData()
                exito = objData.asociar_profesional_a_paciente(id_paciente, id_profesional)
                mBox = QMessageBox()
                if exito:
                        mBox.setWindowTitle('Mensaje')
                        mBox.setText("Profesional asociado al paciente correctamente.")
                else:
                        mBox.setWindowTitle('Error')
                        mBox.setText("No se pudo asociar el profesional al paciente.")
                self.asocProf.close() #Cierro la ventana
        except Exception:
            mBox = QMessageBox()
            mBox.setWindowTitle('Mensaje')
            mBox.setText('Seleccione un profesional')
           
    def mostrarProfesionales(self, id_paciente):

            lis = PacienteProfesionalesData()
            profesionales = lis.obtener_profesionales_de_paciente(id_paciente)        
            
            if profesionales:
                self.lisProfPac.tblListadoPP.setRowCount(len(profesionales))  # Configurar el número de filas
                print(profesionales)
                fila = 0
                for item in profesionales:
                    print(item)
                    self.lisProfPac.tblListadoPP.setItem(fila, 0, QTableWidgetItem(str(item[2]))) #Apellido
                    self.lisProfPac.tblListadoPP.setItem(fila, 1, QTableWidgetItem(str(item[1]))) #Nombre
                    self.lisProfPac.tblListadoPP.setItem(fila, 2, QTableWidgetItem(str(item[16]))) #Profesión

                    fila += 1
            
            self.lisProfPac.btnProf.clicked.connect(lambda: self.cargar_nombres_profesionales(id_paciente))
            self.lisProfPac.btnRefrescar.clicked.connect(lambda: self.mostrarProfesionales(id_paciente))
            self.lisProfPac.show()

   ######## Insumos #########        

    def abrirRegistroInsumo(self, id):   
        self.nInsumo.btnRegistrar.clicked.connect(lambda: self.registrarInsumo(id))          
        self.nInsumo.show()

    def registrarInsumo(self, id_paciente):
        mBox = QMessageBox()
        if self.nInsumo.cbInsumo.currentText() == "--Seleccione--" and self.nInsumo.txtOtro.text() == '':            
            mBox.setWindowTitle('Mensaje')
            mBox.setText("Seleccione o escriba un insumo")
            mBox.exec()
        else:
            fechaE = self.nInsumo.txtFechaEnt.date().toPyDate().strftime("%d/%m/%Y") #formateo la fecha
            if self.nInsumo.txtOtro.text() == '':
                nuevoInsumo = Insumo(
                    fechaEntrega = fechaE,
                    nombre = self.nInsumo.cbInsumo.currentText(),
                    cantidad = self.nInsumo.txtCantI.text(),    
                )
            else:
                nuevoInsumo = Insumo(
                    fechaEntrega = fechaE,
                    nombre = self.nInsumo.txtOtro.text(),
                    cantidad = self.nInsumo.txtCantO.text(),   
                )

            objData = InsumoData()
            
            mBox = QMessageBox()
            success, error_message = objData.registrar(insumo=nuevoInsumo, id_paciente=id_paciente)
            if success:   
                mBox.setWindowTitle('Mensaje')          
                mBox.setText("Insumo agregado")      
                #self.limpiarCamposPaciente()         
            else:
                mBox.setWindowTitle('Error')
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

############## Coordinador - Paciente ################  

    def cargar_nombres_coordinadores(self, id_paciente):
        objData = ProfesionalData()
        profesionales = objData.obtener_coordinadores()

        self.nCoord.cbProfesionales.clear()  # Limpiar ComboBox antes de agregar nuevos items

        if profesionales:
            self.nCoord.cbProfesionales.addItem('--Seleccione--')
            for id_profesional, nombre, apellido in profesionales:
                item = f"{nombre} {apellido}"
                self.nCoord.cbProfesionales.addItem(item, userData=id_profesional)
        else:
            self.nCoord.cbProfesionales.addItem("No hay profesionales cargados")

        # Conectar señal para actualizar ID del profesional seleccionado
        self.nCoord.cbProfesionales.currentIndexChanged.connect(lambda index: self.actualizar_id_profesional_coordinador(index, id_paciente))

        # Conectar botón Registrar
        self.nCoord.btnAsignar.clicked.connect(lambda: self.asociarCoordinadorAPaciente(id_paciente, id_profesional))
        self.nCoord.show()

    def actualizar_id_profesional_coordinador(self, index, id_paciente):
        id_profesional = None
        if index >= 0:
            item_data = self.nCoord.cbProfesionales.itemData(index)
            if item_data is not None:
                id_profesional = item_data
                print(f"ID del profesional seleccionado: {id_profesional}")
                #self.asociarProfesionalAPaciente(id_paciente, id_profesional)
            else:
                print("No se encontró el ID del profesional seleccionado.")
        else:
            print("No se seleccionó ningún profesional.")
        return id_profesional

    def asociarCoordinadorAPaciente(self, id_paciente, id_profesional):
        try:
            if id_profesional != None:
                objData = PacienteCoordinadorData()
                exito = objData.asociar_coordinador_a_paciente(id_paciente, id_profesional)
                mBox = QMessageBox()
                if exito:
                    mBox.setWindowTitle('Mensaje')
                    mBox.setText("Coordinador asociado al paciente correctamente.")
                else:
                    mBox.setWindowTitle('Error')
                    mBox.setText("No se pudo asociar el coordinador al paciente.")
                self.nCoord.close() #Cierro la ventana
        except Exception:
            mBox = QMessageBox()
            mBox.setWindowTitle('Mensaje')
            mBox.setText('Seleccione un coordinador')    

############### Archivos ################

    def cargarArchivos(self, id_paciente):
        # Obtener la lista de archivos relacionados con el paciente desde la base de datos
        lis = ArchivosData()
        archivos = lis.obtener_archivos_por_paciente(id_paciente)
        
        if archivos:
            self.arc.swArchivos.setCurrentIndex(0)
            # Configura la tabla
            self.arc.tableWidget.setRowCount(len(archivos))
            self.arc.tableWidget.setColumnCount(1)
            self.arc.tableWidget.setHorizontalHeaderLabels(["Archivo"])

            # Añade los archivos a la tabla
            for fila, archivo in enumerate(archivos):
                # Añade los archivos a la tabla
                nombre_archivo = archivo[1]  # Accede al primer elemento de la tupla (nombre_archivo)
                contenido_archivo = archivo[2]  # Accede al segundo elemento de la tupla (contenido)

                # Agregar el nombre del archivo a la celda
                item_nombre = QTableWidgetItem(nombre_archivo)
                self.arc.tableWidget.setItem(fila, 0, item_nombre)
               
                # Guardar el contenido del archivo en el QTableWidgetItem
                item_nombre.setData(Qt.ItemDataRole.UserRole, contenido_archivo)
                self.arc.tableWidget.cellDoubleClicked.connect(lambda: self.manejarDobleClic(fila))
            self.arc.show()
        else:
            self.arc.swArchivos.setCurrentIndex(1)
            self.arc.show()
        
        self.arc.btnAgregar.clicked.connect(lambda: self.abrirArchivo(id_paciente))

    def manejarCeldaClic(self, item):
        '''Maneja el clic en una celda de la tabla de archivos'''
        # Verificar si el ítem tiene datos de usuario (UserRole)
        contenido_archivo = item.data(Qt.ItemDataRole.UserRole)
        if contenido_archivo:
            # Aquí puedes manejar la apertura o visualización del archivo según sea necesario
            print(f"Contenido del archivo seleccionado: {contenido_archivo}")

    def abrirArchivo(self, id_paciente):
        '''Abre el buscador de archivos para poder cargar un archivo'''
        options = QFileDialog.Option
        dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        file_types = "All files(*)"
        data_file, _ = QFileDialog.getOpenFileName(self.arc, "Abrir Archivo", dir, file_types)
        if data_file:
            print(f"Archivo seleccionado: {data_file}")
            with open(data_file, 'rb') as file:
                contenido = file.read()
                nombre_archivo = os.path.basename(data_file)
                # Guardar el archivo en la base de datos
                lis = ArchivosData()
                lis.guardar_archivo(nombre_archivo, contenido, id_paciente)


                # Recargar la tabla de archivos
                self.cargarArchivos(id_paciente)

    def manejarDobleClic(self, fila):
        item = self.arc.tableWidget.item(fila, 0)
        contenido_archivo = item.data(Qt.ItemDataRole.UserRole)
        if contenido_archivo:
            # Crear un archivo temporal para abrirlo con la aplicación predeterminada
            temp_file_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.TempLocation), item.text())
            with open(temp_file_path, 'wb') as temp_file:
                temp_file.write(contenido_archivo)

            # Abrir el archivo con la aplicación predeterminada del sistema
            if os.name == 'nt':  # Windows
               os.startfile(temp_file_path) 
            # elif os.name == 'posix':  # macOS, Linux
            #     subprocess.call(('xdg-open', temp_file_path))
                
