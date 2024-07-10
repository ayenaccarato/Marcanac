import json
import os

from PyQt6 import uic, QtCore
from PyQt6.QtCore import Qt, QDate, QStandardPaths
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMessageBox, QPushButton, QWidget, QHBoxLayout, QTableWidgetItem, QFileDialog
from data.archivos_paciente import ArchivosPacienteData
from data.listados import ListadoData
from data.paciente import PacienteData
from data.paciente_coordinador import PacienteCoordinadorData
from model.paciente import Paciente

class PacienteWindow():

    def initGUI(self):
        self.nuevo = uic.loadUi("gui/nuevo_paciente.ui") #Abre la interfaz de agregar paciente
        self.listado = uic.loadUi("gui/listado_pacientes.ui") #Abre la interafz del listado
        self.ver = uic.loadUi("gui/ver_paciente.ui")
        self.actPac = uic.loadUi("gui/modificar_paciente.ui")
        self.ePac = uic.loadUi("gui/mensaje_eliminar_pac.ui")
        #Archivos
        self.arc = uic.loadUi("gui/archivos_paciente.ui")

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
        elif len(self.nuevo.txtDocumento.text()) < 8:  
            mBox.setWindowTitle('Error')         
            mBox.setText("El número de documento ingresado es inválido")
            mBox.exec()
        else:
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
                documento = int(self.nuevo.txtDocumento.text()),
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

    def eliminar_paciente(self, id_paciente):
        self.ePac.show()
        # Mostrar un cuadro de diálogo de confirmación
        self.ePac.btnCancelar.clicked.connect(lambda: self.ePac.close())
        self.ePac.btnConfirmar.clicked.connect(lambda: self.confirmar(id_paciente))

    def confirmar(self, id_paciente):
        '''Se elimina el paciente, si confirman'''
        self.ePac.close()
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
        self.ver.close()

############### Listado ###############

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
                self.setRowBackgroundColor(fila, QColor(170, 255, 127))  # Verde
            else:
               self.setRowBackgroundColor(fila, QColor(255, 88, 66))  # Rojo
            
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

    def setRowBackgroundColor(self, row, color):
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

        self.ver.btnModificar.clicked.connect(lambda: self.abrirVentanaModificarP(id))
        self.ver.btnInsumos.clicked.connect(lambda: self.mostrarInsumos(id))        
        self.ver.btnProfesionales.clicked.connect(lambda: self.mostrarProfesionales(id))
        self.ver.btnCarpeta.clicked.connect(lambda: self.cargarArchivos(id))
        self.ver.btnEliminar.clicked.connect(lambda: self.eliminar_paciente(id))

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
        self.ver.show()

############### Archivos - Paciente ################

    def cargarArchivos(self, id_paciente):
        # Obtener la lista de archivos relacionados con el paciente desde la base de datos
        lis = ArchivosPacienteData()
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
                lis = ArchivosPacienteData()
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
        