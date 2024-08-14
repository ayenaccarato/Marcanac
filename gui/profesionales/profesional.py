import calendar
import os
import shutil


from functools import partial
from datetime import datetime
from time import strftime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from PyQt6 import uic, QtCore
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QPushButton, QWidget, QHBoxLayout, QTableWidgetItem, QStyledItemDelegate, QListWidgetItem, QAbstractItemView
from data.listados import ListadoData
from data.paciente import PacienteData
from data.paciente_profesionales import PacienteProfesionalesData

from data.profesional import ProfesionalData
from gui.profesionales.archivos_profesional import ArchivosProfesionalWindow

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

        ui_file_pac = os.path.join(os.path.dirname(__file__), '..', 'profesionales' ,'listado_pacientes_profesional.ui')
        ui_file_pac = os.path.abspath(ui_file_pac)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file_pac):
            print(f"Error: el archivo {ui_file_pac} no se encuentra.")
            return
        self.lisPacientes = uic.loadUi(ui_file_pac)
            
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

    def abrirListadoProfesionales(self): 
        from gui.profesionales.mes_pago import MesPagoWindow
        self.listadoProf.showMaximized() #Maximizo la ventana
        archivos = ArchivosProfesionalWindow()
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

            fila += 1
 
        self.listadoProf.tblListadoProf.setColumnWidth(2,150)
        self.listadoProf.tblListadoProf.setColumnWidth(3,150)
        try:
            self.listadoProf.btnBuscar.clicked.disconnect()
            self.listadoProf.btnAPagar.clicked.disconnect()
        except TypeError:
            pass
        self.listadoProf.btnBuscar.clicked.connect(lambda: self.buscar('prof'))
        self.listadoProf.btnLista.setVisible(False)
        mes = MesPagoWindow(self.usuario)
        self.listadoProf.btnAPagar.clicked.connect(lambda: mes.listado_pago_profesionales())  
        if self.usuario.rol == 'admin':
            self.listadoProf.btnPago.setVisible(True)   
            self.listadoProf.btnPago.clicked.connect(lambda: archivos.mostrar_listWidget_años())         
        else:
            self.listadoProf.btnPago.setVisible(False)
        self.limpiar_campos_busqueda()   
        self.listadoProf.show()

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
        # else:
        #     self.lisPago.tblListado.clearContents()  # Limpiar contenido actual de la tabla
        #     self.lisPago.tblListado.setRowCount(0)

        #     lis = PagoProfesionalData() 
        #     data = lis.obtener_pagos_profesional(self.lisPago.cbMes.currentText())

        #     if data:
        #         # Reiniciar número de filas
        #         fila = 0
        #         self.lisPago.tblListado.setRowCount(len(data)) #Cuantas filas traen los datos
        #         for item in data:
        #             profesional = ProfesionalData().mostrar(item[0])

        #             self.lisPago.tblListado.setItem(fila, 0, QTableWidgetItem(str(item[2]))) #Fecha de pago
        #             self.lisPago.tblListado.setItem(fila, 1, QTableWidgetItem(str(profesional[2]))) #Apellido
        #             self.lisPago.tblListado.setItem(fila, 2, QTableWidgetItem(str(profesional[1]))) #Nombre
        #             self.lisPago.tblListado.setItem(fila, 3, QTableWidgetItem(str(profesional[18]))) #Codigo
        #             self.lisPago.tblListado.setItem(fila, 4, QTableWidgetItem(str(profesional[16]))) #Profesion

        #             fila += 1
                
        #     else:
        #         # Limpiar la tabla si no se encontraron resultados
        #         self.lisPago.tblListado.clearContents()
        #         self.lisPago.tblListado.setRowCount(0)

            self.lisPago.btnLista.setVisible(True)
            self.lisPago.btnLista.clicked.connect(lambda: self.listado_pagos())

    def limpiar_campos_busqueda(self):        
        self.listadoProf.txtCuit.clear()  # Limpia el contenido del primer QLineEdit
        self.listadoProf.txtApellido.clear()
        self.listadoProf.cbProfesion.setCurrentIndex(0)

    # def handleCellChanged(self, item, id_profesional):
    #     self.pp = PacienteProfesionalesData()
    #     if item is not None:
    #         row = item.row()
    #         column = item.column()
    #         id_paciente = self.lisPacientes.tblListado.item(row, 0).text()  # ID del paciente
    #         new_value = item.text()  # Nuevo valor de la celda

    #         # Convertir el nuevo valor a número si es necesario
    #         try:
    #             if column in [3, 4]:  # Solo convertir si es una columna editable
    #                 new_value = float(new_value)
    #         except ValueError:
    #             # Si no es posible convertir a float, se ignora el cambio
    #             QMessageBox.warning(None, "Advertencia", "El valor ingresado no es un número válido.")
    #             return

    #         # Solo actualiza si la columna es una de las permitidas
    #         if column in [3, 4]:  # Columnas editables: visitas (3) y valor (4)
    #             self.lisPacientes.tblListado.blockSignals(True)
    #             try:
    #                 # Obtener los valores actuales de visitas y valor
    #                 visitas_item = self.lisPacientes.tblListado.item(row, 3)
    #                 valor_item = self.lisPacientes.tblListado.item(row, 4)
    #                 total_item = self.lisPacientes.tblListado.item(row, 5)

    #                 visitas = float(visitas_item.text()) if visitas_item is not None else 0
    #                 valor = float(valor_item.text()) if valor_item is not None else 0

    #                 # Calcular el nuevo total
    #                 total = visitas * valor

    #                 # Actualizar la celda del total
    #                 if total_item is not None:
    #                     total_item.setText(str(total))
    #                 else:
    #                     self.lisPacientes.tblListado.setItem(row, 5, QTableWidgetItem(str(total)))

    #                 # Actualizar en la base de datos
    #                 success, error_message = self.pp.actualizar_dato(id_paciente=id_paciente, columna=column, nuevo_valor=new_value, id_profesional=id_profesional)
    #                 if not success:
    #                     QMessageBox.critical(None, 'Error', f"No se pudo actualizar el dato: {error_message}")
    #             finally:
    #                 self.lisPacientes.tblListado.blockSignals(False)

    def handleCellChanged(self, item, id_profesional):
        self.pp = PacienteProfesionalesData()
        if item is not None:
            row = item.row()
            column = item.column()
            id_paciente = self.lisPacientes.tblListado.item(row, 0).text()  # ID del paciente
            new_value = item.text()  # Nuevo valor de la celda

            # Convertir el nuevo valor a número si es necesario
            try:
                if column in [3, 4, 5]:  # Solo convertir si es una columna editable
                    new_value = float(new_value)
            except ValueError:
                QMessageBox.warning(None, "Advertencia", "El valor ingresado no es un número válido.")
                return

            # Solo actualiza si la columna es una de las permitidas
            if column in [3, 4, 5]:  # Columnas editables: cantidad (3), valor (4) y mes (5)
                self.lisPacientes.tblListado.blockSignals(True)
                try:
                    # Obtener los valores actuales de cantidad, valor, y mes
                    cantidad_item = self.lisPacientes.tblListado.item(row, 3)
                    valor_item = self.lisPacientes.tblListado.item(row, 4)
                    mes_item = self.lisPacientes.tblListado.item(row, 5)
                    total_item = self.lisPacientes.tblListado.item(row, 6)

                    cantidad = float(cantidad_item.text()) if cantidad_item is not None else 0
                    valor = float(valor_item.text()) if valor_item is not None else 0
                    mes = float(mes_item.text()) if mes_item is not None else 1  # Si no hay mes, se usa 1

                    # Calcular el nuevo total
                    total = cantidad * valor * mes

                    # Actualizar la celda del total
                    if total_item is not None:
                        total_item.setText(str(total))
                    else:
                        self.lisPacientes.tblListado.setItem(row, 6, QTableWidgetItem(str(total)))

                    # Actualizar en la base de datos
                    success, error_message = self.pp.actualizar_dato(id_paciente=id_paciente, columna=column, nuevo_valor=new_value, id_profesional=id_profesional)
                    if not success:
                        QMessageBox.critical(None, 'Error', f"No se pudo actualizar el dato: {error_message}")
                finally:
                    self.lisPacientes.tblListado.blockSignals(False)

    def boton_listado_pacientes_prof (self, id_profesional, id_valor, fila):              
        # Crear el botón y añadirlo a la columna 4
        # Crear el botón "Eliminar" y conectarlo
        btn = QPushButton("Eliminar")
        btn.clicked.connect(partial(self.eliminarRelacionPacienteProfesional, id_profesional, id_valor))
        #btn.clicked.connect(lambda _, id_valor=id_valor: self.eliminarRelacionPacienteProfesional(id_valor, id_profesional))
        # Agregar estilo al botón
        btn.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(btn)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lisPacientes.tblListado.setCellWidget(fila, 7, widget)

    def listado_pacientes(self, id_profesional):
        from gui.pacientes.paciente import PacienteWindow
        
        pacientes = PacienteProfesionalesData()
        data = pacientes.obtener_pacientes_de_profesional(id_profesional)

        profesional = ProfesionalData()
        info = profesional.es_cuidador(id_profesional)
        print('info ', info)

        print(f"Datos obtenidos para el profesional {id_profesional}: {data}")

        # Ordenar data por el apellido del paciente (suponiendo que el apellido es el índice 2 en `paciente`)
        data = sorted(data, key=lambda item: PacienteData().mostrar(item[0])[2])

        fila = 0
        self.lisPacientes.tblListado.setRowCount(len(data))  # Cuantas filas traen los datos

        self.total_general = 0
        self.lisPacientes.txtTotal.setText('$ '+ str(self.total_general))
        for item in data:
            paciente = PacienteData().mostrar(item[0])

            self.lisPacientes.tblListado.hideColumn(0)
            self.lisPacientes.tblListado.setItem(fila, 0, QTableWidgetItem(str(item[0])))  # ID
            
            self.lisPacientes.tblListado.setItem(fila, 1, QTableWidgetItem(str(paciente[2])))  # Apellido
            self.lisPacientes.tblListado.setItem(fila, 2, QTableWidgetItem(str(paciente[1])))  # Nombre
            
            self.lisPacientes.tblListado.setItem(fila, 3, QTableWidgetItem(str(item[3]) if item[3] is not None else '0'))  # Cantidad
            self.lisPacientes.tblListado.setItem(fila, 4, QTableWidgetItem(str(item[4]) if item[4] is not None else '0'))  # Valor

            if info is True:
                self.lisPacientes.tblListado.setItem(fila, 5, QTableWidgetItem(str(item[4]) if item[4] is not None else '0'))  # Mes
            else:
                self.lisPacientes.tblListado.hideColumn(5)

            self.lisPacientes.tblListado.setItem(fila, 6, QTableWidgetItem(str(item[5]) if item[5] is not None else '0'))  # Total

            id_valor = item[0]

            self.boton_listado_pacientes_prof(id_profesional, id_valor, fila)

            fila += 1

            self.lisPacientes.tblListado.itemChanged.connect(lambda item: self.handleCellChanged(item, id_profesional))
            self.total_general += float(item[5])

        self.lisPacientes.txtTotal.setText('$ ' + str(self.total_general))
        self.total_con_descuento = self.total_general  # Inicializa el total con descuento
        
        self.lisPacientes.tblListado.setColumnWidth(1, 150)
        self.lisPacientes.tblListado.setColumnWidth(2, 150)
        self.lisPacientes.tblListado.setColumnWidth(3, 150)

        self.paciente_window = PacienteWindow(self.usuario)
        try:
            self.lisPacientes.btnDescargar.clicked.disconnect()
            self.lisPacientes.btnRefrescar.clicked.disconnect()
            self.lisPacientes.btnAgregar.clicked.disconnect()
            self.lisPacientes.btnDescontar.clicked.disconnect()
            self.lisPacientes.btnGuardar.clicked.disconnect()
        except TypeError:
            pass
        self.lisPacientes.btnAgregar.clicked.connect(lambda: self.paciente_window.cargar_pacientes(id_profesional=id_profesional))
        self.lisPacientes.btnRefrescar.clicked.connect(lambda: self.listado_pacientes(id_profesional))
        self.lisPacientes.btnDescargar.clicked.connect(lambda: self.descargar_pdf_pacientes(id_profesional))
        self.lisPacientes.btnDescontar.clicked.connect(lambda: self.descontar_10(self.total_general))
               
        self.lisPacientes.btnGuardar.clicked.connect(lambda: self.guardar(id_profesional))

        self.lisPacientes.show()

    def descontar_10(self, total_general):
        try:
            # Calcular el total con el descuento del 10%
            total_con_descuento = total_general * 0.9

            self.lisPacientes.txtTotal.setText('$ ' + str(total_con_descuento))

            # Guardar el total con descuento en un atributo
            self.total_con_descuento = total_con_descuento
        
        except Exception as e:
            QMessageBox.critical(None, 'Error', f"Error al aplicar el descuento: {e}")

    def guardar(self, id_profesional):
        from data.mes_pago import MesPagoData
        mes = MesPagoData()
        mes_actual = self.obtener_nombre_mes()

        total_a_guardar = self.total_con_descuento

        success, error_message = mes.guardar_pago(id_profesional, total_a_guardar, mes_actual)
        if success:
            QMessageBox.information(None, 'Mensaje', 'El pago fue guardado.')
        else:
            QMessageBox.critical(None, 'Error', f'Ocurrió un error: {error_message}')
        
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

    def eliminarRelacionPacienteProfesional(self, id_profesional, id_valor):
        '''Eliminar la relación entre un paciente y un profesional'''

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
            prof = PacienteProfesionalesData()
            success, error_message = prof.eliminar_relacion_paciente_profesional(id_valor, id_profesional)
            if success:
                
                QMessageBox.information(None, "Eliminación exitosa", "El paciente ha sido eliminado correctamente.")            
                self.lisPacientes.close()
                self.listado_pacientes(id_profesional)  # Refrescar la tabla
            else:
                QMessageBox.warning(None, 'Error', f'No se pudo eliminar el profesional: {error_message}')
        else:
            print("Eliminación cancelada")

