import os

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from data.insumos import InsumoData
from data.paciente import PacienteData
from data.profesional import ProfesionalData
from gui.insumos.insumos import InsumosWindow
from gui.pacientes.paciente import PacienteWindow
from gui.profesionales.profesional import ProfesionalWindow
from gui.usuario.usuario import UsuarioWindow
from model.usuario import Usuario

class MainWindow():

    def __init__(self, user: Usuario):
        self.usuario = user #Obtengo el usuario logueado

        #Creo tablas
        
        # self.profesionales_data = ProfesionalData()
        # self.insumos_data = InsumoData()

        ui_file = os.path.join(os.path.dirname(__file__), '..', 'gui', 'main.ui')
        ui_file = os.path.abspath(ui_file)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file):
            print(f"Error: el archivo {ui_file} no se encuentra.")
            return
        self.main = uic.loadUi(ui_file)
        self.initGUI()
        self.main.show()    

    def initGUI(self):       

        # Eliminar la barra de título
        #self.main.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # Configurar la opacidad de la ventana
        self.main.setWindowOpacity(1.0)

        paciente = PacienteWindow(self.usuario)
               
        profesional = ProfesionalWindow(self.usuario)

        usuario = UsuarioWindow()

        #Botones del menú de main
        self.main.btnListado.clicked.connect(lambda: self.main.stackedWidget.setCurrentWidget(self.main.page_datos)) #Abro pagina de listados
        self.main.btnRegistrar.clicked.connect(lambda: self.main.stackedWidget.setCurrentWidget(self.main.page_registrar)) #Abro pagina de registros
        #Listados
        self.main.listPacientes.clicked.connect(lambda: paciente.abrirListado() )
        self.main.listProfesionales.clicked.connect(lambda: profesional.abrirListadoProfesionales())
        #Registros
        self.main.btnPaciente.clicked.connect(lambda: paciente.abrirRegistro())
        self.main.btnProfesional.clicked.connect(lambda: profesional.abrirRegistroProf())
        print(self.usuario.rol)
        if self.usuario.rol == 'admin':
            self.main.btnUsuario.clicked.connect(lambda: usuario.abrirRegistro())
        else:
            self.main.btnUsuario.setVisible(False)