import json
import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from PyQt6 import uic, QtCore
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QPushButton, QWidget, QHBoxLayout, QTableWidgetItem, QTableWidget

from data.listados import ListadoData
from data.paciente import PacienteData
from data.paciente_coordinador import PacienteCoordinadorData
from data.paciente_profesionales import PacienteProfesionalesData
from data.profesional import ProfesionalData
from gui.pacientes.archivos_paciente import ArchivosPacienteWindow
from gui.insumos.insumos import InsumosWindow
from gui.pacientes.historia_clinica import HistoriaClinicaWindow
from gui.profesionales.profesional import ProfesionalWindow
from model.paciente import Paciente
from model.usuario import Usuario

class PacienteWindow():

    def __init__(self, user: Usuario):
        #Creo las tablas
        PacienteData()
        PacienteCoordinadorData()
        PacienteProfesionalesData()
        #Me guardo el usuario logueado
        self.usuario = user
        
        # Cargar UI para modificar paciente
        ui_file = os.path.join(os.path.dirname(__file__), '..', 'pacientes', 'modificar_paciente.ui')
        ui_file = os.path.abspath(ui_file)
        if not os.path.isfile(ui_file):
            print(f"Error: el archivo {ui_file} no se encuentra.")
            return
        self.actPac = uic.loadUi(ui_file)

        # Cargar UI para listado de pacientes
        try:
            ui_file_lis = os.path.join(os.path.dirname(__file__), '..', 'pacientes', 'listado_pacientes.ui')
            ui_file_lis = os.path.abspath(ui_file_lis)
            if not os.path.isfile(ui_file_lis):
                print(f"Error: el archivo {ui_file_lis} no se encuentra.")
                return
            self.listado = uic.loadUi(ui_file_lis)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error aa: {e}")
            print(f"Ruta del archivo listado_pacientes.ui: {ui_file_lis}")
            print(f"Existe el archivo: {os.path.isfile(ui_file_lis)}")
        
        # Cargar UI para nuevo paciente
        ui_file_n = os.path.join(os.path.dirname(__file__), '..', 'pacientes', 'nuevo_paciente.ui')
        ui_file_n = os.path.abspath(ui_file_n)
        if not os.path.isfile(ui_file_n):
            print(f"Error: el archivo {ui_file_n} no se encuentra.")
            return
        self.nuevo = uic.loadUi(ui_file_n)
        
        # Cargar UI para ver paciente
        ui_file_ver = os.path.join(os.path.dirname(__file__), '..', 'pacientes', 'ver_paciente.ui')
        ui_file_ver = os.path.abspath(ui_file_ver)
        if not os.path.isfile(ui_file_ver):
            print(f"Error: el archivo {ui_file_ver} no se encuentra.")
            return
        self.ver = uic.loadUi(ui_file_ver)
        
        # Cargar UI para asociar coordinador
        ui_file_c = os.path.join(os.path.dirname(__file__), '..', 'pacientes', 'asociar_coordinador.ui')
        ui_file_c = os.path.abspath(ui_file_c)
        if not os.path.isfile(ui_file_c):
            print(f"Error: el archivo {ui_file_c} no se encuentra.")
            return
        self.nCoord = uic.loadUi(ui_file_c)
        
        # Cargar UI para listado de profesionales del paciente
        ui_file_lisP = os.path.join(os.path.dirname(__file__), '..', 'pacientes', 'listado_profesionales_paciente.ui')
        ui_file_lisP = os.path.abspath(ui_file_lisP)
        if not os.path.isfile(ui_file_lisP):
            print(f"Error: el archivo {ui_file_lisP} no se encuentra.")
            return
        self.lisProfPac = uic.loadUi(ui_file_lisP)

        # Cargar UI para asociar paciente
        ui_file_pac = os.path.join(os.path.dirname(__file__), '..', 'profesionales', 'asociar_paciente.ui')
        ui_file_pac = os.path.abspath(ui_file_pac)
        if not os.path.isfile(ui_file_pac):
            print(f"Error: el archivo {ui_file_pac} no se encuentra.")
            return
        self.asocPac = uic.loadUi(ui_file_pac)

