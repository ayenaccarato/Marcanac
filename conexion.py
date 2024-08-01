import sqlite3
import os
import sys
import bcrypt

class Conexion:
    
    def __init__(self):
        try:
            self.db = None
            self.cur = None
            if getattr(sys, 'frozen', False):
                base_path = os.path.dirname(sys.executable)
            else:
                base_path = os.path.dirname(__file__)

            db_path = os.path.join(base_path, 'marcanac.bd')

            # Imprimir la ruta para depuración
            print(f"Ruta de la base de datos: {db_path}")

            self.db = sqlite3.connect(db_path, timeout=10)  # Configura el timeout
            self.cur = self.db.cursor()
            print(f"Conectado a la base de datos en: {db_path}")

            self.crearTablas()
        except sqlite3.Error as ex:
            print("Error en la conexión:", ex)
        except Exception as ex:
            print("Error inesperado:", ex)

    def crearTablas(self):
        try:
            sql_create_table1 = """CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nombre TEXT,
                usuario TEXT UNIQUE,
                clave TEXT,
                rol TEXT
            )"""
            print("aca entro")
            cur = self.db.cursor()
            print("aca entro1")
            cur.execute(sql_create_table1)
            print("aca entro2")
            cur.close()
        
            print("Tabla 'usuarios' creada o ya existe.")
        except Exception as ex:
            print("Error al crear la tabla:", ex)

    def crearAdmin(self):
        try:
            hashed_password = bcrypt.hashpw("12345".encode('utf-8'), bcrypt.gensalt())
            sql_insert = """INSERT INTO usuarios (nombre, usuario, clave, rol) VALUES (?, ?, ?, ?);"""
            cur = self.db.cursor()
            cur.execute(sql_insert, ("Administrador", "admin", hashed_password.decode('utf-8'), "admin"))
            self.db.commit()
            cur.close()
            
            print("Usuario 'admin' creado correctamente.")        
        except sqlite3.IntegrityError as ie:
            print("Error de integridad:", ie)
        except Exception as ex:
            print("Error al crear el administrador:", ex)

    def conectar(self):
        return self.db

# Crear una instancia de la clase Conexion y crear el usuario admin

# con = Conexion()
# con.crearAdmin()

# # Verificar si el usuario 'admin' se creó correctamente
# try:
#     cur = con.con.cursor()
#     cur.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
#     admin_user = cur.fetchone()
#     cur.close()
#     if admin_user:
#         print("Usuario 'admin' verificado en la base de datos:", admin_user)
#     else:
#         print("Usuario 'admin' no encontrado en la base de datos.")
# except Exception as ex:
#     print("Error al verificar el usuario 'admin':", ex)