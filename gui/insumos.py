import json

from PyQt6 import uic, QtCore
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMessageBox, QPushButton, QWidget, QHBoxLayout, QTableWidgetItem
from data.insumos import InsumoData
from data.listados import ListadoData
from model.insumo import Insumo

class InsumosWindow():

    def initGUI(self):
        self.nInsumo = uic.loadUi("gui/cargar_insumo.ui")
        self.lInsumo = uic.loadUi("gui/listado_insumos.ui")

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
            
            fila = 0
            for item in insumos:
                
                self.lInsumo.tblListadoI.setItem(fila, 0, QTableWidgetItem(str(item[1])))
                self.lInsumo.tblListadoI.setItem(fila, 1, QTableWidgetItem(str(item[2])))
                self.lInsumo.tblListadoI.setItem(fila, 2, QTableWidgetItem(str(item[3])))

                fila += 1
        
        self.lInsumo.btnInsumo.clicked.connect(lambda: self.abrirRegistroInsumo(id_paciente))
        self.lInsumo.btnRefrescar.clicked.connect(lambda: self.mostrarInsumos(id_paciente))
        self.lInsumo.show()