### Registrar ###

    def abrirRegistro(self):  
        try:
            self.nuevo.btnRegistrar.clicked.disconnect()
        except TypeError:
            pass
        self.nuevo.btnRegistrar.clicked.connect(self.registrarPaciente)     
        self.nuevo.showMaximized() #Maximizo la ventana
        #self.nuevo.show()     

    def registro(self, doc):
        fechaN = self.nuevo.txtFechaN.date().toPyDate().strftime("%d/%m/%Y") #formateo la fecha
        fechaI = self.nuevo.txtFechaI.date().toPyDate().strftime("%d/%m/%Y")
                    
        subm =json.dumps(self.agruparSubm('nuevo')) #Serializo el diccionario
                    
        equi = json.dumps(self.agruparEquip('nuevo'))
        asisR = json.dumps(self.agruparAsisR('nuevo'))
        nuevoPaciente = Paciente(
            nombre = self.nuevo.txtNombre.text().capitalize(),
            apellido = self.nuevo.txtApellido.text().capitalize(),
            domicilio = self.nuevo.txtDomicilio.text().capitalize(),
            localidad = self.nuevo.txtLocalidad.text().capitalize(),
            documento = int(doc),
            fechaNacimiento = fechaN,
            obraSocial = self.nuevo.cbObraSocial.currentText(),
            numAfiliado = int(self.nuevo.txtNroAfi.text()),
            telefono = self.nuevo.txtTelefono.text(),
            fechaIngreso = fechaI,
            fechaEgreso = "",
            motivo = "",
            familiar = self.nuevo.txtFamiliar.text().capitalize(),
            parentesco = self.nuevo.txtParentesco.text(),
            telFamiliar = self.nuevo.txtTelFamiliar.text(),
            modulo = self.nuevo.cbModulo.currentText(),
            submodulo = subm,
            equip = equi,
            sopNutri = self.nuevo.cbSN.currentText(),
            asisRespi = asisR,
        )

        objData = PacienteData()                    
                   
        if objData.registrar(paciente=nuevoPaciente):   
            print('registro')
            QMessageBox.information(None, 'Mensaje', 'Paciente registrado')   
            self.limpiarCamposPaciente()          
        else:
            QMessageBox.warning(None, 'Error', 'El paciente no pudo ser registrado')
                        
        self.nuevo.close() #Cierro la ventana

    def registrarPaciente(self):
        
        if self.nuevo.cbObraSocial.currentText() == "--Seleccione--" or self.nuevo.cbModulo.currentText() == "--Seleccione--":            
            QMessageBox.information(None, 'Mensaje', 'Seleccione una obra social o módulo')
        elif len(self.nuevo.txtNroAfi.text()) < 12:
            QMessageBox.information(None, 'Mensaje', 'El número de afiliado debe contener 12 números')
        elif len(self.nuevo.txtDocumento.text()) < 7:  
            QMessageBox.warning(None, 'Error', 'El número de documento ingresado es inválido')
        elif len(self.nuevo.txtDocumento.text()) == 7:
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
                    print('aaa')
                    #Se agrega un 0 adelante para que complete los 8 digitos
                    doc = '0' + self.nuevo.txtDocumento.text()
                    self.registro(doc)
                else:
                    print("Ingrese otro documento")
        else:
            doc = self.nuevo.txtDocumento.text()
            self.registro(doc)
            
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
        #self.actPac.show()
        self.actPac.showMaximized() #Maximizo la ventana

    def actualizarPaciente(self, id):
        try:
            
            objData = PacienteData()
            paciente = objData.mostrar(id)

            self.actPac.txtNombre.setText(paciente[1])
            self.actPac.txtApellido.setText(paciente[2])
            self.actPac.txtDomicilio.setText(paciente[3])
            self.actPac.txtLocalidad.setText(paciente[4])
            self.actPac.txtDocumento.setText(paciente[5])

            self.set_fecha(paciente[6], self.actPac.txtFechaN)
            self.set_fecha(paciente[10], self.actPac.txtFechaI)
            self.set_fecha(paciente[11], self.actPac.txtFechaE)

            self.actPac.cbObraSocial.setCurrentText(paciente[7])
            self.actPac.txtNroAfi.setText(paciente[8])
            self.actPac.txtTelefono.setText(paciente[9])

            self.actPac.txtMotivo.setText(paciente[12])
            self.actPac.txtFamiliar.setText(paciente[13])
            self.ver.txtParentesco.setText(paciente[14])
            self.ver.txtTelFamiliar.setText(paciente[15])
            self.actPac.cbModulo.setCurrentText(paciente[16])

            dic = json.loads(paciente[17])
            
            # Submodulo
            self.actPac.fono.setChecked(dic['Fono'])
            self.actPac.to.setChecked(dic['TO'])
            self.actPac.psico.setChecked(dic['Psico'])

            dicE = json.loads(paciente[18])
            # Equipamiento
            self.actPac.cama.setChecked(dicE['Cama'])
            self.actPac.colchon.setChecked(dicE['Colchon'])
            self.actPac.silla.setChecked(dicE['Silla'])

            self.actPac.cbSN.setCurrentText(paciente[19])
            dicA = json.loads(paciente[20])
            # Asistencia Respiratoria
            self.actPac.arA.setChecked(dicA['A'])
            self.actPac.arB.setChecked(dicA['B'])
            self.actPac.arC.setChecked(dicA['C'])

            try:
                self.actPac.btnGuardar.clicked.disconnect()
            except TypeError:
                pass

            # Conectar el botón btnGuardar a guardarCambiosPaciente
            self.actPac.btnGuardar.clicked.connect(lambda: self.guardarCambiosPaciente(id))
        except Exception as e:
            QMessageBox.critical(None, 'Error', f"Error: {e}")

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
                parentesco = self.actPac.txtParentesco.text(),
                telFamiliar = self.actPac.txtTelFamiliar.text(),
                modulo = self.actPac.cbModulo.currentText(),
                submodulo = subm,
                equip = equi,
                sopNutri = self.actPac.cbSN.currentText(),
                asisRespi = asisR,
        )
        
        objData = PacienteData()
        success, error_message = objData.modificar(id, pacActualizado)
        
        if success:
            QMessageBox.information(None, 'Mensaje', 'Paciente actualizado correctamente')

        else:
            QMessageBox.warning(None, 'Error', f'El paciente no pudo ser actualizado: {error_message}')
        
        self.actPac.close() #Cierro la ventana
        
        self.mostrarPaciente(id)
        self.ver.show()

