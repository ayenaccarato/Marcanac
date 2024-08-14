from datetime import datetime
import os

from data.mes_pago import MesPagoData

from data.profesional import ProfesionalData
from model.usuario import Usuario

from PyQt6 import uic
from PyQt6.QtWidgets import QTableWidgetItem



class MesPagoWindow():

    def __init__(self, user: Usuario):
        self.usuario = user

        ui_file = os.path.join(os.path.dirname(__file__), '..', 'profesionales' ,'listado_pago_profesionales.ui')
        ui_file = os.path.abspath(ui_file)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file):
            print(f"Error: el archivo {ui_file} no se encuentra.")
            return
        self.mes_pago = uic.loadUi(ui_file)

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

    def listado_pago_profesionales(self):
       
        mes_actual = self.obtener_nombre_mes()

        profesional = ProfesionalData()
        lis = MesPagoData()
        data = lis.obtener_profesionales_por_mes(mes_actual)

        # Ordenar data por el apellido del paciente (suponiendo que el apellido es el índice 2 en `paciente`)
        data = sorted(data, key=lambda item: profesional.mostrar(item[1])[2])
 
        fila = 0
        self.mes_pago.tblListado.setRowCount(len(data)) #Cuantas filas traen los datos

        for item in data:            
            info = profesional.mostrar(item[1])

            self.mes_pago.tblListado.setItem(fila, 0, QTableWidgetItem(str(info[2]))) #Apellido
            self.mes_pago.tblListado.setItem(fila, 1, QTableWidgetItem(str(info[1]))) #Nombre
            self.mes_pago.tblListado.setItem(fila, 2, QTableWidgetItem(str(item[3]))) #Mes a Pagar
           
            self.mes_pago.tblListado.setItem(fila, 3, QTableWidgetItem(str(info[18]))) #Código de transferencia

            self.mes_pago.tblListado.setItem(fila, 4, QTableWidgetItem(str(item[2]))) #Total a pagar

            fila += 1
 
        self.mes_pago.tblListado.setColumnWidth(0,150)
        self.mes_pago.tblListado.setColumnWidth(1,150)
        try:
            self.mes_pago.btnBuscar.clicked.disconnect()
        except TypeError:
            pass
        self.mes_pago.btnBuscar.clicked.connect(lambda: self.buscar())
        self.mes_pago.btnLista.setVisible(False)

        #self.limpiar_campos_busqueda()   
        self.mes_pago.show()

    def buscar(self):
        self.mes_pago.tblListado.clearContents()  # Limpiar contenido actual de la tabla
        self.mes_pago.tblListado.setRowCount(0)

        mes_actual = self.obtener_nombre_mes()

        profesional = ProfesionalData()
        lis = MesPagoData()
        data = lis.obtener_profesionales_por_mes(mes_actual)
        
        data = lis.obtener_busqueda(self.mes_pago.txtApellido.text().upper(), self.mes_pago.txtCodigo.text())

        if data:
            # Reiniciar número de filas
            fila = 0
            self.mes_pago.tblListado.setRowCount(len(data)) #Cuantas filas traen los datos

            for item in data:
                #info = profesional.mostrar(item[1])

                self.mes_pago.tblListado.setItem(fila, 0, QTableWidgetItem(str(item[0]))) #Apellido
                self.mes_pago.tblListado.setItem(fila, 1, QTableWidgetItem(str(item[1]))) #Nombre
                self.mes_pago.tblListado.setItem(fila, 2, QTableWidgetItem(str(item[3]))) #Mes a Pagar
            
                self.mes_pago.tblListado.setItem(fila, 3, QTableWidgetItem(str(item[2]))) #Código de transferencia

                self.mes_pago.tblListado.setItem(fila, 4, QTableWidgetItem(str(item[4]))) #Total a pagar

                fila += 1
    
            self.mes_pago.tblListado.setColumnWidth(0,150)
            self.mes_pago.tblListado.setColumnWidth(1,150)
        else:
                # Limpiar la tabla si no se encontraron resultados
            self.mes_pago.tblListado.clearContents()
            self.mes_pago.tblListado.setRowCount(0)

        self.mes_pago.btnLista.setVisible(True)
        self.mes_pago.btnLista.clicked.connect(lambda: self.listado_pago_profesionales())