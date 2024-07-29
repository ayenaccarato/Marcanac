from PyQt6 import uic, QtCore
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QMessageBox, QPushButton, QWidget, QHBoxLayout, QTableWidgetItem
from data.listados import ListadoData
from data.paciente_profesionales import PacienteProfesionalesData
from data.profesional import ProfesionalData
from gui.profesionales.archivos_profesional import ArchivosProfesionalWindow
from gui.profesionales.ver_profesional import VerProfesionalWindow
from model.profesional import Profesional
from model.usuario import Usuario

class ProfesionalWindow():

    def __init__(self, user: Usuario):
        self.usuario = user
        self.prof = uic.loadUi("gui/profesionales/nuevo_profesional.ui")
        self.listadoProf = uic.loadUi("gui/profesionales/listado_profesionales.ui")
        self.verProf = uic.loadUi("gui/profesionales/ver_profesional.ui")
        self.actProf = uic.loadUi("gui/profesionales/modificar_profesional.ui")

        self.asocProf = uic.loadUi("gui/pacientes/asociar_profesional.ui")
              

    def abrirRegistroProf(self):   
        self.prof.btnRegistrar.clicked.connect(self.registrarProfesional)     
        self.prof.show()

    def registrarProfesional(self):
        mBox = QMessageBox()
        if self.prof.cbProfesional.currentText() == "--Seleccione--":    
            mBox.setWindowTitle('Mensaje')        
            mBox.setText("Seleccione una profesión")
            mBox.exec()
        # elif len(self.prof.txtCbu1.text()) < 22:           
        #     mBox.setWindowTitle('Error')
        #     mBox.setText("El CBU 1 ingresado es inválido. Debe contener 22 números")
        #     mBox.exec()
        # elif len(self.prof.txtCbu2.text()) < 22:           
        #     mBox.setWindowTitle('Error')
        #     mBox.setText("El CBU 2 ingresado es inválido. Debe contener 22 números")
        #     mBox.exec()   
        # elif len(self.prof.txtCbu3.text()) != 0 and len(self.prof.txtCbu3.text()) < 22:           
        #     mBox.setWindowTitle('Error')
        #     mBox.setText("El CBU 3 ingresado es inválido. Debe contener 22 números")
        #     mBox.exec()          
        else:
            fechaN = self.prof.txtFechaN.date().toPyDate().strftime("%d/%m/%Y") #formateo la fecha
                        
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
                cuidador = self.prof.cuidador.isChecked(),
                codTransf = self.prof.txtCodigo.text(), 
                ### Datos de pago a terceros ### 
                nombre2 = self.prof.txtNombre_2.text(),
                apellido2 = self.prof.txtApellido_2.text(),
                CUIT2 = self.prof.txtCuit_2.text(),
                cbu3 = self.prof.txtCbu3.text()         
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
        self.prof.txtFechaN.setDate(QtCore.QDate.currentDate())  # Restablece la fecha de nacimiento a la fecha actual
        self.prof.txtCP.clear()  
        self.prof.txtMatricula.clear()
        self.prof.txtTelefono.clear()       
        self.prof.txtCbu1.clear()
        self.prof.txtCbu2.clear() 
        self.prof.txtAlias.clear()
        self.prof.txtMail.clear()
        self.prof.cbProfesional.setCurrentIndex(0)
        self.prof.txtCodigo.clear()
        # Limpiar checkbox de monotributo
        self.prof.monotributo.setChecked(False)        
        # Limpiar checkbox de coordinador
        self.prof.coordinador.setChecked(False)
        # Limpiar checkbox de cuidador
        self.prof.cuidador.setChecked(False)

        self.prof.txtNombre_2.clear(),
        self.prof.txtApellido_2.clear(),
        self.prof.txtCuit_2.clear(),
        self.prof.txtCbu3.clear()  