### Ver ###

    def set_fecha(self, fecha_str, widget):
        if fecha_str:
            try:
                # Asume que la fecha en la base de datos está en formato 'dd/mm/yyyy'
                day, month, year = map(int, fecha_str.split("/"))
                date_qt = QDate(year, month, day)
            except ValueError:
                # Manejar error de formato de fecha
                date_qt = QDate(2000, 1, 1)  # O alguna otra fecha predeterminada
        else:
            date_qt = QDate(2000, 1, 1)  # O alguna otra fecha predeterminada
        widget.setDate(date_qt)
    
    def mostrarPaciente(self, id):
        try:
            self.ver.showMaximized() #Maximizo la ventana
            insumosList = InsumosWindow()
            data = PacienteCoordinadorData()
            
            archivos = ArchivosPacienteWindow()
            hc = HistoriaClinicaWindow()
            coordinador = data.obtener_coordinador_de_paciente(id)
            if coordinador:
                nombre_completo = f"{coordinador[1]} {coordinador[2]}"
                self.ver.txtCoordinador.setText(nombre_completo)
                self.ver.swCoordinador.setCurrentIndex(0)
            else:
                self.ver.swCoordinador.setCurrentIndex(1)
                try:
                    self.ver.btnAsignar.clicked.disconnect()
                except TypeError:
                    pass
                self.ver.btnAsignar.clicked.connect(lambda: self.cargar_nombres_coordinadores(id))
            
            objData = PacienteData()
            paciente = objData.mostrar(id)

            self.ver.txtNombre.setText(paciente[1])
            self.ver.txtApellido.setText(paciente[2])
            self.ver.txtDomicilio.setText(paciente[3])
            self.ver.txtLocalidad.setText(paciente[4])
            self.ver.txtDocumento.setText(paciente[5])
            self.ver.cbObraSocial.setCurrentText(paciente[7])
            self.ver.txtTelefono.setText(paciente[9])
            self.ver.txtNroAfi.setText(paciente[8])

            self.set_fecha(paciente[6], self.ver.txtFechaN)
            self.set_fecha(paciente[10], self.ver.txtFechaI)
            self.set_fecha(paciente[11], self.ver.txtFechaE)
                
            self.ver.txtMotivo.setText(paciente[12])   
            self.ver.txtFamiliar.setText(paciente[13])
            self.ver.txtParentesco.setText(paciente[14])
            self.ver.txtTelFamiliar.setText(paciente[15])
            self.ver.cbModulo.setCurrentText(paciente[16])

            dic = json.loads(paciente[17])
            
            # Submodulo
            self.ver.fono.setChecked(dic["Fono"])        
            self.ver.to.setChecked(dic['TO'])        
            self.ver.psico.setChecked(dic['Psico'])
            
            dicE = json.loads(paciente[18])
            # Equipamiento
            self.ver.cama.setChecked(dicE['Cama'])
            self.ver.colchon.setChecked(dicE['Colchon'])
            self.ver.silla.setChecked(dicE['Silla'])

            self.ver.cbSN.setCurrentText(paciente[19])
            dicA = json.loads(paciente[20])
            # Asistencia Respiratoria
            self.ver.arA.setChecked(dicA['A'])
            self.ver.arB.setChecked(dicA['B'])
            self.ver.arC.setChecked(dicA['C'])

            try:
                self.ver.btnDescargar.clicked.disconnect()
                self.ver.btnModificar.clicked.disconnect()
                self.ver.btnCarpeta.clicked.disconnect()
                self.ver.btnEliminar.clicked.disconnect()
                self.ver.btnInsumos.clicked.disconnect()
                self.ver.btnProfesionales.clicked.disconnect()  
                self.ver.btnHisClinica.clicked.disconnect()
                
            except TypeError:
                pass

            self.ver.btnModificar.clicked.connect(lambda: self.abrirVentanaModificarP(id=id))
            self.ver.btnInsumos.clicked.connect(lambda: insumosList.mostrarInsumos(id_paciente=id))        
            self.ver.btnProfesionales.clicked.connect(lambda: self.mostrarProfesionales(id_paciente=id))
            self.ver.btnCarpeta.clicked.connect(lambda: archivos.cargarArchivos(id_paciente=id))
            if self.usuario.rol == 'admin':
                self.ver.btnEliminar.clicked.connect(lambda: self.eliminar_paciente(id))
            else:
                self.ver.btnEliminar.setVisible(False)

            self.ver.btnDescargar.clicked.connect(lambda: self.descargar_pdf(id_paciente=id))
            self.ver.btnHisClinica.clicked.connect(lambda: hc.cargarArchivos(id_paciente=id))

            self.ver.show()
        except Exception as e:
            QMessageBox.critical(None, 'Error', f"Error: {e}")

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
        pac_coor = PacienteCoordinadorData()
        eliminado = paciente.eliminar(id_paciente)
        
        if eliminado:
            QMessageBox.information(None, 'Mensaje', 'Paciente eliminado')
            pac_coor.eliminar_relacion(id_paciente)
            
        else:
            QMessageBox.critical(None, 'Error', 'El paciente no pudo ser eliminado')

        self.listado.close()
        self.ver.close()
        self.abrirListado()

    def eliminarRelacionPacienteProfesional(self, id_paciente, id_valor):
        '''Eliminar la relación entre un paciente y un profesional'''

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
            prof = PacienteProfesionalesData()
            success, error_message = prof.eliminar_relacion_paciente_profesional(id_paciente, id_valor)
            if success:
                self.lisProfPac.close()
                QMessageBox.information(None, "Eliminación exitosa", "El profesional ha sido eliminado correctamente.")            
                self.mostrarProfesionales(id_paciente)  # Refrescar la tabla
            else:
                QMessageBox.warning(None, 'Error', f'No se pudo eliminar el profesional: {error_message}')
        else:
            print("Eliminación cancelada")        

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

        if hasattr(self.listado, 'tblListado'):
            if isinstance(self.listado.tblListado, QTableWidget):
                fila = 0
                self.listado.tblListado.setRowCount(len(data)) # Cuantas filas traen los datos
                for item in data:
                    self.listado.tblListado.setItem(fila, 0, QTableWidgetItem(str(item[2]))) # Apellido
                    self.listado.tblListado.setItem(fila, 1, QTableWidgetItem(str(item[1]))) # Nombre
                    self.listado.tblListado.setItem(fila, 2, QTableWidgetItem(str(item[10]))) # Fecha de ingreso
                    
                    if item[11] == '':                
                        self.setRowBackgroundColorP(fila, QColor(170, 255, 127))  # Verde
                    else:
                        self.setRowBackgroundColorP(fila, QColor(255, 88, 66))  # Rojo
                    
                    id_valor = item[0]
                    
                    self.boton_listado_paciente(id_valor, fila)
                    fila += 1

                self.listado.tblListado.setColumnWidth(2, 150)
                self.listado.tblListado.setColumnWidth(4, 150)
                self.listado.tblListado.setColumnWidth(5, 150) 
                try:
                    self.listado.btnBuscar.clicked.disconnect()
                except TypeError:
                    pass
                self.listado.btnBuscar.clicked.connect(lambda: self.buscarPac())
                self.listado.btnLista.setVisible(False)
                self.limpiar_campos_busqueda()
                self.listado.show()
            else:
                print("Error: 'tblListado' no es un QTableWidget.")
        else:
            print("Error: 'listado' no tiene el atributo 'tblListado'.")

    def setRowBackgroundColorP(self, row, color):
        # Verificar si la fila existe en la tabla antes de establecer el color
        if row < self.listado.tblListado.rowCount():
            for col in range(self.listado.tblListado.columnCount()):
                item = self.listado.tblListado.item(row, col)
                if item:
                    item.setBackground(color)

    def buscarPac(self):
        if self.listado.txtApellido.text() == '' and self.listado.txtDocumento.text() == '':
            QMessageBox.information(None, 'Mensaje', 'Ingrese datos a buscar')
            
        else:
            self.listado.tblListado.clearContents()  # Limpiar contenido actual de la tabla
            self.listado.tblListado.setRowCount(0)
            lis = ListadoData() 
            data = lis.buscarPaciente(self.listado.txtDocumento.text(), self.listado.txtApellido.text().upper())
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
        try:
            self.nCoord.btnAsignar.clicked.disconnect()
        except TypeError:
            pass
        self.nCoord.btnAsignar.clicked.connect(lambda: self.asociarCoordinadorAPaciente(id_paciente, id_profesional))
        self.nCoord.show()
    
    def actualizar_id_profesional_coordinador(self, index, id_paciente):
        id_profesional = None
        if index >= 0:
            item_data = self.nCoord.cbProfesionales.itemData(index)
            if item_data is not None:
                id_profesional = item_data
                print(f"ID del profesional seleccionado: {id_profesional}")
                print('actualizar', id_profesional)
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
                print('Profesional ', id_profesional, ' paciente ', id_paciente)
                exito, error_message = objData.asociar_coordinador_a_paciente(id_paciente, id_profesional)
                
                if exito:
                    QMessageBox.information(None, 'Mensaje', 'Coordinador asociado al paciente correctamente') 
                else:
                    QMessageBox.critical(None, 'Error', f'El coordinador no pudo ser asociado: {error_message}')
                    
                self.nCoord.close() #Cierro la ventana
                self.ver.close()
                self.mostrarPaciente(id_paciente)
                self.ver.show()
        except UnboundLocalError as ex:
            QMessageBox.critical(None, 'Error', f'variable local: {ex}')
        except Exception as e:
            QMessageBox.critical(None, 'Error', f'Seleccione un coordinador: {e}')

