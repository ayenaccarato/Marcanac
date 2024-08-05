import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QPushButton, QWidget, QHBoxLayout, QTableWidgetItem, QFileDialog
from data.insumos import InsumoData
from data.paciente import PacienteData
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
        self.lInsumo.btnDescargar.clicked.connect(lambda: self.descargar_pdf(id_paciente))
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

########### PDF ###############

    def descargar_pdf(self, id_paciente):
        try:
            # Obtener la información de los insumos
            insumo = InsumoData()
            paciente = PacienteData()
            paciente_info = paciente.mostrar(id_paciente)
            data = insumo.mostrar(id_paciente)
            print(data)
            
            insumos_data_list = []
            for item in data:
                insumos_data = {
                    'fecha_entrega': item[1],
                    'nombre': item[2],
                    'cantidad': item[3],
                }
                insumos_data_list.append(insumos_data)
            
            # Mostrar el cuadro de diálogo para guardar el archivo PDF
            filePath, _ = QFileDialog.getSaveFileName(self.lInsumo, "Guardar PDF", f"Insumos_de_{paciente_info[1]}_{paciente_info[2]}.pdf", "PDF Files (*.pdf)")
            
            if filePath:
                # Generar el PDF
                if self.generar_pdf_paciente(insumos_data_list, filePath):
                    QMessageBox.information(None, "Éxito", "El PDF se guardó correctamente.")
                else:
                    QMessageBox.warning(None, "Error", "No se pudo guardar el PDF.")
            else:
                QMessageBox.warning(None, "Advertencia", "No se seleccionó ningún archivo para guardar.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Ocurrió un error: {str(e)}")

    def generar_pdf_paciente(self, insumos_data_list, filePath):
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
            title_text = "Insumos de paciente"
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
            headers = ['Fecha de entrega', 'Nombre', 'Cantidad']
            for i, header in enumerate(headers):
                x = margin + i * col_width
                y = current_y
                c.rect(x, y, col_width, box_height)  # Dibujar el recuadro
                c.drawString(x + box_margin, y + box_height - line_height - box_margin, header)  # Dibujar el texto del encabezado
            
            # Ajustar la posición para los datos
            current_y -= box_height  # Mover hacia abajo para empezar a dibujar datos

            # Iterar sobre la lista de profesionales
            for index, insumos_data in enumerate(insumos_data_list):
                col = 0  # Empezar en la primera columna
                row = index  # Fila en la que se encuentra el recuadro
                
                for key in headers:
                    # Convertir el encabezado a minúsculas para coincidir con las claves del diccionario
                    key = key.lower().replace(' de', '').replace(' ', '_')
                    
                    value = insumos_data.get(key, '')
                    
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