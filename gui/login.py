import os

from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
from data.usuario import UsuarioData
from gui.main import MainWindow
from model.usuario import Usuario

class Login():

    def __init__(self):
        #ui_file = os.path.join('gui', 'login.ui')
        # Obtén la ruta del archivo UI en relación con el archivo actual
        ui_file = os.path.join(os.path.dirname(__file__), '..', 'gui', 'login.ui')
        ui_file = os.path.abspath(ui_file)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file):
            print(f"Error: el archivo {ui_file} no se encuentra.")
            return
        self.login = uic.loadUi(ui_file)
        self.initGUI()
        self.login.show()


    def ingresar(self):
        try:
            if self.login.txtUsuario.text() == "":
                QMessageBox.warning(None, "Error de ingreso", "Ingrese un usuario válido")
                self.login.txtUsuario.setFocus()  # Ubica el cursor en el campo usuario
                return  # Sale del método después de mostrar el mensaje
            
            if self.login.txtClave.text() == "":
                QMessageBox.warning(None, "Error de ingreso", "Ingrese una contraseña válida")
                self.login.txtClave.setFocus()
                return  # Sale del método después de mostrar el mensaje
            
            # Intentar autenticación
            usuario = Usuario(usuario=self.login.txtUsuario.text(), clave=self.login.txtClave.text())
            usData = UsuarioData()
            res = usData.login(usuario)
            print("Resultado de la autenticación:", res)  # Mensaje de depuración

            if res:
                usuario = res  # Actualizar usuario con nombre y rol obtenidos
                self.main = MainWindow(usuario)  # Puedes pasar el usuario a la ventana principal si es necesario
                #try:
                #    self.main.show()  # Mostrar la ventana principal
                #except Exception as e:
                #     QMessageBox.critical(None, "Error", f"Error pla: {e}")
                self.login.hide()  # Oculta la ventana de login 
            else:
                QMessageBox.warning(None, "Error de autenticación", "Datos incorrectos. Vuelva a intentarlo.")
        
        except Exception as e:
            print(f"Error al intentar ingresar: {e}")
            QMessageBox.critical(None, "Error", f"Error inesperado: {e}")

    def initGUI(self):
        self.login.btnAcceder.clicked.connect(self.ingresar)