### Paciente - Profesionales ###

    def boton_listado_profesionales_pac (self, id_paciente, id_valor, fila):              
        # Crear el botón y añadirlo a la columna 4
        # Crear el botón "Eliminar" y conectarlo
        btn = QPushButton("Eliminar")
        
        btn.clicked.connect(lambda _, id_valor=id_valor: self.eliminarRelacionPacienteProfesional(id_paciente, id_valor))
        # Agregar estilo al botón
        btn.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(btn)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lisProfPac.tblListadoPP.setCellWidget(fila, 3, widget)

    def mostrarProfesionales(self, id_paciente):
        profesional = ProfesionalWindow(self.usuario)

        lis = PacienteProfesionalesData()
        profesionales = lis.obtener_profesionales_de_paciente(id_paciente)        
        
        # Limpiar la tabla antes de añadir nuevas filas
        self.lisProfPac.tblListadoPP.clearContents()
        self.lisProfPac.tblListadoPP.setRowCount(0)

        if profesionales:
            self.lisProfPac.tblListadoPP.setRowCount(len(profesionales))  # Configurar el número de filas
            self.lisProfPac.tblListadoPP.setColumnCount(4)

            new_headers = ["Apellido", "Nombre", "Profesión", "Acciones"]
            self.lisProfPac.tblListadoPP.setHorizontalHeaderLabels(new_headers)
                
            fila = 0
            for item in profesionales:
                    
                self.lisProfPac.tblListadoPP.setItem(fila, 0, QTableWidgetItem(str(item[2]))) #Apellido
                self.lisProfPac.tblListadoPP.setItem(fila, 1, QTableWidgetItem(str(item[1]))) #Nombre
                self.lisProfPac.tblListadoPP.setItem(fila, 2, QTableWidgetItem(str(item[16]))) #Profesión

                id_valor = item[0]
                    
                self.boton_listado_profesionales_pac(id_paciente, id_valor, fila)

                fila += 1
            
        self.lisProfPac.btnProf.clicked.connect(lambda: profesional.cargar_nombres_profesionales(id_paciente))
        self.lisProfPac.btnRefrescar.clicked.connect(lambda: self.mostrarProfesionales(id_paciente))
        try:
            self.lisProfPac.btnDescargar.clicked.disconnect()
        except TypeError:
            pass
        self.lisProfPac.btnDescargar.clicked.connect(lambda: self.descargar_pdf_prof_pac(id_paciente))
        self.lisProfPac.show()

