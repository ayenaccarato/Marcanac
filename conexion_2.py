import psycopg2
import bcrypt

import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del entorno desde el archivo .env
#Clase para la bd postgresql
class Conexion:
    init = False

    def __init__(self):
        if not Conexion.init:
            self.db_params = {
                'dbname': os.getenv('DB_NAME'),
                'user': os.getenv('DB_USER'),
                'password': os.getenv('DB_PASSWORD'),
                'host': os.getenv('DB_HOST'),
                'port': os.getenv('DB_PORT')
            }

            try:
                self.con = psycopg2.connect(**self.db_params)
                self.con.autocommit = True  # Para que los cambios se guarden automáticamente
                print(f"Conectado a la base de datos en: {self.db_params['host']}")

                self.crearTablas()
                self.crearAdmin()

                Conexion.init = True  # Establece init en True después de la inicialización
            except psycopg2.Error as ex:
                print("Error en la conexión:", ex)
            except Exception as ex:
                print("Error inesperado:", ex)
            finally:
                if hasattr(self, 'con') and self.con:
                    self.con.close()
                    print("Conexión a la base de datos cerrada.")

    def conectar(self):
        try:
            return psycopg2.connect(**self.db_params)
        except psycopg2.Error as ex:
            print("Error al conectar a la base de datos:", ex)
            return None

    def crearTablas(self):
        try:
            sql_create_table1 = """CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY, 
                nombre TEXT,
                usuario TEXT UNIQUE,
                clave TEXT,
                rol TEXT
            )"""
            with self.con.cursor() as cur:
                cur.execute(sql_create_table1)
                print("Tabla 'usuarios' creada o ya existe.")
        except Exception as ex:
            print("Error al crear la tabla:", ex)

    def crearAdmin(self):
        try:
            hashed_password = bcrypt.hashpw("12345".encode('utf-8'), bcrypt.gensalt())
            sql_insert = """INSERT INTO usuarios (nombre, usuario, clave, rol) VALUES (%s, %s, %s, %s);"""
            with self.con.cursor() as cur:
                cur.execute(sql_insert, ("Administrador", "admin", hashed_password.decode('utf-8'), "admin"))
                print("Usuario 'admin' creado correctamente.")
        except psycopg2.IntegrityError as ie:
            print("Error de integridad:", ie)
        except Exception as ex:
            print("Error al crear el administrador:", ex)

# Crear una instancia de la clase Conexion y crear el usuario admin
if not Conexion.init:
    con = Conexion()

# Verificar si el usuario 'admin' se creó correctamente
try:
    db = con.conectar()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
        admin_user = cur.fetchone()
        if admin_user:
            print("Usuario 'admin' verificado en la base de datos:", admin_user)
        else:
            print("Usuario 'admin' no encontrado en la base de datos.")
except Exception as ex:
    print("Error al verificar el usuario 'admin':", ex)
finally:
    if db:
        db.close()