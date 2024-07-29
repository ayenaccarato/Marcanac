from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt, QDate

from data.profesional import ProfesionalData
from gui.profesionales.archivos_profesional import ArchivosProfesionalWindow

class VerProfesionalWindow():

    def __init__(self):
        #self.verProf = uic.loadUi("gui/profesionales/ver_profesional.ui")
        pass

    # def mostrarProfesional(self, id):

    #     archivos = ArchivosProfesionalWindow()

    #     objData = ProfesionalData()
        
    #     profesional = objData.mostrar(id)

    #     self.verProf.txtNombre.setText(profesional[1])
    #     self.verProf.txtApellido.setText(profesional[2])
    #     self.verProf.txtDomicilio.setText(profesional[3])
    #     self.verProf.txtLocalidad.setText(profesional[4])
    #     self.verProf.txtCuit.setText(profesional[5])

    #     day, month, year = map(int, profesional[6].split("/"))
    #     date_qt = QDate(year, month, day)
    #     self.verProf.txtFechaN.setDate(date_qt)
        
    #     self.verProf.txtCP.setText(profesional[7])
    #     self.verProf.txtMatricula.setText(profesional[8])
    #     self.verProf.txtTelefono.setText(profesional[9])
    #     self.verProf.txtCbu1.setText(profesional[10])
    #     self.verProf.txtCbu2.setText(profesional[11])
    #     self.verProf.txtAlias.setText(profesional[12])
    #     self.verProf.txtMail.setText(profesional[13])
        
    #     self.verProf.monotributo.setChecked(profesional[14] == 'True')
    #     self.verProf.coordinador.setChecked(profesional[15] == 'True')
        
    #     self.verProf.cbProfesional.setCurrentText(profesional[16])
    #     self.verProf.cuidador.setChecked(profesional[17] == 'True'),
    #     self.verProf.txtCodigo.setText(profesional[18])
        
    #     ## Datos pago a terceros ##
    #     self.verProf.txtNombre_2.setText(profesional[19])
    #     self.verProf.txtApellido_2.setText(profesional[20])
    #     self.verProf.txtCuit_2.setText(profesional[21])
    #     self.verProf.txtCbu3.setText(profesional[22])

    #     self.verProf.btnModificar.clicked.connect(lambda: self.abrirVentanaModificar(id))
    #     self.verProf.btnCarpeta.clicked.connect(lambda: archivos.cargarArchivosProfesional(id_profesional=id))
    #     self.verProf.btnEliminar.clicked.connect(lambda: eliminar.eliminar_profesional(id))
        
    #     self.verProf.show()
        