##### Pacientes de Profesional #####
    def cargar_pacientes(self, id_profesional):
        self.id_profesional_seleccionado = id_profesional
        objData = PacienteData()
        pacientes = objData.obtener_pacientes()
        self.asocPac.cbPacientes.clear()  # Limpiar ComboBox antes de agregar nuevos items

        if pacientes:
            self.asocPac.cbPacientes.addItem('--Seleccione--')
            for id_paciente, nombre, apellido in pacientes:
                item = f"{nombre} {apellido}"
                self.asocPac.cbPacientes.addItem(item, userData=id_paciente)
        else:
            self.asocPac.cbPacientes.addItem("No hay pacientes cargados")

        # Conectar señal para actualizar ID del paciente seleccionado
        self.asocPac.cbPacientes.currentIndexChanged.connect(lambda index: self.actualizar_id_paciente(index))

        # Conectar botón Registrar usando el ID del paciente seleccionado dinámicamente
        self.asocPac.btnRegistrar.clicked.connect(self.asociarPacienteAProfesional)
        self.asocPac.show()

    def actualizar_id_paciente(self, index):
        if index > 0:  # Asegúrate de que no sea la primera opción '--Seleccione--'
            item_data = self.asocPac.cbPacientes.itemData(index)
            if item_data is not None:
                self.id_paciente_seleccionado = item_data  # Almacenar el ID del paciente seleccionado
                print(f"ID del paciente seleccionado: {self.id_paciente_seleccionado}")
            else:
                print("No se encontró el ID del paciente seleccionado.")
        else:
            self.id_paciente_seleccionado = None  # Resetear si se selecciona la opción '--Seleccione--'
            print("No se seleccionó ningún paciente válido.")

    def asociarPacienteAProfesional(self):
        if hasattr(self, 'id_profesional_seleccionado') and self.id_paciente_seleccionado:            
            id_profesional = self.id_profesional_seleccionado
            id_paciente = self.id_paciente_seleccionado
            try:
                objData = PacienteProfesionalesData()
                
                # # Verificar si la asociación ya existe
                # if objData.existe_asociacion(id_paciente, id_profesional):
                #     QMessageBox.warning(None, 'Error', 'El paciente ya está asociado a este profesional')
                #     return
                
                exito = objData.asociar_profesional_a_paciente(id_paciente, id_profesional)

                if exito:
                    QMessageBox.information(None, 'Mensaje', 'Paciente asociado al profesional correctamente')
                else:
                    QMessageBox.warning(None, 'Error', 'No se pudo asociar el paciente al profesional')
                    print(id_paciente, id_profesional)

                self.asocPac.close()  # Cerrar la ventana
            except Exception as e:
                QMessageBox.critical(None, 'Error', 'Error al asociar paciente con profesional')
                print(f"Error: {e}")
        else:
            QMessageBox.warning(None, 'Error', 'No se ha seleccionado un paciente o profesional')

