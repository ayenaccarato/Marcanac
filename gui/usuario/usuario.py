import os
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QWidget, QPushButton, QHBoxLayout

from data.usuario import UsuarioData
from model.usuario import Usuario


class UsuarioWindow():  

    def __init__(self, user):
        self.usuario = user
        #Carga UI de nuevo usuario
        ui_file = os.path.join(os.path.dirname(__file__), '..', 'usuario', 'nuevo_usuario.ui')
        ui_file = os.path.abspath(ui_file)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file):
            print(f"Error: el archivo {ui_file} no se encuentra.")
            return
        self.nuevo = uic.loadUi(ui_file)

        #Carga UI del listado de usuarios
        ui_file_lis = os.path.join(os.path.dirname(__file__), '..', 'usuario', 'listado_usuarios.ui')
        ui_file_lis = os.path.abspath(ui_file_lis)  # Convierte a ruta absoluta
        if not os.path.isfile(ui_file_lis):
            print(f"Error: el archivo {ui_file_lis} no se encuentra.")
            return
        self.listado = uic.loadUi(ui_file_lis)

### Registro ###
    def abrirRegistro(self): 
        self.nuevo.btnRegistrar.clicked.connect(self.registrar)     
        self.nuevo.show()

    def registrar(self):        
        if self.nuevo.cbRol.currentText() == "--Seleccione--":   
            QMessageBox.information(None, 'Mensaje', 'Seleccione un rol')         
        elif self.nuevo.txtUsuario.text() == "" or self.nuevo.txtClave.text() == "":   
            QMessageBox.warning(None, 'Error', 'Debe completar los campos')         

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

            if objData.crear_usuario(usuario=nuevoUsuario):      
                QMessageBox.information(None, 'Mensaje', 'Usuario registrado')
                               
            else:
                QMessageBox.warning(None, 'Error', 'El usuario no pudo ser registrado')       

            self.nuevo.close() #Cierro la ventana

### Eliminar ###

    def eliminarUsuario(self, id):
        if id == 1:
            QMessageBox.critical(None, 'Error', 'No puede eliminar este usuario')
        else:
            # Crear el cuadro de diálogo de confirmación
            mBox = QMessageBox()
            mBox.setWindowTitle('Confirmar eliminación')
            mBox.setText("¿Está seguro que desea eliminar este usuario?")

            # Añadir botones personalizados
            si_btn = mBox.addButton("Sí", QMessageBox.ButtonRole.YesRole)
            no_btn = mBox.addButton("No", QMessageBox.ButtonRole.NoRole)
            
            mBox.setDefaultButton(no_btn)
            mBox.exec()

            if mBox.clickedButton() == si_btn:
                self.confirmar(id)
            else:
                print("Eliminación cancelada")

    def confirmar(self, id):
        '''Se elimina el profesional, si confirman'''
        usuario = UsuarioData()
        eliminado = usuario.eliminar(id)

        if eliminado:
            QMessageBox.information(None, 'Mensaje', 'Paciente eliminado')    
        else:
            QMessageBox.critical(None, 'Error', 'El paciente no pudo ser eliminado')
        
        self.listado_usuarios()
### Listado ###

    def boton_listado_usuario(self, id_valor, fila):              
        # Crear el botón y añadirlo a la columna 7
        # Crear el botón "Ver más" y conectarlo
        btn = QPushButton("Eliminar")
        
        btn.clicked.connect(lambda _, id_valor=id_valor: self.eliminarUsuario(id_valor))
        # Agregar estilo al botón
        btn.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(btn)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
       
        self.listado.tblListado.setCellWidget(fila, 3, widget)

    def limpiar_campos_busqueda(self):        
        self.listado.txtNombre.clear()  # Limpia el contenido del primer QLineEdit
        self.listado.txtUsuario.clear()
        self.listado.cbRol.setCurrentIndex(0)

    def listado_usuarios(self):
        lis = UsuarioData() 
        data = lis.obtener_usuarios()    
        fila = 0
        self.listado.tblListado.setRowCount(len(data)) #Cuantas filas traen los datos
        for item in data:
            self.listado.tblListado.setItem(fila, 0, QTableWidgetItem(str(item[1]))) #Nombre
            self.listado.tblListado.setItem(fila, 1, QTableWidgetItem(str(item[2]))) #Usuario
            if item[4] == 'admin':
                self.listado.tblListado.setItem(fila, 2, QTableWidgetItem('Administrador')) #Rol
            else:
                self.listado.tblListado.setItem(fila, 2, QTableWidgetItem('Empleado'))
           

            id_valor = item[0]
            
            self.boton_listado_usuario(id_valor, fila)

            fila += 1
 
        self.listado.tblListado.setColumnWidth(0,150)
        self.listado.tblListado.setColumnWidth(1,150)
        try:
            self.listado.btnBuscar.clicked.disconnect()
        except TypeError:
            pass
        self.listado.btnBuscar.clicked.connect(lambda: self.buscar())
        self.listado.btnLista.setVisible(False)
        self.limpiar_campos_busqueda()   
        self.listado.show()

    def buscar(self):
        if self.listado.txtNombre.text() == '' and self.listado.txtUsuario.text() == '' and self.listado.cbRol.currentText() == '--Seleccione--':
            QMessageBox.information(None, 'Mensaje', 'Ingrese datos a buscar')
        else:
            # Limpiar el contenido actual de la tabla
            self.listado.tblListado.clearContents()
            self.listado.tblListado.setRowCount(0)
            lis = UsuarioData() 
            if self.listado.cbRol.currentText() == 'Administrador':
                rol = 'admin'
            elif self.listado.cbRol.currentText() == 'Empleado':
                rol = 'employee'
            else:
                rol = ''

            print('Rol', rol, ' nombre ', self.listado.txtNombre.text().upper(), ' usuario ', self.listado.txtUsuario.text().upper())
            data = lis.buscar_usuarios(rol.upper(), self.listado.txtNombre.text().upper(), self.listado.txtUsuario.text().upper())
            
            if data:
                # Reiniciar número de filas
                print('busqueda', data)
                fila = 0
                self.listado.tblListado.setRowCount(len(data)) #Cuantas filas traen los datos
                for item in data:
                    self.listado.tblListado.setItem(fila, 0, QTableWidgetItem(str(item[1]))) #Nombre
                    self.listado.tblListado.setItem(fila, 1, QTableWidgetItem(str(item[2]))) #Usuario
                    if item[4] == 'admin':
                        self.listado.tblListado.setItem(fila, 2, QTableWidgetItem('Administrador')) #Rol
                    else:
                        self.listado.tblListado.setItem(fila, 2, QTableWidgetItem('Empleado'))
                    
                    id_valor = item[0]
                    
                    self.boton_listado_usuario(id_valor, fila)
                            
                    fila += 1
            else:
                # Limpiar la tabla si no se encontraron resultados
                self.listado.tblListado.clearContents()
                self.listado.tblListado.setRowCount(0)

            self.listado.btnLista.setVisible(True)
            self.listado.btnLista.clicked.connect(lambda: self.listado_usuarios())