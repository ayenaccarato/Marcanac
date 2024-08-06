import sqlite3
import conexion as con
import bcrypt
from model.usuario import Usuario
from PyQt6.QtWidgets import QMessageBox

class UsuarioData():   

    # def __init__(self):
    #     self.db = None
    #     self.cursor = None

    def login(self, usuario: Usuario):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute("SELECT * FROM usuarios WHERE usuario = ?;", (usuario._usuario,))
            data = self.cursor.fetchone()
            if data:
                clave_hash = data[3] 
                # Verificar la contraseña
                if bcrypt.checkpw(usuario._clave.encode('utf-8'), clave_hash.encode('utf-8')):
                    usuario_encontrado = Usuario(nombre=data[1], usuario=data[2], rol=data[4])
                    return usuario_encontrado
                else:
                    return None
            else:
                return None
        except Exception as ex:
            print(ex)
        finally:
            # Verificar si el cursor y la conexión existen antes de cerrarlos
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def crear_usuario(self, usuario: Usuario):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            hashed_password = bcrypt.hashpw(usuario._clave.encode('utf-8'), bcrypt.gensalt())
            sql_insert = """ INSERT INTO usuarios (nombre, usuario, clave, rol) VALUES (?, ?, ?, ?)"""
            self.cursor.execute(sql_insert, (usuario._nombre, usuario._usuario, hashed_password.decode('utf-8'), usuario._rol))
            self.db.commit()
            return True
        except Exception as ex:
            print(ex)
            return False
        finally:
            # Verificar si el cursor y la conexión existen antes de cerrarlos
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
    
    def obtener_usuarios(self):
        '''Retorno los usuarios'''
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()
        sql = """
            SELECT * FROM usuarios  
            ORDER BY nombre
        """
        res = self.cursor.execute(sql)
        data = res.fetchall() #Muestro todo lo que me devuelva
        return data
    
    def buscar_usuarios(self, rol, nombre, usuario): 
        '''Busco usuarios por distintos datos, dependiendo que se ingresa
        puede ser rol, nombre o usuario'''
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()

        # Crear el patrón de búsqueda para el apellido
        rol_busqueda = f'%{rol}%'
        nombre_busqueda = f'%{nombre}%'
        usuario_busqueda = f'%{usuario}%'

        sql = """
            SELECT * 
            FROM usuarios 
            WHERE (UPPER(rol) LIKE ? OR ? = '') 
            AND (UPPER(nombre) LIKE ? OR ? = '') 
            AND (UPPER(usuario) LIKE ? OR ? = '')
        """
        print(f"Consulta SQL: {sql}")
        print(f"Parámetros: {rol}, {nombre_busqueda}, {usuario_busqueda}")
        try:
            res = self.cursor.execute(sql, (rol_busqueda, rol, nombre_busqueda, nombre, usuario_busqueda, usuario))
        except Exception as e:
            QMessageBox.critical(None, 'Error', f'Error: {e}')
            print(e)
        data = res.fetchall() #Muestro todo lo que me devuelva
        return data
    
    def eliminar(self, id_usuario): 
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
                
            # Eliminar usuarios
            self.cursor.execute('DELETE FROM usuarios WHERE id = ?', (id_usuario,))
            self.db.commit()
            print(f"Usuario con ID {id_usuario} eliminado correctamente.")
            return True, ""
        except sqlite3.Error as ex:
            return False, str(ex)            
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
        
