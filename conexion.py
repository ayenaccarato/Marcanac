import sqlite3
import os
import sys
import bcrypt



class Conexion:
    init = False

    def __init__(self):
        # Siempre establece db_path
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(__file__)

        self.db_path = os.path.join(base_path, 'marcanac.bd')
        
        print(f"Ruta de la base de datos: {self.db_path}")

        # Solo ejecuta estas operaciones una vez
        if not Conexion.init:
            try:
                self.con = sqlite3.connect(self.db_path, timeout=10)  # Configura el timeout
                print(f"Conectado a la base de datos en: {self.db_path}")

                self.crearTablas()
                self.crearAdmin()

                Conexion.init = True  # Establece init en True después de la inicialización
            except sqlite3.Error as ex:
                print("Error en la conexión:", ex)
            except Exception as ex:
                print("Error inesperado:", ex)
            finally:
                if hasattr(self, 'con'):
                    self.con.close()
                    print("Conexión a la base de datos cerrada.")
        else:
            print("La inicialización ya se ha realizado.")

    def crearTablas(self):
        try:
            sql_create_table1 = """CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nombre TEXT,
                usuario TEXT UNIQUE,
                clave TEXT,
                rol TEXT
            )"""
            cur = self.con.cursor()
            cur.execute(sql_create_table1)
            cur.close()
            print("Tabla 'usuarios' creada o ya existe.")
        except Exception as ex:
            print("Error al crear la tabla:", ex)

    def crearAdmin(self):
        try:
            hashed_password = bcrypt.hashpw("12345".encode('utf-8'), bcrypt.gensalt())
            sql_insert = """INSERT INTO usuarios (nombre, usuario, clave, rol) VALUES (?, ?, ?, ?);"""
            cur = self.con.cursor()
            cur.execute(sql_insert, ("Administrador", "admin", hashed_password.decode('utf-8'), "admin"))
            self.con.commit()
            cur.close()
            print("Usuario 'admin' creado correctamente.")        
        except sqlite3.IntegrityError as ie:
            print("Error de integridad:", ie)
        except Exception as ex:
            print("Error al crear el administrador:", ex)

    def conectar(self):
        return sqlite3.connect(self.db_path, timeout=10)  # Crear una nueva conexión

# Crear una instancia de la clase Conexion y crear el usuario admin
if not Conexion.init:
    con = Conexion()

# Verificar si el usuario 'admin' se creó correctamente
try:
    db = con.conectar()
    cur = db.cursor()
    cur.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
    admin_user = cur.fetchone()
    cur.close()
    db.close()
    if admin_user:
        print("Usuario 'admin' verificado en la base de datos:", admin_user)
    else:
        print("Usuario 'admin' no encontrado en la base de datos.")
except Exception as ex:
    print("Error al verificar el usuario 'admin':", ex)