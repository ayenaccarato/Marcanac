import os

from functools import partial
from datetime import datetime
from time import strftime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from PyQt6 import uic, QtCore
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QPushButton, QWidget, QHBoxLayout, QTableWidgetItem, QStyledItemDelegate
from data.listados import ListadoData
from data.paciente import PacienteData
from data.paciente_profesionales import PacienteProfesionalesData
from data.pago_profesional import PagoProfesionalData
from data.profesional import ProfesionalData
from gui.profesionales.archivos_profesional import ArchivosProfesionalWindow

from model.pago import PagoProfesional
from model.profesional import Profesional
from model.usuario import Usuario

class ProfesionalWindow():

    def __init__(self, user: Usuario):
        ProfesionalData()
        self.usuario = user
        #self.prof = uic.loadUi("gui/profesionales/nuevo_profesional.ui")
        ui_file_prof = os.path.join(os.path.dirname(__file__), '..', 'profesionales' ,'nuevo_profesional.ui')
        ui_file_prof = os.path.abspath(ui_file_prof)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file_prof):
            print(f"Error: el archivo {ui_file_prof} no se encuentra.")
            return
        self.prof = uic.loadUi(ui_file_prof)
        
        #self.listadoProf = uic.loadUi("gui/profesionales/listado_profesionales.ui")
        ui_file_lis = os.path.join(os.path.dirname(__file__), '..', 'profesionales' ,'listado_profesionales.ui')
        ui_file_lis = os.path.abspath(ui_file_lis)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file_lis):
            print(f"Error: el archivo {ui_file_lis} no se encuentra.")
            return
        self.listadoProf = uic.loadUi(ui_file_lis)

        #self.verProf = uic.loadUi("gui/profesionales/ver_profesional.ui")
        ui_file_ver = os.path.join(os.path.dirname(__file__), '..', 'profesionales' ,'ver_profesional.ui')
        ui_file_ver = os.path.abspath(ui_file_ver)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file_ver):
            print(f"Error: el archivo {ui_file_ver} no se encuentra.")
            return
        self.verProf = uic.loadUi(ui_file_ver)

        #self.actProf = uic.loadUi("gui/profesionales/modificar_profesional.ui")
        ui_file_act = os.path.join(os.path.dirname(__file__), '..', 'profesionales' ,'modificar_profesional.ui')
        ui_file_act = os.path.abspath(ui_file_act)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file_act):
            print(f"Error: el archivo {ui_file_act} no se encuentra.")
            return
        self.actProf = uic.loadUi(ui_file_act)

        #self.asocProf = uic.loadUi("gui/pacientes/asociar_profesional.ui")
        ui_file_a= os.path.join(os.path.dirname(__file__), '..', 'pacientes' ,'asociar_profesional.ui')
        ui_file_a = os.path.abspath(ui_file_a)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file_a):
            print(f"Error: el archivo {ui_file_a} no se encuentra.")
            return
        self.asocProf = uic.loadUi(ui_file_a)

        ui_file_pago= os.path.join(os.path.dirname(__file__), '..', 'profesionales' ,'listado_profesionales_pago.ui')
        ui_file_pago = os.path.abspath(ui_file_pago)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file_pago):
            print(f"Error: el archivo {ui_file_pago} no se encuentra.")
            return
        self.lisPago = uic.loadUi(ui_file_pago)

        ui_file_pac = os.path.join(os.path.dirname(__file__), '..', 'profesionales' ,'listado_pacientes_profesional.ui')
        ui_file_pac = os.path.abspath(ui_file_pac)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file_pac):
            print(f"Error: el archivo {ui_file_pac} no se encuentra.")
            return
        self.lisPacientes = uic.loadUi(ui_file_pac)

        # self.lisPacientes.tblListado.cellChanged.connect(lambda: self.handleCellChanged)

    def abrirRegistroProf(self):   
        self.prof.btnRegistrar.clicked.connect(self.registrarProfesional)     
        self.prof.show()

    def is_valid_email(self, email):
        """Verifica si el correo electrónico tiene un formato válido."""
        import re
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email) is not None

    def registrarProfesional(self):
        if self.prof.cbProfesional.currentText() == "--Seleccione--":    
            QMessageBox.information(None, 'Mensaje', 'Seleccione una profesión')       
        # Validar el correo electrónico (opcional, pero recomendado)
        email = self.prof.txtMail.text()
        if not self.is_valid_email(email):
            QMessageBox.critical(None, 'Error', "El correo electrónico ingresado no es válido. Debe ser del estilo: ejemplo@ejemplo.com")
        else:
            fechaN = self.prof.txtFechaN.date().toPyDate().strftime("%d/%m/%Y") #formateo la fecha
                        
            nuevoProfesional = Profesional(
                nombre = self.prof.txtNombre.text().capitalize(), #Pongo primer letra en mayuscula
                apellido = self.prof.txtApellido.text().capitalize(),
                domicilio = self.prof.txtDomicilio.text().capitalize(),
                localidad = self.prof.txtLocalidad.text().capitalize(),
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
                nombre2 = self.prof.txtNombre_2.text().capitalize(),
                apellido2 = self.prof.txtApellido_2.text().capitalize(),
                CUIT2 = self.prof.txtCuit_2.text(),
                cbu3 = self.prof.txtCbu3.text()         
            )

            objData = ProfesionalData()
            
            success, error_message = objData.registrar(profesional=nuevoProfesional)
            if success:   
                QMessageBox.information(None, 'Mensaje', 'Profesional registrado') 
                self.limpiarCamposProfesional()         
            else:
                QMessageBox.critical(None, 'Error', f'El profesional no pudo ser registrado: {error_message}')

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
    
    # def boton_pagar(self, id_valor, fila):
        
    #     btn_pagar = QPushButton("Pagar")
        
    #     btn_pagar.clicked.connect(lambda _, id_valor=id_valor: self.agregarPago(id_valor))
    #     # Agregar estilo al botón
    #     btn_pagar.setStyleSheet("background-color: rgb(85, 170, 255); color: rgb(255, 255, 255);")
    #     widget = QWidget()
    #     layout = QHBoxLayout(widget)
    #     layout.addWidget(btn_pagar)
    #     layout.setContentsMargins(0, 0, 0, 0)
    #     layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    #     self.listadoProf.tblListadoProf.setCellWidget(fila, 8, widget)
    
    # def obtener_ultimo_mes(self, pagos):
    #     # Suponemos que la fecha está en la segunda posición de cada tupla
    #     fechas = [datetime.strptime(pago[2], "%d/%m/%Y") for pago in pagos]
    #     fecha_mas_actual = max(fechas)  # Obtiene la fecha más reciente
    #     return fecha_mas_actual.strftime("%m")
    
    def abrirListadoProfesionales(self): 
        self.listadoProf.showMaximized() #Maximizo la ventana

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

            self.listadoProf.tblListadoProf.hideColumn(8) #PAgo

            id_valor = item[0]
            
            self.boton_listado_profesional(id_valor, fila)

            # if self.usuario.rol == 'admin':
            #     mes_actual = '0' + str(datetime.now().month) 

            #     pago_profesional = PagoProfesionalData()
            #     pagos_existentes = pago_profesional.obtener_pagos()
                
            #     pago_realizado = any(id_valor == tup[1] for tup in pagos_existentes)
                
            #     if not pago_realizado:
            #         self.listadoProf.tblListadoProf.showColumn(8)
            #         self.boton_pagar(id_valor, fila)
            #     else:
            #         if mes_actual == pago_profesional.obtener_fecha_pago_profesional(id_valor)[0]:
            #             self.listadoProf.tblListadoProf.setItem(fila, 8, QTableWidgetItem('Pago'))
            #             self.listadoProf.tblListadoProf.setCellWidget(fila, 8, None)
            # else:
            #     self.listadoProf.tblListadoProf.hideColumn(8)

            fila += 1
 
        self.listadoProf.tblListadoProf.setColumnWidth(2,150)
        self.listadoProf.tblListadoProf.setColumnWidth(3,150)
        try:
            self.listadoProf.btnBuscar.clicked.disconnect()
        except TypeError:
            pass
        self.listadoProf.btnBuscar.clicked.connect(lambda: self.buscar('prof'))
        self.listadoProf.btnLista.setVisible(False)
        if self.usuario.rol == 'admin':
            self.listadoProf.btnPago.setVisible(True)
            self.listadoProf.btnPago.clicked.connect(lambda: self.listado_pagos())
        else:
            self.listadoProf.btnPago.setVisible(False)
        self.limpiar_campos_busqueda()   
        self.listadoProf.show()

    # def agregarPago(self, id_profesional):
        
    #     fecha = datetime.now().strftime("%d/%m/%Y")

    #     nuevo_pago = PagoProfesional(
    #         profesional_id = id_profesional,
    #         fecha_pago = fecha
    #     )

    #     pago = PagoProfesionalData()

    #     success, error_message = pago.registrar_pago(nuevo_pago)
    #     if success:   
    #         QMessageBox.information(None, 'Mensaje', 'Pago registrado')     
    #         self.abrirListadoProfesionales() 
    #     else:
    #         QMessageBox.critical(None, 'Error', f'El pago no pudo ser registrado: {error_message}')

    # def listado_pagos(self):
        # self.lisPago.showMaximized() #Maximizo la ventana

        # lis = PagoProfesionalData()
        # data = lis.obtener_pagos()   
        # fila = 0
        # self.lisPago.tblListado.setRowCount(len(data)) #Cuantas filas traen los datos

        # for item in data:
        #     #Obtengo el profesional
        #     profesional = ProfesionalData().mostrar(item[0])

        #     self.lisPago.tblListado.setItem(fila, 0, QTableWidgetItem(str(item[2]))) #Fecha de pago
        #     self.lisPago.tblListado.setItem(fila, 1, QTableWidgetItem(str(profesional[2]))) #Apellido
        #     self.lisPago.tblListado.setItem(fila, 2, QTableWidgetItem(str(profesional[1]))) #Nombre
        #     self.lisPago.tblListado.setItem(fila, 3, QTableWidgetItem(str(profesional[18]))) #Codigo
        #     self.lisPago.tblListado.setItem(fila, 4, QTableWidgetItem(str(profesional[16]))) #Profesion

        #     fila += 1
 
        # self.lisPago.tblListado.setColumnWidth(1,150)
        # self.lisPago.tblListado.setColumnWidth(2,150)
        # self.lisPago.tblListado.setColumnWidth(4,150)
        # try:
        #     self.lisPago.btnBuscar.clicked.disconnect()
        # except TypeError:
        #     pass

        # self.lisPago.btnBuscar.clicked.connect(lambda: self.buscar('pagos'))
        # self.lisPago.btnLista.setVisible(False)

        # #self.limpiar_campos_busqueda()   
        # self.lisPago.show()
    
    def setRowBackgroundColor(self, row, color):
        # Verificar si la fila existe en la tabla antes de establecer el color
        if row < self.listado.tblListado.rowCount():
            for col in range(self.listado.tblListado.columnCount()):
                item = self.listado.tblListado.item(row, col)
                if item:
                    item.setBackground(color)

    def buscar(self, tipo):
        if tipo == 'prof':
            self.listadoProf.tblListadoProf.clearContents()  # Limpiar contenido actual de la tabla
            self.listadoProf.tblListadoProf.setRowCount(0)
            lis = ListadoData() 
            data = lis.buscarProfesional(self.listadoProf.txtCuit.text(), self.listadoProf.txtApellido.text().upper(), self.listadoProf.cbProfesion.currentText())
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
        else:
            self.lisPago.tblListado.clearContents()  # Limpiar contenido actual de la tabla
            self.lisPago.tblListado.setRowCount(0)

            lis = PagoProfesionalData() 
            data = lis.obtener_pagos_profesional(self.lisPago.cbMes.currentText())

            if data:
                # Reiniciar número de filas
                fila = 0
                self.lisPago.tblListado.setRowCount(len(data)) #Cuantas filas traen los datos
                for item in data:
                    profesional = ProfesionalData().mostrar(item[0])

                    self.lisPago.tblListado.setItem(fila, 0, QTableWidgetItem(str(item[2]))) #Fecha de pago
                    self.lisPago.tblListado.setItem(fila, 1, QTableWidgetItem(str(profesional[2]))) #Apellido
                    self.lisPago.tblListado.setItem(fila, 2, QTableWidgetItem(str(profesional[1]))) #Nombre
                    self.lisPago.tblListado.setItem(fila, 3, QTableWidgetItem(str(profesional[18]))) #Codigo
                    self.lisPago.tblListado.setItem(fila, 4, QTableWidgetItem(str(profesional[16]))) #Profesion

                    fila += 1
                
            else:
                # Limpiar la tabla si no se encontraron resultados
                self.lisPago.tblListado.clearContents()
                self.lisPago.tblListado.setRowCount(0)

            self.lisPago.btnLista.setVisible(True)
            self.lisPago.btnLista.clicked.connect(lambda: self.listado_pagos())

    def limpiar_campos_busqueda(self):        
        self.listadoProf.txtCuit.clear()  # Limpia el contenido del primer QLineEdit
        self.listadoProf.txtApellido.clear()
        self.listadoProf.cbProfesion.setCurrentIndex(0)

    def handleCellChanged(self, item, id_profesional):
        self.pp = PacienteProfesionalesData()
        if item is not None:
            row = item.row()
            column = item.column()
            id_paciente = self.lisPacientes.tblListado.item(row, 0).text()  # ID del paciente
            new_value = item.text()  # Nuevo valor de la celda

            # Convertir el nuevo valor a número si es necesario
            try:
                if column == 4:
                    new_value = float(new_value)
            except ValueError:
                # Si no es posible convertir a float, se ignora el cambio
                return

            # Solo actualiza si la columna es una de las permitidas
            if column in [3, 4]:  # Columnas editables: visitas (3) y valor (4)
                # Obtener los valores actuales de visitas y valor
                visitas_item = self.lisPacientes.tblListado.item(row, 3)
                valor_item = self.lisPacientes.tblListado.item(row, 4)
                total_item = self.lisPacientes.tblListado.item(row, 5)

                visitas = float(visitas_item.text()) if visitas_item is not None else 0
                valor = float(valor_item.text()) if valor_item is not None else 0

                # Calcular el nuevo total
                total = visitas * valor

                # Actualizar la celda del total
                if total_item is not None:
                    total_item.setText(str(total))
                else:
                    self.lisPacientes.tblListado.setItem(row, 5, QTableWidgetItem(str(total)))

                # Actualizar en la base de datos
                success, error_message = self.pp.actualizar_dato(id_paciente=id_paciente, columna=column, nuevo_valor=new_value, id_profesional=id_profesional)
                if not success:
                    QMessageBox.critical(None, 'Error', f"No se pudo actualizar el dato: {error_message}")
                else:
                    QMessageBox.information(None, 'Mensaje', f"Paciente ID: {id_paciente}, Columna: {column}, Nuevo valor: {new_value}")
        # if item is not None:
        #     row = item.row()
        #     column = item.column()
        #     print('handle')
        #     id_paciente = self.lisPacientes.tblListado.item(row, 0).text()
        #     print('id pac ', id_paciente)
        #     new_value = item.text()
        #     print('nuevo valor', new_value)

        #     exito, error_message = self.pp.actualizar_dato(id_paciente=id_paciente, id_profesional=id_profesional, columna=column, nuevo_valor=new_value)
        #     if exito:
        #         print('si')
        #         QMessageBox.information(None, 'Mensaje', f"Paciente ID: {id_paciente}, Columna: {column}, Nuevo valor: {new_value}")
        #     else:
        #         print('no')
        #         QMessageBox.critical(None, 'Error', f"Ocurrio un error: {error_message}")

    def listado_pacientes(self, id_profesional):
        from gui.pacientes.paciente import PacienteWindow
        pacientes = PacienteProfesionalesData()
        data = pacientes.obtener_pacientes_de_profesional(id_profesional)
        print('data ', data)

        fila = 0
        self.lisPacientes.tblListado.setRowCount(len(data)) #Cuantas filas traen los datos
        for item in data:
            paciente = PacienteData().mostrar(item[0])          

            self.lisPacientes.tblListado.setItem(fila, 0, QTableWidgetItem(str(item[0]))) #ID
            self.lisPacientes.tblListado.hideColumn(0)
            self.lisPacientes.tblListado.setItem(fila, 1, QTableWidgetItem(str(paciente[2]))) #Apellido
            self.lisPacientes.tblListado.setItem(fila, 2, QTableWidgetItem(str(paciente[1]))) #Nombre
            if item[3] == None:
                self.lisPacientes.tblListado.setItem(fila, 3, QTableWidgetItem(str(0))) #Cantidad de visitas
            else:
                self.lisPacientes.tblListado.setItem(fila, 3, QTableWidgetItem(str(item[3]))) #Cantidad de visitas
            if item[4] == None:
                self.lisPacientes.tblListado.setItem(fila, 4, QTableWidgetItem(str(0))) #Valor de visita
            else:
                self.lisPacientes.tblListado.setItem(fila, 4, QTableWidgetItem(str(item[4]))) #Valor de visita
            if item[5] == None:
                self.lisPacientes.tblListado.setItem(fila, 5, QTableWidgetItem(str(0))) #Total
            else:
                self.lisPacientes.tblListado.setItem(fila, 5, QTableWidgetItem(str(item[5]))) #Total

            fila += 1

        # Conectar el evento cellChanged al método handleCellChanged
        self.lisPacientes.tblListado.itemChanged.connect(lambda item: self.handleCellChanged(item, id_profesional))
        #self.lisPacientes.tblListado.itemChanged.connect(self.handleCellChanged)

        # # Desconectar cualquier conexión existente
        # self.lisPacientes.tblListado.cellChanged.disconnect(self.handleCellChanged)

        self.lisPacientes.tblListado.setColumnWidth(1,150)
        self.lisPacientes.tblListado.setColumnWidth(2,150)
        self.lisPacientes.tblListado.setColumnWidth(3,150)

        self.paciente_window = PacienteWindow(self.usuario)
        self.lisPacientes.btnAgregar.clicked.connect(lambda: self.paciente_window.cargar_pacientes(id_profesional=id_profesional))
        self.lisPacientes.btnRefrescar.clicked.connect(lambda: self.listado_pacientes(id_profesional))
        self.lisPacientes.btnDescargar.clicked.connect(lambda: self.descargar_pdf_pacientes(id_profesional))

        self.lisPacientes.show()

