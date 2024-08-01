import os
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox

from data.usuario import UsuarioData
from model.usuario import Usuario


class UsuarioWindow():  

    def __init__(self):
        #self.nuevo = uic.loadUi("gui/usuario/nuevo_usuario.ui")
        ui_file = os.path.join(os.path.dirname(__file__), '..', 'usuario', 'nuevo_usuario.ui')
        ui_file = os.path.abspath(ui_file)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file):
            print(f"Error: el archivo {ui_file} no se encuentra.")
            return
        self.nuevo = uic.loadUi(ui_file)
    
    # def __init__(self):
    #     try:
    #         ui_file = os.path.join(os.path.dirname(__file__), '..', 'gui', 'usuario', 'nuevo_usuario.ui')
    #         ui_file = os.path.abspath(ui_file)
            
    #         if not os.path.isfile(ui_file):
    #             raise FileNotFoundError(f"El archivo {ui_file} no se encuentra.")
            
    #         self.nuevo = uic.loadUi(ui_file)
    #         print("Archivo .ui cargado exitosamente.")
    #     except Exception as e:
    #         print(f"Error al cargar el archivo .ui: {e}")

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
                    
            #mBox = QMessageBox()
            if objData.crear_usuario(usuario=nuevoUsuario):   
                # mBox.setWindowTitle('Mensaje')             
                # mBox.setText("Usuario registrado")      
                QMessageBox.information(None, 'Mensaje', 'Usuario registrado')
                               
            else:
                #mBox.setWindowTitle('Error')
                #mBox.setText("El usuario no pudo ser registrado")
                QMessageBox.warning(None, 'Error', 'El usuario no pudo ser registrado')       
            #mBox.exec()
            self.nuevo.close() #Cierro la ventana