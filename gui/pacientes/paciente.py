import json

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

import itertools
from reportlab.lib.pagesizes import A4




from PyQt6 import uic, QtCore
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QPushButton, QWidget, QHBoxLayout, QTableWidgetItem

from data.listados import ListadoData
from data.paciente import PacienteData
from data.paciente_coordinador import PacienteCoordinadorData
from data.paciente_profesionales import PacienteProfesionalesData
from data.profesional import ProfesionalData
from gui.pacientes.archivos_paciente import ArchivosPacienteWindow
from gui.insumos.insumos import InsumosWindow
from gui.profesionales.profesional import ProfesionalWindow
from model.paciente import Paciente
from model.usuario import Usuario

class PacienteWindow():

    def __init__(self, user: Usuario):
        self.usuario = user
        self.actPac = uic.loadUi("gui/pacientes/modificar_paciente.ui")
        
        self.listado = uic.loadUi("gui/pacientes/listado_pacientes.ui")
        self.nuevo = uic.loadUi("gui/pacientes/nuevo_paciente.ui")
        self.ver = uic.loadUi("gui/pacientes/ver_paciente.ui")
        #Coordinador
        self.nCoord = uic.loadUi("gui/pacientes/asociar_coordinador.ui")
        #Profesionales del paciente
        self.lisProfPac = uic.loadUi("gui/pacientes/listado_profesionales_paciente.ui")