##### Ver #####

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

    def mostrarProfesional(self, id):
        try:
            archivos = ArchivosProfesionalWindow()
            objData = ProfesionalData()
            profesional = objData.mostrar(id)

            self.verProf.txtNombre.setText(profesional[1])
            self.verProf.txtApellido.setText(profesional[2])
            self.verProf.txtDomicilio.setText(profesional[3])
            self.verProf.txtLocalidad.setText(profesional[4])
            self.verProf.txtCuit.setText(profesional[5])

            self.set_fecha(profesional[6], self.verProf.txtFechaN)
            
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
            self.verProf.cuidador.setChecked(profesional[17] == 'True')
            self.verProf.txtCodigo.setText(profesional[18])
            
            # Datos pago a terceros
            self.verProf.txtNombre_2.setText(profesional[19])
            self.verProf.txtApellido_2.setText(profesional[20])
            self.verProf.txtCuit_2.setText(profesional[21])
            self.verProf.txtCbu3.setText(profesional[22])

            try:
                self.verProf.btnDescargar.clicked.disconnect()
                self.verProf.btnModificar.clicked.disconnect()
                self.verProf.btnCarpeta.clicked.disconnect()
                self.verProf.btnEliminar.clicked.disconnect()
            except TypeError:
                pass

            self.verProf.btnModificar.clicked.connect(lambda: self.abrirVentanaModificar(id))
            self.verProf.btnCarpeta.clicked.connect(lambda: archivos.cargarArchivosProfesional(id_profesional=id))
            if self.usuario.rol == 'admin':
                self.verProf.btnEliminar.clicked.connect(lambda: self.eliminar_profesional(id))
            else:
                self.verProf.btnEliminar.setVisible(False)

            self.verProf.btnDescargar.clicked.connect(lambda: self.descargar_pdf(id_profesional=id))
            self.verProf.btnPacientes.clicked.connect(lambda: self.listado_pacientes(id_profesional=id))

            self.verProf.show()
        except Exception as e:
            QMessageBox.critical(None, 'Error', f"Error: {e}")

    def abrirVentanaModificar(self, id):
        self.verProf.close()
        self.actualizarProfesional(id)
        self.actProf.show()

    def actualizarProfesional(self, id):
        try:
            objData = ProfesionalData()
            profesional = objData.mostrar(id)

            self.actProf.txtNombre.setText(profesional[1])
            self.actProf.txtApellido.setText(profesional[2])
            self.actProf.txtDomicilio.setText(profesional[3])
            self.actProf.txtLocalidad.setText(profesional[4])
            self.actProf.txtCuit.setText(profesional[5])

            self.set_fecha(profesional[6], self.actProf.txtFechaN)
            
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
            self.actProf.cuidador.setChecked(profesional[17] == 'True')
            self.actProf.txtCodigo.setText(profesional[18])
            
            # Datos pago a terceros
            self.actProf.txtNombre_2.setText(profesional[19])
            self.actProf.txtApellido_2.setText(profesional[20])
            self.actProf.txtCuit_2.setText(profesional[21])
            self.actProf.txtCbu3.setText(profesional[22])

            try:
                self.actProf.btnGuardar.clicked.disconnect()
            except TypeError:
                pass
            # Conectar el botón btnGuardar a guardarCambiosProfesional
            self.actProf.btnGuardar.clicked.connect(lambda: self.guardarCambiosProfesional(id))
        except Exception as e:
            QMessageBox.critical(None, 'Error', f"Error: {e}")

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
        
        if success:
            QMessageBox.information(None, 'Mensaje', 'Profesional actualizado correctamente')
            
        else:
            QMessageBox.critical(None, 'Error', f'El profesional no pudo ser actualizado: {error_message}')
            
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

        
        if eliminado:
            QMessageBox.information(None, 'Mensaje', 'Profesional eliminado')
            
        else:
            QMessageBox.critical(None, 'Error', 'El profesional no pudo ser eliminado')

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
            for id_profesional, nombre, apellido, profesion in profesionales:
                item = f"{nombre} {apellido} - {profesion}"
                self.asocProf.cbProfesionales.addItem(item, userData=id_profesional)
        else:
            self.asocProf.cbProfesionales.addItem("No hay profesionales cargados")

        # Conectar señal para actualizar ID del profesional seleccionado
        self.asocProf.cbProfesionales.currentIndexChanged.connect(lambda index: self.actualizar_id_profesional(index))

        # Conectar botón Registrar
        self.asocProf.btnRegistrar.clicked.connect(lambda: self.asociarProfesionalAPaciente(id_paciente))
        self.asocProf.show()

    def actualizar_id_profesional(self, index):
        if index >= 0:
            item_data = self.asocProf.cbProfesionales.itemData(index)
            if item_data is not None:
                self.id_profesional_seleccionado = item_data  # Almacenar el ID del profesional seleccionado
                print(f"ID del profesional seleccionado: {self.id_profesional_seleccionado}")
            else:
                print("No se encontró el ID del profesional seleccionado.")
        else:
            print("No se seleccionó ningún profesional.")

    def asociarProfesionalAPaciente(self, id_paciente):
        if hasattr(self, 'id_profesional_seleccionado'):
            id_profesional = self.id_profesional_seleccionado
            try:
                objData = PacienteProfesionalesData()
                exito = objData.asociar_profesional_a_paciente(id_paciente, id_profesional)

                if exito:
                    QMessageBox.information(None, 'Mensaje', 'Profesional asociado al paciente correctamente')
                else:
                    QMessageBox.warning(None, 'Error', 'No se pudo asociar el profesional al paciente')
                    print(id_profesional)

                self.asocProf.close()  # Cerrar la ventana
            except Exception as e:
                QMessageBox.critical(None, 'Error', 'Seleccione un profesional')
                print(f"Error: {e}")
        else:
            QMessageBox.warning(None, 'Error', 'No se ha seleccionado ningún profesional')
           