############# Listado ###############

    def boton_listado_profesional(self, id_valor, fila):
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
            self.listadoProf.tblListadoProf.setItem(fila, 5, QTableWidgetItem(str(item[18]))) #Codigo
            self.listadoProf.tblListadoProf.setItem(fila, 6, QTableWidgetItem(str(item[16]))) #Profesion

            id_valor = item[0]
            
            self.boton_listado_profesional(id_valor, fila)

            fila += 1
 
        self.listadoProf.tblListadoProf.setColumnWidth(2,150)
        self.listadoProf.tblListadoProf.setColumnWidth(3,150)
        
        self.listadoProf.btnBuscar.clicked.connect(lambda: self.buscar())
        self.listadoProf.btnLista.setVisible(False)
        self.limpiar_campos_busqueda()   
        self.listadoProf.show()
    
    def setRowBackgroundColor(self, row, color):
        # Verificar si la fila existe en la tabla antes de establecer el color
        if row < self.listado.tblListado.rowCount():
            for col in range(self.listado.tblListado.columnCount()):
                item = self.listado.tblListado.item(row, col)
                if item:
                    item.setBackground(color)

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
                
                self.boton_listado_profesional(id_valor, fila)
                        
                fila += 1
        else:
            # Limpiar la tabla si no se encontraron resultados
            self.listadoProf.tblListadoProf.clearContents()
            self.listadoProf.tblListadoProf.setRowCount(0)
        self.listadoProf.btnLista.setVisible(True)
        self.listadoProf.btnLista.clicked.connect(lambda: self.abrirListadoProfesionales())    

    def limpiar_campos_busqueda(self):        
        self.listadoProf.txtCuit.clear()  # Limpia el contenido del primer QLineEdit
        self.listadoProf.txtApellido.clear()
        self.listadoProf.cbProfesion.setCurrentIndex(0)

    def mostrarProfesional(self, id):
        archivos = ArchivosProfesionalWindow()
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
        self.verProf.cuidador.setChecked(profesional[17] == 'True'),
        self.verProf.txtCodigo.setText(profesional[18])
        
        ## Datos pago a terceros ##
        self.verProf.txtNombre_2.setText(profesional[19])
        self.verProf.txtApellido_2.setText(profesional[20])
        self.verProf.txtCuit_2.setText(profesional[21])
        self.verProf.txtCbu3.setText(profesional[22])

        self.verProf.btnModificar.clicked.connect(lambda: self.abrirVentanaModificar(id))
        self.verProf.btnCarpeta.clicked.connect(lambda: archivos.cargarArchivosProfesional(id_profesional=id))
        if self.usuario.rol == 'admin':
            self.verProf.btnEliminar.clicked.connect(lambda: self.eliminar_profesional(id))
        else:
            self.verProf.btnEliminar.setVisible(False)
            
        self.verProf.show()

    def abrirVentanaModificar(self, id):
        self.verProf.close()
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
        self.actProf.cuidador.setChecked(profesional[17] == 'True'),
        self.actProf.txtCodigo.setText(profesional[18])
        
        ## Datos pago a terceros ##
        self.actProf.txtNombre_2.setText(profesional[19])
        self.actProf.txtApellido_2.setText(profesional[20])
        self.actProf.txtCuit_2.setText(profesional[21])
        self.actProf.txtCbu3.setText(profesional[22])

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
            cuidador = self.actProf.cuidador.isChecked(),
            codTransf=self.actProf.txtCodigo.text(),
            ### Datos de pago a terceros ### 
            nombre2 = self.actProf.txtNombre_2.text(),
            apellido2 = self.actProf.txtApellido_2.text(),
            CUIT2 = self.actProf.txtCuit_2.text(),
            cbu3 = self.actProf.txtCbu3.text()     
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
        self.mostrarProfesional(id)
        self.verProf.show() #Vuelvo a abrir la ficha que estaban modificando

### Eliminar ###

    def eliminar_profesional(self, id_profesional):
        # Crear el cuadro de diálogo de confirmación
        mBox = QMessageBox()
        mBox.setWindowTitle('Confirmar eliminación')
        mBox.setText("¿Está seguro que desea eliminar este profesional?")

        # Añadir botones personalizados
        si_btn = mBox.addButton("Sí", QMessageBox.ButtonRole.YesRole)
        no_btn = mBox.addButton("No", QMessageBox.ButtonRole.NoRole)
        
        mBox.setDefaultButton(no_btn)
        mBox.exec()

        if mBox.clickedButton() == si_btn:
            self.confirmar(id_profesional)
        else:
            print("Eliminación cancelada")

    def confirmar(self, id_profesional):
        '''Se elimina el profesional, si confirman'''
        profesional = ProfesionalData()
        eliminado = profesional.eliminar(id_profesional)

        mBox = QMessageBox()
        if eliminado:
            mBox.setWindowTitle('Mensaje')
            mBox.setText("Profesional eliminado")
        else:
            mBox.setWindowTitle('Error')
            mBox.setText("El profesional no pudo ser eliminado")

        mBox.exec() 

        #Cierro las ventanas y vuelvo a abrir el listado para refrescar la informacion
        self.listadoProf.close()
        self.verProf.close()   
        self.abrirListadoProfesionales() 

####################
    
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
           
    

################# Coordinador - Paciente ###############
