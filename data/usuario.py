import conexion as con
import bcrypt
from model.usuario import Usuario

class UsuarioData():   

    def __init__(self):
        self.db = None
        self.cursor = None

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
            print("cerre la base")
            # Verificar si el cursor y la conexión existen antes de cerrarlos
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
            print("cerre la base")

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