##### Asociar Profesionales #####

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

    def obtener_nombre_mes(self):
        # Obtener el número del mes actual (01 a 12)
        mes_numero = int(datetime.now().strftime("%m"))  # Convertir el mes a entero para usar en calendar.month_name

        # Diccionario para traducir nombres de meses a castellano
        meses_castellano = {
            1: 'Enero',
            2: 'Febrero',
            3: 'Marzo',
            4: 'Abril',
            5: 'Mayo',
            6: 'Junio',
            7: 'Julio',
            8: 'Agosto',
            9: 'Septiembre',
            10: 'Octubre',
            11: 'Noviembre',
            12: 'Diciembre'
        }
        
        # Obtener el nombre del mes en castellano
        mes_nombre = meses_castellano.get(mes_numero)
        
        # Verificar si el nombre del mes es None, lo que indica un mes no válido
        if mes_nombre is None:
            raise ValueError("Número de mes inválido")
        
        return mes_nombre

    # def descargar_pdf_pacientes(self, id_profesional):
    #     try:
    #         # Obtener la información del profesional y sus pacientes
    #         profesional = ProfesionalData().mostrar(id=id_profesional)
    #         pacientes = PacienteProfesionalesData().obtener_pacientes_de_profesional(profesional_id=id_profesional)
    #         print('pacientes ', pacientes)
    #         pacientes_data_list = []
    #         for item in pacientes:
    #             print('paciente ', item[0])
    #             profesional_data = {
    #                 'nombre': item[1],
    #                 'apellido': item[2],
    #                 'visitas': item[3],
    #                 'valor': item[4],
    #                 'total': item[5]                 
    #             }
    #             pacientes_data_list.append(profesional_data)
            
    #         # Mostrar el cuadro de diálogo para guardar el archivo PDF
    #         filePath, _ = QFileDialog.getSaveFileName(self.verProf, "Guardar PDF", f"Pacientes_de_{profesional[1]}_{profesional[2]}.pdf", "PDF Files (*.pdf)")

    #         if filePath:
    #             # Generar el PDF
    #             if self.generar_pdf_pacientes(pacientes_data_list, filePath, profesional):
    #                 QMessageBox.information(None, "Éxito", "El PDF se guardó correctamente.")
    #             else:
    #                 QMessageBox.warning(None, "Error", "No se pudo guardar el PDF.")
    #         else:
    #             QMessageBox.warning(None, "Advertencia", "No se seleccionó ningún archivo para guardar.")
    #     except Exception as e:
    #         QMessageBox.critical(None, "Error", f"Ocurrió un error: {str(e)}")

    def descargar_pdf_pacientes(self, id_profesional):
        try:
            # Obtener la información del profesional y sus pacientes
            profesional = ProfesionalData().mostrar(id=id_profesional)
            pacientes = PacienteProfesionalesData().obtener_pacientes_de_profesional(profesional_id=id_profesional)
            print('pacientes ', pacientes)
            
            pacientes_data_list = []
            for item in pacientes:
                profesional_data = {
                    'nombre': item[1],
                    'apellido': item[2],
                    'cantidad': item[3],
                    'valor': item[4],
                    'total': item[5]                 
                }
                pacientes_data_list.append(profesional_data)
            
            # Mostrar el cuadro de diálogo para guardar el archivo PDF
            filePath, _ = QFileDialog.getSaveFileName(self.verProf, "Guardar PDF", f"Pacientes_de_{profesional[1]}_{profesional[2]}.pdf", "PDF Files (*.pdf)")

            # Obtener la ruta de la carpeta del mes actual
            año_actual = datetime.now().year
            mes_nombre = self.obtener_nombre_mes()

            ruta_carpeta_ano = os.path.join(os.path.dirname(__file__), '..', 'pagos', str(año_actual))
            # Asegurarse de que la carpeta del año y la del mes existan, creándolas si es necesario
            os.makedirs(ruta_carpeta_ano, exist_ok=True)
            ruta_carpeta_mes = os.path.join(ruta_carpeta_ano, mes_nombre)
            os.makedirs(ruta_carpeta_mes, exist_ok=True)
            nombre_archivo = f"Pacientes_de_{profesional[1]}_{profesional[2]}_{mes_nombre}_{año_actual}.pdf"
            ruta_completa_carpeta = os.path.join(ruta_carpeta_mes, nombre_archivo)

            # Verificar si se ha seleccionado una ruta para guardar el archivo PDF
            if filePath:
                # Crear la carpeta del mes si no existe
                if not os.path.exists(ruta_carpeta_mes):
                    os.makedirs(ruta_carpeta_mes)
                
                # # Guardar el PDF en la carpeta del mes
                # if self.generar_pdf_pacientes(pacientes_data_list, ruta_completa_carpeta, profesional):
                #     QMessageBox.information(None, "Éxito", f"El PDF se guardó en {filePath} y {ruta_completa_carpeta}.")
                # else:
                #     QMessageBox.warning(None, "Error", "No se pudo guardar el PDF.")
                 # Guardar el PDF en la carpeta del mes
                if self.generar_pdf_pacientes(pacientes_data_list, ruta_completa_carpeta, profesional):
                    # Copiar el archivo PDF a la ubicación seleccionada por el usuario
                    if os.path.exists(ruta_completa_carpeta):
                        try:
                            shutil.copy(ruta_completa_carpeta, filePath)
                            QMessageBox.information(None, "Éxito", "El PDF se guardó correctamente en ambas ubicaciones.")
                        except Exception as e:
                            QMessageBox.warning(None, "Error", "No se pudo guardar el PDF.")
                            #QMessageBox.critical(None, "Error", f"No se pudo copiar el archivo a la ubicación seleccionada: {e}")
            else:
                QMessageBox.warning(None, "Advertencia", "No se seleccionó ningún archivo para guardar.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Ocurrió un error: {str(e)}")

    # def generar_pdf_pacientes(self, pacientes_data_list, filePath, profesional):
    #     try:
    #         c = canvas.Canvas(filePath, pagesize=A4)
    #         width, height = A4
    #         margin = 1 * cm
    #         line_height = 0.5 * cm
    #         box_margin = 0.2 * cm

    #         # Ajustar el título
    #         c.setFont("Helvetica-Bold", 14)
    #         title_x = margin
    #         title_y = height - margin
    #         title_text = f"Pacientes de {profesional[1]} {profesional[2]}"
    #         title_width = c.stringWidth(title_text, "Helvetica-Bold", 14)
    #         c.drawString((width - title_width) / 2, title_y, title_text)  # Centrar el título

    #         # Ajustar el espacio después del título
    #         current_y = height - margin - line_height * 4
            
    #         # Ajustar los campos
    #         c.setFont("Helvetica", 10)
    #         num_cols = 5  # Cambiado a 5 columnas
    #         col_width = (width - 2 * margin) / num_cols  # Dividir el ancho de la página en 5 columnas
    #         box_height = 2 * line_height  # Altura de cada recuadro
            
    #         # # Inicializar la suma total
    #         # total_general = 0

    #         # Dibujar las cabeceras de las columnas
    #         headers = ['Apellido', 'Nombre', 'Cantidad', 'Valor', 'Total']
    #         for i, header in enumerate(headers):
    #             x = margin + i * col_width
    #             y = current_y
    #             c.rect(x, y, col_width, box_height)  # Dibujar el recuadro
    #             c.drawString(x + box_margin, y + box_height - line_height - box_margin, header)  # Dibujar el texto del encabezado
            
    #         # Ajustar la posición para los datos
    #         current_y -= box_height  # Mover hacia abajo para empezar a dibujar datos
    #         total_row_y = 0
    #         # Iterar sobre la lista de pacientes
    #         for index, paciente_data in enumerate(pacientes_data_list):
    #             col = 0  # Empezar en la primera columna
    #             row = index  # Fila en la que se encuentra el recuadro
                
    #             for key in headers:
    #                 # Convertir el encabezado a minúsculas para coincidir con las claves del diccionario
    #                 key = key.lower().replace('cantidad de ', '')
    #                 value = paciente_data.get(key, '')

    #                 # # Sumar el total si es una columna de total
    #                 # if key == 'total':
    #                 #     try:
    #                 #         total_general += float(value)  # Convertir a flotante y acumular
    #                 #     except ValueError:
    #                 #         pass  # Ignorar si el valor no es un número
                    
    #                 # Calcular la posición para el dato
    #                 x = margin + col * col_width
    #                 y = current_y - row * box_height
                    
    #                 # Mostrar información de depuración
    #                 print(f"Index: {index}, Col: {col}, Row: {row}, X: {x}, Y: {y}, Value: {value}")
                    
    #                 # Dibujar el recuadro para el dato
    #                 c.rect(x, y, col_width, box_height)
                    
    #                 # Dibujar el dato dentro del recuadro
    #                 c.drawString(x + box_margin, y + box_height - line_height - box_margin, value)
                    
    #                 col += 1  # Mover a la siguiente columna
                    
    #             # Ajustar la posición para la próxima fila
    #             if (index + 1) % num_cols == 0:
    #                 current_y -= box_height

    #         # Ajustar la posición para la fila de totales (dos filas más abajo)
    #         total_row_y = current_y - (box_height * 4) # Mover dos filas hacia abajo

    #         total_text = self.lisPacientes.txtTotal.text().replace('$ ', '')  # Eliminar el símbolo '$ '
    #         total_float = float(total_text)  # Convertir a float

    #         # Dibujar recuadro del total general
    #         x = margin + i * col_width
    #         c.rect(x, total_row_y, col_width, box_height)  # Dibujar el recuadro
    #         total_str = "{:.2f}".format(total_float)  # Formatear el total
    #         c.drawString(x + box_margin, total_row_y + box_height - line_height - box_margin, total_str)
            
    #         # Finalizar el PDF
    #         c.save()
    #         return True
    #     except Exception as e:
    #         print(f"Error al generar el PDF: {str(e)}")
    #         return False
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
            num_cols = 5  # Número de columnas
            col_width = (width - 2 * margin) / num_cols  # Dividir el ancho de la página en 5 columnas
            box_height = 2 * line_height  # Altura de cada recuadro

            # Dibujar las cabeceras de las columnas
            headers = ['Apellido', 'Nombre', 'Cantidad', 'Valor', 'Total']
            for i, header in enumerate(headers):
                x = margin + i * col_width
                y = current_y
                c.rect(x, y, col_width, box_height)  # Dibujar el recuadro
                c.drawString(x + box_margin, y + box_height - line_height - box_margin, header)  # Dibujar el texto del encabezado

            # Ajustar la posición para los datos
            current_y -= box_height  # Mover hacia abajo para empezar a dibujar datos

            # Iterar sobre la lista de pacientes
            for index, paciente_data in enumerate(pacientes_data_list):
                col = 0  # Empezar en la primera columna
                
                for key in headers:
                    # Convertir el encabezado a minúsculas para coincidir con las claves del diccionario
                    key = key.lower().replace('cantidad de ', '')
                    value = paciente_data.get(key, '')

                    # Calcular la posición para el dato
                    x = margin + col * col_width
                    y = current_y
                    
                    # Dibujar el recuadro para el dato
                    c.rect(x, y, col_width, box_height)
                    
                    # Dibujar el dato dentro del recuadro
                    c.drawString(x + box_margin, y + box_height - line_height - box_margin, value)
                    
                    col += 1  # Mover a la siguiente columna
                
                # Ajustar la posición para la próxima fila
                current_y -= box_height

            # Agregar espacio en blanco antes del total general
            current_y -= box_height  # Dejar una fila en blanco

            # Dibujar el total general
            total_text = self.lisPacientes.txtTotal.text().replace('$ ', '')  # Eliminar el símbolo '$ '
            total_float = float(total_text)  # Convertir a float

            # Dibujar recuadro del total general
            c.rect(margin + 4 * col_width, current_y, col_width, box_height)  # Dibujar el recuadro en la última columna
            total_str = "{:.2f}".format(total_float)  # Formatear el total
            c.drawString(margin + 4 * col_width + box_margin, current_y + box_height - line_height - box_margin, total_str)
            
            # Finalizar el PDF
            c.save()
            return True
        except Exception as e:
            print(f"Error al generar el PDF: {str(e)}")
            return False