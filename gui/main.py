from PyQt6 import uic

from gui.insumos.insumos import InsumosWindow
from gui.pacientes.paciente import PacienteWindow
from gui.profesionales.profesional import ProfesionalWindow
from gui.usuario.usuario import UsuarioWindow
from model.usuario import Usuario

class MainWindow():

    def __init__(self, user: Usuario):
        self.usuario = user
        self.main = uic.loadUi("gui/main_2.ui")
        self.initGUI()
        self.main.show()
        #self.main.showMaximized()

        # self.main.btnRestaurar.hide() #Oculto boton         

        # self.main.btnMinimizar.clicked.connect(self.control_btnMinimizar) #Minimizo la pantalla
        # self.main.btnRestaurar.clicked.connect(self.control_btnNormal) #Vuelve a la normalidad
        # self.main.btnMaximizar.clicked.connect(self.control_btnMaximizar) #Maximizo la pagina
        # self.main.btnCerrar.clicked.connect(lambda:self.main.close()) #Cierro

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