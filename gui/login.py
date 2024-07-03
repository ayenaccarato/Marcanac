from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from data.usuario import UsuarioData
from gui.main import MainWindow
from model.usuario import Usuario

class Login():
    def __init__(self):
        self.login = uic.loadUi("gui/login.ui")
        self.initGUI()
       # self.login.lblMensaje.setText("")
        self.login.show()

    def ingresar(self):
        mBox = QMessageBox()
        if self.login.txtUsuario.text() == "":
            mBox.setText("Ingrese un usuario válido") 
            self.login.txtUsuario.setFocus() #Ubica el cursor en el campo usuario
        elif self.login.txtClave.text() == "":
            mBox.setText("Ingrese una contraseña válida") 
            self.login.txtClave.setFocus()
        else:
            #self.login.lblMensaje.setText("")
            usuario = Usuario(usuario=self.login.txtUsuario.text(), clave=self.login.txtClave.text())
            usData = UsuarioData()
            res = usData.login(usuario)
            if res:
                self.main = MainWindow()
                self.login.hide() #Oculta la ventana de login 
            else:
                
                mBox.setText("Datos incorrectos Vuelva a intentarlo") 

    def registrar(self):
        #hashed_password.decode('utf-8') para encriptar contraseñas
        pass

    def initGUI(self):
        self.login.btnAcceder.clicked.connect(self.ingresar)

