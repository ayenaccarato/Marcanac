import os

from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from data.usuario import UsuarioData
from gui.main import MainWindow
from model.usuario import Usuario

class Login():

    def __init__(self):
        ui_file = os.path.join('gui', 'login.ui')
        self.login = uic.loadUi(ui_file)
        self.initGUI()
        self.login.show()

    def ingresar(self):
        mBox = QMessageBox()
        if self.login.txtUsuario.text() == "":
            mBox.setWindowTitle("Error de ingreso")
            mBox.setText("Ingrese un usuario válido") 
            self.login.txtUsuario.setFocus() # Ubica el cursor en el campo usuario
            mBox.exec()
        elif self.login.txtClave.text() == "":
            mBox.setWindowTitle("Error de ingreso")
            mBox.setText("Ingrese una contraseña válida") 
            self.login.txtClave.setFocus()
            mBox.exec()
        else:
            # Intentar autenticación
            usuario = Usuario(usuario=self.login.txtUsuario.text(), clave=self.login.txtClave.text())
            usData = UsuarioData()
            res = usData.login(usuario)
            print(res)
            if res:
                usuario = res  # Actualizar usuario con nombre y rol obtenidos
                self.main = MainWindow(usuario)  # Puedes pasar el usuario a la ventana principal si es necesario
                #self.main  # Mostrar la ventana principal
                self.login.hide() # Oculta la ventana de login 
            else:
                mBox.setWindowTitle("Error de autenticación")
                mBox.setText("Datos incorrectos. Vuelva a intentarlo.")
                mBox.exec()

    def initGUI(self):
        self.login.btnAcceder.clicked.connect(self.ingresar)

