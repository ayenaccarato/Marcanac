from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

from data.usuario import UsuarioData
from model.usuario import Usuario


class UsuarioWindow():  

    def __init__(self):
        self.nuevo = uic.loadUi("gui/usuario/nuevo_usuario.ui")

    def abrirRegistro(self): 
        self.nuevo.btnRegistrar.clicked.connect(self.registrar)     
        self.nuevo.show()

    def registrar(self):        
        mBox = QMessageBox()
        if self.nuevo.cbRol.currentText() == "--Seleccione--":            
            mBox.setWindowTitle('Mensaje')
            mBox.setText("Seleccione un rol")
            mBox.exec()
        elif self.nuevo.txtUsuario.text() == "" or self.nuevo.txtClave.text() == "":            
            mBox.setWindowTitle('Mensaje')
            mBox.setText("Debe completar los campos")
            mBox.exec() 

        else:
            if self.nuevo.cbRol.currentText() == "Administrador":
                nRol = "admin"
            else:
                nRol = "employee"
                
            nuevoUsuario = Usuario(
                nombre = self.nuevo.txtNombre.text(),
                usuario = self.nuevo.txtUsuario.text(),
                clave = self.nuevo.txtClave.text(),                  
                rol = nRol   
            )

            objData = UsuarioData()
                    
            mBox = QMessageBox()
            if objData.crear_usuario(usuario=nuevoUsuario):   
                mBox.setWindowTitle('Mensaje')             
                mBox.setText("Usuario registrado")      
                               
            else:
                mBox.setWindowTitle('Error')
                mBox.setText("El usuario no pudo ser registrado")
                        
            mBox.exec()
            self.nuevo.close() #Cierro la ventana