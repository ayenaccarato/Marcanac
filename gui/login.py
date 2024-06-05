from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from data.usuario import UsuarioData
from model.usuario import Usuario

class Login():
    def __init__(self):
        self.login = uic.loadUi("gui/login.ui")
        self.initGUI()
        self.login.lblMensaje.setText("")
        self.login.show()

    def ingresar(self):
        if self.login.txtUsuario.text() == "":
            self.login.lblMensaje.setText("Ingrese un usuario válido")
            self.login.txtUsuario.setFocus() #Ubica el cursor en el campo usuario
        elif self.login.txtClave.text() == "":
            self.login.lblMensaje.setText("Ingrese una contraseña válida")
            self.login.txtClave.setFocus()
        else:
            self.login.lblMensaje.setText("")
            usuario = Usuario(usuario=self.login.txtUsuario.text(), clave=self.login.txtClave.text())
            usData = UsuarioData()
            res = usData.login(usuario)
            if res:
               self.login.lblMensaje.setText("Login correcto")
            else:
                self.login.lblMensaje.setText("Datos de acceso incorrectos")

    def initGUI(self):
        self.login.btnAcceder.clicked.connect(self.ingresar)

