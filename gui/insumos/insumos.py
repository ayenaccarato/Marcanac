import os

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QPushButton, QWidget, QHBoxLayout, QTableWidgetItem
from data.insumos import InsumoData
from data.paciente_insumo import PacienteInsumoData
from model.insumo import Insumo

class InsumosWindow():

    def __init__(self):
        InsumoData()
        PacienteInsumoData()
        #elf.nInsumo = uic.loadUi("gui/insumos/cargar_insumo.ui")
        ui_file = os.path.join(os.path.dirname(__file__), '..', 'insumos', 'cargar_insumo.ui')
        ui_file = os.path.abspath(ui_file)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file):
            print(f"Error: el archivo {ui_file} no se encuentra.")
            return
        self.nInsumo = uic.loadUi(ui_file)

        #self.lInsumo = uic.loadUi("gui/insumos/listado_insumos.ui")
        ui_file_i = os.path.join(os.path.dirname(__file__), '..', 'insumos', 'listado_insumos.ui')
        ui_file_i = os.path.abspath(ui_file_i)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file_i):
            print(f"Error: el archivo {ui_file_i} no se encuentra.")
            return
        self.lInsumo = uic.loadUi(ui_file_i)

####### Nuevo #######

    def abrirRegistroInsumo(self, id):   
        self.nInsumo.btnRegistrar.clicked.connect(lambda: self.registrarInsumo(id))          
        self.nInsumo.show()

    def registrarInsumo(self, id_paciente):
        if self.nInsumo.cbInsumo.currentText() == "--Seleccione--" and self.nInsumo.txtOtro.text() == '':       
            QMessageBox.information(None, 'Mensaje', 'Seleccione o escriba un insumo')     
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

            success, error_message = objData.registrar(insumo=nuevoInsumo, id_paciente=id_paciente)
            if success:   
                QMessageBox.information(None, 'Mensaje', 'Insumo agregado')        
            else:
                QMessageBox.warning(None, 'Error', f'El insumo no pudo ser agregado: {error_message}')

            self.mostrarInsumos(id_paciente)
            self.nInsumo.close() #Cierro la ventana

    ### Eliminar ###

    def eliminar_insumo(self, id_insumo, id_paciente):
        # Crear el cuadro de diálogo de confirmación
        mBox = QMessageBox()
        mBox.setWindowTitle('Confirmar eliminación')
        mBox.setText("¿Está seguro que desea eliminar este insumo?")

        # Añadir botones personalizados
        si_btn = mBox.addButton("Sí", QMessageBox.ButtonRole.YesRole)
        no_btn = mBox.addButton("No", QMessageBox.ButtonRole.NoRole)
        
        mBox.setDefaultButton(no_btn)
        mBox.exec()

        if mBox.clickedButton() == si_btn:
            self.confirmar(id_insumo, id_paciente)
        else:
            print("Eliminación cancelada")

    def confirmar(self, id_insumo, id_paciente):
        '''Se elimina el profesional, si confirman'''
        pInsumo = PacienteInsumoData()
        pInsumo.eliminar_relacion_paciente_insumo(id_paciente, id_insumo)
        insumo = InsumoData()
        eliminado = insumo.eliminar(id_insumo)

        if eliminado:
            QMessageBox.information(None, 'Mensaje', 'Insumo eliminado')
        else:
            QMessageBox.warning(None, 'Error', 'El insumo no pudo ser eliminado')

        # self.lInsumo.close()
        # self.mostrarInsumos(id_paciente)

##### Listado #####

    def mostrarInsumos(self, id_paciente):

        lis = InsumoData()
        insumos = lis.mostrar(id_paciente)   
        print(insumos)     
        
        if insumos:
            self.lInsumo.swInsumos.setCurrentIndex(1)
            self.lInsumo.tblListadoI.setRowCount(len(insumos))  # Configurar el número de filas
            
            fila = 0
            for item in insumos:
                
                self.lInsumo.tblListadoI.setItem(fila, 0, QTableWidgetItem(str(item[1])))
                self.lInsumo.tblListadoI.setItem(fila, 1, QTableWidgetItem(str(item[2])))
                self.lInsumo.tblListadoI.setItem(fila, 2, QTableWidgetItem(str(item[3])))

                id_valor = item[0]
            
                self.boton_listado_insumo(id_valor, fila, id_paciente)

                fila += 1
        else:
            self.lInsumo.swInsumos.setCurrentIndex(0)
        
        self.lInsumo.btnInsumo.clicked.connect(lambda: self.abrirRegistroInsumo(id_paciente))
        self.lInsumo.btnRefrescar.clicked.connect(lambda: self.mostrarInsumos(id_paciente))
        self.lInsumo.show()

    def boton_listado_insumo(self, id_valor, fila, id_paciente):        
        
        # Crear el botón y añadirlo a la columna 7
        # Crear el botón "Ver más" y conectarlo
        btn = QPushButton("Eliminar")
        
        btn.clicked.connect(lambda _, id_valor=id_valor, id_paciente=id_paciente: self.eliminar_insumo(id_valor, id_paciente))
        
        # Agregar estilo al botón
        btn.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(btn)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
       
        self.lInsumo.tblListadoI.setCellWidget(fila, 3, widget)