### Registrar ###

    def abrirRegistro(self):   
        self.nuevo.btnRegistrar.clicked.connect(self.registrarPaciente)     
        self.nuevo.show()

    def registrarPaciente(self):
        mBox = QMessageBox()
        if self.nuevo.cbObraSocial.currentText() == "--Seleccione--" or self.nuevo.cbModulo.currentText() == "--Seleccione--":            
            mBox.setWindowTitle('Mensaje')
            mBox.setText("Seleccione una obra social o módulo")
            mBox.exec()

        elif len(self.nuevo.txtDocumento.text()) < 7:  
            mBox.setWindowTitle('Error')         
            mBox.setText("El número de documento ingresado es inválido")
            mBox.exec()
        else:
            if len(self.nuevo.txtDocumento.text()) == 7:
                doc = self.nuevo.txtDocumento.text()
                mBox = QMessageBox()
                mBox.setWindowTitle('Confirmar registro')
                mBox.setText(f"¿Es correcto el DNI ingresado? {doc}")

                # Añadir botones personalizados
                si_btn = mBox.addButton("Sí", QMessageBox.ButtonRole.YesRole)
                no_btn = mBox.addButton("No", QMessageBox.ButtonRole.NoRole)
                
                mBox.setDefaultButton(no_btn)
                mBox.exec()

                if mBox.clickedButton() == si_btn:
                    #Se agrega un 0 adelante para que complete los 8 digitos
                    doc = '0' + self.nuevo.txtDocumento.text()

                    fechaN = self.nuevo.txtFechaN.date().toPyDate().strftime("%d/%m/%Y") #formateo la fecha
                    fechaI = self.nuevo.txtFechaI.date().toPyDate().strftime("%d/%m/%Y")
                    
                    subm =json.dumps(self.agruparSubm('nuevo')) #Serializo el diccionario
                    
                    equi = json.dumps(self.agruparEquip('nuevo'))
                    asisR = json.dumps(self.agruparAsisR('nuevo'))
                    nuevoPaciente = Paciente(
                        nombre = self.nuevo.txtNombre.text(),
                        apellido = self.nuevo.txtApellido.text(),
                        domicilio = self.nuevo.txtDomicilio.text(),
                        localidad = self.nuevo.txtLocalidad.text(),
                        documento = int(doc),
                        fechaNacimiento = fechaN,
                        obraSocial = self.nuevo.cbObraSocial.currentText(),
                        numAfiliado = int(self.nuevo.txtNroAfi.text()),
                        telefono = self.nuevo.txtTelefono.text(),
                        fechaIngreso = fechaI,
                        fechaEgreso = "",
                        motivo = "",
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
                else:
                    print("Ingrese otro documento")
            

    def agruparSubm(self, ventana):
        ''' Convierto en un diccionario, 
        que submódulo tiene'''
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
        ''' Convierto en un diccionario, 
        que Equipamiento tiene'''
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
        ''' Convierto en un diccionario, 
        que asistencia respiratoria tiene'''
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
    
    def limpiarCamposPaciente(self):        
        self.nuevo.txtNombre.clear()
        self.nuevo.txtApellido.clear()
        self.nuevo.txtDomicilio.clear()
        self.nuevo.txtLocalidad.clear()
        self.nuevo.txtDocumento.clear()
        self.nuevo.txtFechaN.setDate(QtCore.QDate.currentDate())  # Restablece la fecha de nacimiento a la fecha actual
        self.nuevo.cbObraSocial.setCurrentIndex(0)  # Restablece el combobox a su estado inicial
        self.nuevo.txtNroAfi.clear()
        self.nuevo.txtTelefono.clear()
        self.nuevo.txtFechaI.setDate(QtCore.QDate.currentDate())  # Restablece la fecha de ingreso a la fecha actual
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

### Modificar ###

    def abrirVentanaModificarP(self, id):
        self.ver.close()
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
        self.actPac.txtFamiliar.setText(paciente[13])
        self.actPac.cbModulo.setCurrentText(paciente[14])

        dic = json.loads(paciente[15])
        
        #Submodulo
        self.actPac.fono.setChecked(dic['Fono'])
        self.actPac.to.setChecked(dic['TO'])
        self.actPac.psico.setChecked(dic['Psico'])
        dicE = json.loads(paciente[16])
        #Equipamiento
        self.actPac.cama.setChecked(dicE['Cama'])
        self.actPac.colchon.setChecked(dicE['Colchon'])
        self.actPac.silla.setChecked(dicE['Silla'])

        self.actPac.cbSN.setCurrentText(paciente[17])
        dicA = json.loads(paciente[18])
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
        
        if fecha != "01/01/2000": 
            fechaE = fecha
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
        
        self.mostrarPaciente(id)
       
        self.listado.abrirListado()
        
        self.ver.close()

### Ver ###

    def mostrarPaciente(self, id):
        insumosList = InsumosWindow()
        data = PacienteCoordinadorData()
        
        archivos = ArchivosPacienteWindow()
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
        self.ver.txtFamiliar.setText(paciente[13])
        self.ver.cbModulo.setCurrentText(paciente[14])

        dic = json.loads(paciente[15])
        
        #Submodulo
        self.ver.fono.setChecked(dic["Fono"])        
        self.ver.to.setChecked(dic['TO'])        
        self.ver.psico.setChecked(dic['Psico'])
        
        dicE = json.loads(paciente[16])
        #Equipamiento
        self.ver.cama.setChecked(dicE['Cama'])
        self.ver.colchon.setChecked(dicE['Colchon'])
        self.ver.silla.setChecked(dicE['Silla'])

        self.ver.cbSN.setCurrentText(paciente[17])
        dicA = json.loads(paciente[18])
        #Asistencia Respiratoria
        self.ver.arA.setChecked(dicA['A'])
        self.ver.arB.setChecked(dicA['B'])
        self.ver.arC.setChecked(dicA['C'])

        self.ver.btnModificar.clicked.connect(lambda: self.abrirVentanaModificarP(id=id))
        self.ver.btnInsumos.clicked.connect(lambda: insumosList.mostrarInsumos(id_paciente=id))        
        self.ver.btnProfesionales.clicked.connect(lambda: self.mostrarProfesionales(id_paciente=id))
        self.ver.btnCarpeta.clicked.connect(lambda: archivos.cargarArchivos(id_paciente=id))
        if self.usuario.rol == 'admin':
            self.ver.btnEliminar.clicked.connect(lambda: self.eliminar_paciente(id))
        else:
            self.ver.btnEliminar.setVisible(False)
        
        self.ver.btnDescargar.clicked.connect(lambda: self.descargar_pdf(id_paciente=id))

        self.ver.show()

### Eliminar ###

    def eliminar_paciente(self, id_paciente):
        # Crear el cuadro de diálogo de confirmación
        mBox = QMessageBox()
        mBox.setWindowTitle('Confirmar eliminación')
        mBox.setText("¿Está seguro que desea eliminar este paciente?")

        # Añadir botones personalizados
        si_btn = mBox.addButton("Sí", QMessageBox.ButtonRole.YesRole)
        no_btn = mBox.addButton("No", QMessageBox.ButtonRole.NoRole)
        
        mBox.setDefaultButton(no_btn)
        mBox.exec()

        if mBox.clickedButton() == si_btn:
            self.confirmar(id_paciente)
        else:
            print("Eliminación cancelada")

    def confirmar(self, id_paciente):
        '''Se elimina el profesional, si confirman'''
        paciente = PacienteData()
        eliminado = paciente.eliminar(id_paciente)

        mBox = QMessageBox()
        if eliminado:
            mBox.setWindowTitle('Mensaje')
            mBox.setText("Paciente eliminado")
        else:
            mBox.setWindowTitle('Error')
            mBox.setText("El paciente no pudo ser eliminado")

        mBox.exec()

        self.listado.close()
        self.ver.close()
        self.abrirListado()

### Listado ###

    def boton_listado_paciente(self, id_valor, fila):
        
        
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
       
        self.listado.tblListado.setCellWidget(fila, 3, widget)

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
                self.setRowBackgroundColorP(fila, QColor(170, 255, 127))  # Verde
            else:
               self.setRowBackgroundColorP(fila, QColor(255, 88, 66))  # Rojo
            
            id_valor = item[0]
            
            self.boton_listado_paciente(id_valor, fila)

            fila += 1

        self.listado.tblListado.setColumnWidth(2,150)
        self.listado.tblListado.setColumnWidth(4,150)
        self.listado.tblListado.setColumnWidth(5,150) 
        self.listado.btnBuscar.clicked.connect(lambda: self.buscarPac())
        self.listado.btnLista.setVisible(False)
        self.limpiar_campos_busqueda()
        self.listado.show()

    def setRowBackgroundColorP(self, row, color):
        # Verificar si la fila existe en la tabla antes de establecer el color
        if row < self.listado.tblListado.rowCount():
            for col in range(self.listado.tblListado.columnCount()):
                item = self.listado.tblListado.item(row, col)
                if item:
                    item.setBackground(color)

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
                    
                    self.boton_listado_paciente(id_valor, fila)
                    
                    fila += 1
            else:
                # Limpiar la tabla si no se encontraron resultados
                self.listado.tblListado.clearContents()
                self.listado.tblListado.setRowCount(0)
            self.listado.btnLista.setVisible(True)
            self.listado.btnLista.clicked.connect(lambda: self.abrirListado())

    def limpiar_campos_busqueda(self):
        self.listado.txtDocumento.clear()  # Limpia el contenido del primer QLineEdit
        self.listado.txtApellido.clear()  # Limpia el contenido del segundo QLin

### Paciente - Coordinador ###

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
            self.nCoord.cbProfesionales.addItem("No hay coordinadores cargados")

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

### Paciente - Profesionales ###

    def mostrarProfesionales(self, id_paciente):
            profesional = ProfesionalWindow(self.usuario)

            lis = PacienteProfesionalesData()
            profesionales = lis.obtener_profesionales_de_paciente(id_paciente)        
            
            if profesionales:
                self.lisProfPac.tblListadoPP.setRowCount(len(profesionales))  # Configurar el número de filas
                
                fila = 0
                for item in profesionales:
                    
                    self.lisProfPac.tblListadoPP.setItem(fila, 0, QTableWidgetItem(str(item[2]))) #Apellido
                    self.lisProfPac.tblListadoPP.setItem(fila, 1, QTableWidgetItem(str(item[1]))) #Nombre
                    self.lisProfPac.tblListadoPP.setItem(fila, 2, QTableWidgetItem(str(item[16]))) #Profesión

                    fila += 1
            
            self.lisProfPac.btnProf.clicked.connect(lambda: profesional.cargar_nombres_profesionales(id_paciente))
            self.lisProfPac.btnRefrescar.clicked.connect(lambda: self.mostrarProfesionales(id_paciente))
            self.lisProfPac.show()


##############
    # def descargar_pdf(self, id_paciente):
    #     # Obtener la información del paciente
    #     paciente = PacienteData()
    #     data = paciente.mostrar(id_paciente)
    #     paciente_data = {
    #         'nombre': data[1],
    #         'apellido': data[2],
    #         'documento': data[5],
    #         'fecha_nacimiento': data[6],
    #         'direccion': data[3],
    #         'telefono': data[9]
    #     }
        
    #     # Generar el PDF
    #     archivo_pdf = self.generar_pdf_paciente(paciente_data)
        
    #     # Mostrar diálogo para guardar el archivo
    #     filePath, _ = QFileDialog.getSaveFileName(self.ver, "Guardar PDF", archivo_pdf, "PDF Files (*.pdf)")
    #     if filePath:
    #         # Renombrar el archivo al nombre seleccionado por el usuario
    #         import os
    #         os.rename(archivo_pdf, filePath)
    #         mBox = QMessageBox()
    #         mBox.setWindowTitle('Mensaje')
    #         mBox.setText('PDF generado y guardado exitosamente')
    #         mBox.exec()

    def descargar_pdf(self, id_paciente):
        try:
            # Obtener la información del paciente
            paciente = PacienteData()
            data = paciente.mostrar(id_paciente)
            paciente_data = {
                'nombre': data[1],
                'apellido': data[2],
                'dni': data[5],
                'fecha_nacimiento': data[6],
                'direccion': data[3],
                'telefono': data[9]
            }
            
            # Mostrar el cuadro de diálogo para guardar el archivo PDF
            filePath, _ = QFileDialog.getSaveFileName(self.ver, "Guardar PDF", f"{paciente_data['nombre']}_{paciente_data['apellido']}.pdf", "PDF Files (*.pdf)")
            
            if filePath:
                # Generar el PDF
                if self.generar_pdf_paciente(paciente_data, filePath):
                    QMessageBox.information(None, "Éxito", "El PDF se guardó correctamente.")
                else:
                    QMessageBox.warning(None, "Error", "No se pudo guardar el PDF.")
            else:
                QMessageBox.warning(None, "Advertencia", "No se seleccionó ningún archivo para guardar.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Ocurrió un error: {str(e)}")

# Función para generar el PDF (definida anteriormente)
    # def generar_pdf_paciente(self, paciente_data):
    #     from reportlab.lib.pagesizes import letter
    #     from reportlab.pdfgen import canvas

    #     # Definir el nombre del archivo PDF
    #     archivo_pdf = f"{paciente_data['nombre']}_{paciente_data['apellido']}.pdf"
        
    #     document = SimpleDocTemplate(archivo_pdf, pagesize=letter)
    #     styles = getSampleStyleSheet()
    #     content = []

    #     # Añadir Título
    #     title_style = styles['Title']
    #     content.append(Paragraph("Paciente", title_style))

    #     # Añadir Información del Paciente
    #     normal_style = styles['Normal']
    #     content.append(Paragraph(f"Nombre: {paciente_data['nombre']}", normal_style))
    #     content.append(Paragraph(f"Apellido: {paciente_data['apellido']}", normal_style))
    #     content.append(Paragraph(f"DNI: {paciente_data['documento']}", normal_style))
    #     content.append(Paragraph(f"Fecha de Nacimiento: {paciente_data['fecha_nacimiento']}", normal_style))
    #     content.append(Paragraph(f"Dirección: {paciente_data['direccion']}", normal_style))
    #     content.append(Paragraph(f"Teléfono: {paciente_data['telefono']}", normal_style))

    #     # Generar PDF
    #     document.build(content)
    #     return archivo_pdf

        # # Crear un canvas para el PDF
        # c = canvas.Canvas(archivo_pdf, pagesize=letter)
        # width, height = letter
        
        # # Agregar contenido al PDF
        # c.setFont("Helvetica", 12)
        # c.drawString(100, height - 100, f"Nombre: {paciente_data['nombre']}")
        # c.drawString(100, height - 120, f"Apellido: {paciente_data['apellido']}")
        # c.drawString(100, height - 140, f"DNI: {paciente_data['documento']}")
        # c.drawString(100, height - 160, f"Fecha de Nacimiento: {paciente_data['fecha_nacimiento']}")
        # c.drawString(100, height - 180, f"Dirección: {paciente_data['direccion']}")
        # c.drawString(100, height - 200, f"Teléfono: {paciente_data['telefono']}")
        
        # # Agregar más información según sea necesario
        
        # # Guardar el PDF
        # c.showPage()
        # c.save()
        
        # return archivo_pdf

    def generar_pdf_paciente(self, paciente_data, filePath):
        try:
            c = canvas.Canvas(filePath, pagesize=A4)
            width, height = A4
            margin = 50
            line_height = 20
            
            # Ajustar el título
            c.setFont("Helvetica-Bold", 12)
            title_x = margin
            title_y = height - margin
            c.drawString(title_x, title_y, "Información del Paciente")
            
            # Ajustar el espacio después del título
            current_y = title_y - line_height
            
            # Ajustar los campos
            c.setFont("Helvetica", 10)
            col_widths = [150, 300]  # Ancho de las columnas
            max_cols = 2  # Número máximo de columnas por línea
            
            fields = [
                ('Nombre', paciente_data['nombre']),
                ('Apellido', paciente_data['apellido']),
                ('DNI', paciente_data['dni']),
                ('Fecha de Nacimiento', paciente_data['fecha_nacimiento']),
                ('Dirección', paciente_data['direccion']),
                ('Teléfono', paciente_data['telefono'])
            ]
            
            for i, (field, value) in enumerate(fields):
                col = i % max_cols
                row = i // max_cols
                
                # Calcular posiciones para el campo
                x = margin + col * (col_widths[col] + 20)
                y = current_y - row * (line_height * 1.5)
                
                # Ajustar el ancho máximo para el texto
                text_width = col_widths[col] - 20
                
                # Dibujar campo y valor
                c.drawString(x, y, f"{field}:")
                c.drawString(x + text_width, y, value[:text_width])
                
                # Ajustar el ancho del campo y valor en caso de desbordamiento
                if len(value) > text_width:
                    lines = [value[i:i + text_width] for i in range(0, len(value), text_width)]
                    for j, line in enumerate(lines):
                        c.drawString(x + text_width, y - (j + 1) * line_height, line)
            
            # Finalizar el PDF
            c.save()
            return True
        except Exception as e:
            print(f"Error al generar el PDF: {str(e)}")
            return False