################# PDF Profesionales ###############

    def descargar_pdf(self, id_profesional):
        try:
            # Obtener la información del profesional
            profesional = ProfesionalData()
            data = profesional.mostrar(id_profesional)
            profesional_data = {
                'nombre': data[1],
                'apellido': data[2],
                'cuit': data[5],
                'fecha_nacimiento': data[6],
                'direccion': data[3],
                'localidad': data[4],
                'codigo_postal': data[7],
                'telefono': data[9],                
                'mail': data[13],
                'profesion': data[16],
                'matricula': data[8],
                'cbu1': data[10],
                'cbu2': data[11],
                'alias': data[12],
                'monotributo': data[14],
                'coordinador': data[15],
                'cuidador': data[17],  
                'codigo_trans': data[18],
                'nombre2': data[19],
                'apellido2': data[20],
                'cuit2': data[21],
                'cbu3': data[22]              
            }
            
            # Mostrar el cuadro de diálogo para guardar el archivo PDF
            filePath, _ = QFileDialog.getSaveFileName(self.verProf, "Guardar PDF", f"{profesional_data['nombre']}_{profesional_data['apellido']}.pdf", "PDF Files (*.pdf)")
            
            if filePath:
                # Generar el PDF
                if self.generar_pdf_profesional(profesional_data, filePath):
                    QMessageBox.information(None, "Éxito", "El PDF se guardó correctamente.")
                else:
                    QMessageBox.warning(None, "Error", "No se pudo guardar el PDF.")
            else:
                QMessageBox.warning(None, "Advertencia", "No se seleccionó ningún archivo para guardar.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Ocurrió un error: {str(e)}")

    def generar_pdf_profesional(self, profesional_data, filePath):
        try:
            c = canvas.Canvas(filePath, pagesize=A4)
            width, height = A4
            margin = 1 * cm
            line_height = 0.5 * cm
            box_margin = 0.2 * cm
            
            # Ajustar el título
            c.setFont("Helvetica-Bold", 14)
            title_x = margin
            title_y = height - margin
            title_text = "Ficha de Profesional"
            title_width = c.stringWidth(title_text, "Helvetica-Bold", 14)
            c.drawString((width - title_width) / 2, title_y, title_text)  # Centrar el título
            
            # Ajustar el espacio después del título
            current_y = title_y - line_height * 2
            
            # Ajustar los campos
            c.setFont("Helvetica", 10)
            col_width = (width - 2 * margin) / 2  # Dividir el ancho de la página en 2 columnas
            box_height = 2 * line_height  # Altura de cada recuadro

            def procesar_boolean(data):
                if data == 'True':
                    return 'Sí'
                else:
                    return 'No'
                
            monotributo = procesar_boolean(profesional_data.get('monotributo', '{}'))

            coordinador = procesar_boolean(profesional_data.get('coordinador', '{}'))
            cuidador = procesar_boolean(profesional_data.get('cuidador', '{}'))
            fields = [ 
                ('Nombre', profesional_data.get('nombre', '')),
                ('Apellido', profesional_data.get('apellido', '')),
                ('CUIT', profesional_data.get('cuit', '')),
                ('Fecha de Nacimiento', profesional_data.get('fecha_nacimiento', '')),
                ('Domicilio', profesional_data.get('direccion', '')),
                ('Localidad', profesional_data.get('localidad', '')),
                ('Teléfono', profesional_data.get('telefono', '')),
                ('Código Postal', profesional_data.get('codigo_postal', '')),
                ('Mail', profesional_data.get('mail', '')),
                ('Profesión', profesional_data.get('profesion', '')),
                ('Matrícula', profesional_data.get('matricula', '')),
                ('CBU 1', profesional_data.get('cbu1', '')),
                ('CBU 2', profesional_data.get('cbu2', '')),
                ('Alias', profesional_data.get('alias', '')),
                ('Monotributo', monotributo),
                ('Coordinador', coordinador),
                ('Cuidador', cuidador),
                ('Código de transferencia', profesional_data.get('codigo_trans', '')),
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
            
            # Agregar sección de Pago a terceros
            
            subtitle_text = "Pago a Terceros"
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
            
            sections = [
                ('Nombre', profesional_data.get('nombre2', '')),
                ('Apellido', profesional_data.get('apellido2', '')),
                ('CUIT', profesional_data.get('cuit2', '')),
                ('CBU', profesional_data.get('cbu3', '')),               
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
        
###### PDF Pacientes de Profesional ######

    def descargar_pdf_pacientes(self, id_profesional):
        try:
            # Obtener la información del profesional y sus pacientes
            profesional = ProfesionalData().mostrar(id=id_profesional)
            pacientes = PacienteProfesionalesData().obtener_pacientes_de_profesional(profesional_id=id_profesional)
            print('pacientes ', pacientes)
            pacientes_data_list = []
            for item in pacientes:
                print('paciente ', item[0])
                profesional_data = {
                    'nombre': item[1],
                    'apellido': item[2],
                    'visitas': item[3],
                    'valor': item[4],
                    'total': item[5]                 
                }
                pacientes_data_list.append(profesional_data)
            
            # Mostrar el cuadro de diálogo para guardar el archivo PDF
            filePath, _ = QFileDialog.getSaveFileName(self.verProf, "Guardar PDF", f"Pacientes_de_{profesional[1]}_{profesional[2]}.pdf", "PDF Files (*.pdf)")

            if filePath:
                # Generar el PDF
                if self.generar_pdf_pacientes(pacientes_data_list, filePath, profesional):
                    QMessageBox.information(None, "Éxito", "El PDF se guardó correctamente.")
                else:
                    QMessageBox.warning(None, "Error", "No se pudo guardar el PDF.")
            else:
                QMessageBox.warning(None, "Advertencia", "No se seleccionó ningún archivo para guardar.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Ocurrió un error: {str(e)}")

    def generar_pdf_pacientes(self, pacientes_data_list, filePath, profesional):
        try:
            c = canvas.Canvas(filePath, pagesize=A4)
            width, height = A4
            margin = 1 * cm
            line_height = 0.5 * cm
            box_margin = 0.2 * cm

            # Ajustar el título
            c.setFont("Helvetica-Bold", 14)
            title_x = margin
            title_y = height - margin
            title_text = f"Pacientes de {profesional[1]} {profesional[2]}"
            title_width = c.stringWidth(title_text, "Helvetica-Bold", 14)
            c.drawString((width - title_width) / 2, title_y, title_text)  # Centrar el título

            # Ajustar el espacio después del título
            current_y = height - margin - line_height * 4
            
            # Ajustar los campos
            c.setFont("Helvetica", 10)
            num_cols = 5  # Cambiado a 5 columnas
            col_width = (width - 2 * margin) / num_cols  # Dividir el ancho de la página en 5 columnas
            box_height = 2 * line_height  # Altura de cada recuadro
            
             # Inicializar la suma total
            total_general = 0

            # Dibujar las cabeceras de las columnas
            headers = ['Apellido', 'Nombre', 'Cantidad de visitas', 'Valor', 'Total']
            for i, header in enumerate(headers):
                x = margin + i * col_width
                y = current_y
                c.rect(x, y, col_width, box_height)  # Dibujar el recuadro
                c.drawString(x + box_margin, y + box_height - line_height - box_margin, header)  # Dibujar el texto del encabezado
            
            # Ajustar la posición para los datos
            current_y -= box_height  # Mover hacia abajo para empezar a dibujar datos
            total_row_y = 0
            # Iterar sobre la lista de pacientes
            for index, paciente_data in enumerate(pacientes_data_list):
                col = 0  # Empezar en la primera columna
                row = index  # Fila en la que se encuentra el recuadro
                
                for key in headers:
                    print('key ', key)
                    # Convertir el encabezado a minúsculas para coincidir con las claves del diccionario
                    key = key.lower().replace('cantidad de ', '')
                    print('key post ', key)
                    value = paciente_data.get(key, '')

                    # Sumar el total si es una columna de total
                    if key == 'total':
                        try:
                            total_general += float(value)  # Convertir a flotante y acumular
                        except ValueError:
                            pass  # Ignorar si el valor no es un número
                    
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

            
            # Ajustar la posición para la fila de totales (dos filas más abajo)
            total_row_y = current_y - (box_height * 4) # Mover dos filas hacia abajo

            # # Dibujar la fila de totales
            # c.setFont("Helvetica-Bold", 10)
            # c.drawString(margin, total_row_y, "Total General")  # Texto para la fila de totales
            # c.setFont("Helvetica", 10)

            # Dibujar recuadro del total general
            x = margin + i * col_width
            c.rect(x, total_row_y, col_width, box_height)  # Dibujar el recuadro
            total_str = "{:.2f}".format(total_general)  # Formatear el total
            c.drawString(x + box_margin, total_row_y + box_height - line_height - box_margin, total_str)
            
            # Finalizar el PDF
            c.save()
            return True
        except Exception as e:
            print(f"Error al generar el PDF: {str(e)}")
            return False