############## PDF Paciente #################

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
                'localidad': data[4],
                'telefono': data[9],
                'obra_social': data[7],
                'numero_afiliado': data[8],
                'familiar_a_cargo': data[13],
                'parentesco': data[14],
                'telefono_familiar': data[15],
                'fecha_ingreso': data[10],
                'fecha_egreso': data[11],
                'motivo': data[12],
                'modulo': data[16],
                'soporte_nutricional': data[19],
                'submodulo': data[17],
                'equipamiento': data[18],
                'asistencia_respiratoria': data[20]
                
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

    def generar_pdf_paciente(self, paciente_data, filePath):
        try:
            c = canvas.Canvas(filePath, pagesize=A4)
            width, height = A4
            margin = 2 * cm
            line_height = 0.5 * cm
            box_margin = 0.2 * cm

             # Ajustar el título
            c.setFont("Helvetica-Bold", 14)
            title_x = margin
            title_y = height - margin
            title_text = "Ficha de Paciente"
            title_width = c.stringWidth(title_text, "Helvetica-Bold", 14)
            c.drawString((width - title_width) / 2, title_y, title_text)  # Centrar el título
            
            # Ajustar el espacio después del título
            current_y = title_y - line_height * 2
            
            # Ajustar los campos
            c.setFont("Helvetica", 10)
            col_width = (width - 2 * margin) / 2  # Dividir el ancho de la página en 2 columnas
            box_height = 2 * line_height  # Altura de cada recuadro

            fields = [
                ('Nombre', paciente_data.get('nombre', '')),
                ('Apellido', paciente_data.get('apellido', '')),
                ('Número de Documento', paciente_data.get('dni', '')),
                ('Fecha de Nacimiento', paciente_data.get('fecha_nacimiento', '')),
                ('Domicilio', paciente_data.get('direccion', '')),
                ('Localidad', paciente_data.get('localidad', '')),
                ('Teléfono', paciente_data.get('telefono', '')),
                ('Obra Social', paciente_data.get('obra_social', '')),
                ('Número de Afiliado', paciente_data.get('numero_afiliado', '')),
                ('Familiar a Cargo', paciente_data.get('familiar_a_cargo', '')),
                ('Parentesco', paciente_data.get('parentesco', '')),
                ('Teléfono familiar', paciente_data.get('telefono_familiar', '')),
                ('Fecha de Ingreso', paciente_data.get('fecha_ingreso', '')),
                ('Fecha de Egreso', paciente_data.get('fecha_egreso', '')),
                ('Motivo', paciente_data.get('motivo', '')),
                ('Coordinador', paciente_data.get('coordinador', ''))
            ]
            
            for i, (field, value) in enumerate(fields):
                col = i % 2
                row = i // 2
                
                # Calcular posiciones para el campo
                x = margin + col * col_width
                y = current_y - row * box_height
                
                # Dibujar el recuadro para el título
                title_box_x = x
                title_box_y = y - box_height + line_height
                c.rect(title_box_x, title_box_y, col_width / 2, box_height)
                
                # Dibujar el recuadro para el valor
                value_box_x = x + col_width / 2
                value_box_y = y - box_height + line_height
                c.rect(value_box_x, value_box_y, col_width / 2, box_height)
                
                # Dibujar campo y valor dentro del recuadro
                title_text_x = title_box_x + box_margin
                title_text_y = title_box_y + box_height - line_height - box_margin
                value_text_x = value_box_x + box_margin
                value_text_y = value_box_y + box_height - line_height - box_margin
                
                c.drawString(title_text_x, title_text_y, f"{field}:")
                c.drawString(value_text_x, value_text_y, value)
            
            # Agregar sección de Resolución
            # current_y = current_y - (len(fields) // 2) * box_height - box_height
            # c.setFont("Helvetica-Bold", 12)
            # c.drawString(margin, current_y, "Resolución")
            # c.line(margin, current_y - 0.2 * cm, width - margin, current_y - 0.2 * cm)
            subtitle_text = "Resolución"
            text_width = c.stringWidth(subtitle_text, "Helvetica-Bold", 12)

            # Calcular la posición x para centrar el texto
            text_x = (width - text_width) / 2

            # Ajustar la posición vertical
            current_y = current_y - (len(fields) // 2) * box_height - box_height
            c.setFont("Helvetica-Bold", 12)

            # Dibujar el subtítulo centrado
            c.drawString(text_x, current_y, subtitle_text)

            # Dibujar la línea debajo del subtítulo
            c.line(margin, current_y - 0.2 * cm, width - margin, current_y - 0.2 * cm)
            
            # Sub-secciones (solo los datos cargados)
            current_y = current_y - line_height * 1.5
            c.setFont("Helvetica", 10)
            
            # Procesar diccionarios para submodulo, asistencia respiratoria y equipamiento
            def procesar_diccionario(diccionario_str):
                diccionario = json.loads(diccionario_str)
                return ', '.join([key for key, value in diccionario.items() if value])
            
            submodulo = procesar_diccionario(paciente_data.get('submodulo', '{}'))
            asistencia_respiratoria = procesar_diccionario(paciente_data.get('asistencia_respiratoria', '{}'))
            equipamiento = procesar_diccionario(paciente_data.get('equipamiento', '{}'))
            
            sections = [
                ('Módulo', paciente_data.get('modulo', '')),
                ('Soporte Nutricional', paciente_data.get('soporte_nutricional', '')),
                ('SubMódulo', submodulo),
                ('Equipamiento', equipamiento),
                ('Asistencia Respiratoria', asistencia_respiratoria)
            ]
            
            for i, (label, value) in enumerate(sections):
                col = i % 2
                row = i // 2
                
                x = margin + col * col_width
                y = current_y - row * box_height
                
                # Dibujar el recuadro para el título
                title_box_x = x
                title_box_y = y - box_height + line_height
                c.rect(title_box_x, title_box_y, col_width / 2, box_height)
                
                # Dibujar el recuadro para el valor
                value_box_x = x + col_width / 2
                value_box_y = y - box_height + line_height
                c.rect(value_box_x, value_box_y, col_width / 2, box_height)
                
                # Dibujar campo y valor dentro del recuadro
                title_text_x = title_box_x + box_margin
                title_text_y = title_box_y + box_height - line_height - box_margin
                value_text_x = value_box_x + box_margin
                value_text_y = value_box_y + box_height - line_height - box_margin
                
                c.drawString(title_text_x, title_text_y, f"{label}:")
                c.drawString(value_text_x, value_text_y, value)
            
            # Finalizar el PDF
            c.save()
            return True
        except Exception as e:
            print(f"Error al generar el PDF: {str(e)}")
            return False

######### PDF Profesionales de Paciente #######

    def descargar_pdf_prof_pac(self, id_paciente):
        try:
            # Obtener la información del profesional
            paciente = PacienteData()
            paciente_info = paciente.mostrar(id_paciente)

            prof = PacienteProfesionalesData()
            data = prof.obtener_profesionales_de_paciente(id_paciente)
            print(data)

            profesionales_data_list = []
            for item in data:
                profesional_data = {
                    'nombre': item[1],
                    'apellido': item[2],                
                    'profesion': item[16],          
                }
                profesionales_data_list.append(profesional_data)
            
            # Mostrar el cuadro de diálogo para guardar el archivo PDF
            filePath, _ = QFileDialog.getSaveFileName(self.ver, "Guardar PDF", f"Profesionales_de_{paciente_info[1]}_{paciente_info[2]}.pdf", "PDF Files (*.pdf)")
            
            if filePath:
                # Generar el PDF
                if self.generar_pdf_profesional(profesionales_data_list, filePath):
                    QMessageBox.information(None, "Éxito", "El PDF se guardó correctamente.")
                else:
                    QMessageBox.warning(None, "Error", "No se pudo guardar el PDF.")
            else:
                QMessageBox.warning(None, "Advertencia", "No se seleccionó ningún archivo para guardar.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Ocurrió un error: {str(e)}")

    def generar_pdf_profesional(self, profesionales_data_list, filePath):
        try:
            print('profesionales', profesionales_data_list)
            c = canvas.Canvas(filePath, pagesize=A4)
            width, height = A4
            margin = 1 * cm
            line_height = 0.5 * cm
            box_margin = 0.2 * cm
            
            # Ajustar el título
            c.setFont("Helvetica-Bold", 14)
            title_x = margin
            title_y = height - margin
            title_text = "Profesionales de paciente"
            title_width = c.stringWidth(title_text, "Helvetica-Bold", 14)
            c.drawString((width - title_width) / 2, title_y, title_text)  # Centrar el título
            
            # Ajustar el espacio después del título
            current_y = height - margin - line_height * 4
            
            # Ajustar los campos
            c.setFont("Helvetica", 10)
            num_cols = 3
            col_width = (width - 2 * margin) / num_cols  # Dividir el ancho de la página en 3 columnas
            box_height = 2 * line_height  # Altura de cada recuadro
            
            # Dibujar las cabeceras de las columnas
            headers = ['Nombre', 'Apellido', 'Profesión']
            for i, header in enumerate(headers):
                x = margin + i * col_width
                y = current_y
                c.rect(x, y, col_width, box_height)  # Dibujar el recuadro
                c.drawString(x + box_margin, y + box_height - line_height - box_margin, header)  # Dibujar el texto del encabezado
            
            # Ajustar la posición para los datos
            current_y -= box_height  # Mover hacia abajo para empezar a dibujar datos
            
            # Iterar sobre la lista de profesionales
            for index, profesional_data in enumerate(profesionales_data_list):
                col = 0  # Empezar en la primera columna
                row = index  # Fila en la que se encuentra el recuadro
                
                for key in headers:
                    # Convertir el encabezado a minúsculas para coincidir con las claves del diccionario
                    key = key.lower().replace('ó', 'o')
                    print(key)
                    value = profesional_data.get(key, '')
                    
                    # Calcular la posición para el dato
                    x = margin + col * col_width
                    y = current_y - row * box_height
                    
                    # Mostrar información de depuración
                    print(f"Index: {index}, Col: {col}, Row: {row}, X: {x}, Y: {y}, Value: {value}")
                    
                    # Dibujar el recuadro para el dato
                    c.rect(x, y, col_width, box_height)
                    
                    # Dibujar el dato dentro del recuadro
                    c.drawString(x + box_margin, y + box_height - line_height - box_margin, value)
                    
                    col += 1  # Mover a la siguiente columna
                    
                # Ajustar la posición para la próxima fila
                if (index + 1) % num_cols == 0:
                    current_y -= box_height

            # Finalizar el PDF
            c.save()
            return True
        except Exception as e:
            print(f"Error al generar el PDF: {str(e)}")
            return False