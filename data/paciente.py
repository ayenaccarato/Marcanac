import random
import sqlite3
import conexion as con
from model.paciente import Paciente

### PostgreSQL ###
# import psycopg2
# from psycopg2 import sql
# import conexion as con

# class PacienteData:

#     init = False

#     def __init__(self):
#         if not PacienteData.init:
#             try:
#                 self.conn = con.Conexion()  # Usa la instancia de Conexion
#                 self.db = self.conn.conectar()
#                 self.cursor = self.db.cursor()

#                 # Consulta SQL para crear la tabla
#                 sql_create_pacientes = """ CREATE TABLE IF NOT EXISTS pacientes (
#                     id SERIAL PRIMARY KEY, 
#                     nombre VARCHAR(255), 
#                     apellido VARCHAR(255),
#                     domicilio VARCHAR(255),
#                     localidad VARCHAR(255),
#                     documento VARCHAR(255) UNIQUE,
#                     fechaNacimiento TIMESTAMP,
#                     obraSocial VARCHAR(255),
#                     numAfiliado VARCHAR(255),
#                     telefono VARCHAR(255),
#                     fechaIngreso TIMESTAMP,
#                     fechaEgreso TIMESTAMP,
#                     motivo TEXT,
#                     familiar VARCHAR(255),
#                     parentesco VARCHAR(255),
#                     telFamiliar VARCHAR(255),
#                     modulo VARCHAR(255),
#                     submodulo VARCHAR(255),
#                     equip VARCHAR(255),
#                     sopNutri VARCHAR(255),
#                     asisRespi VARCHAR(255)
#                 ) """
#                 self.cursor.execute(sql_create_pacientes)
#                 self.db.commit()
#                 print("Tabla Pacientes creada")
#                 self.crear_datos()  # Solo creará datos si la tabla está vacía
#                 PacienteData.init = True
#             except psycopg2.Error as ex:
#                 print("Error al crear la tabla Pacientes:", ex)
#             except Exception as ex:
#                 print("Error inesperado al crear la tabla Pacientes:", ex)
#             finally:
#                 if hasattr(self, 'cursor') and self.cursor:
#                     self.cursor.close()
#                 if hasattr(self, 'db') and self.db:
#                     self.db.close()
class PacienteData:

    init = False

    def __init__(self):
        if not PacienteData.init:
            try:
                self.conn = con.Conexion()  # Usa la instancia de Conexion
                self.db = self.conn.conectar()
                self.cursor = self.db.cursor()

                sql_create_pacientes = """ CREATE TABLE IF NOT EXISTS pacientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    nombre TEXT, 
                    apellido TEXT,
                    domicilio TEXT,
                    localidad TEXT,
                    documento TEXT UNIQUE,
                    fechaNacimiento DATETIME,
                    obraSocial TEXT,
                    numAfiliado TEXT,
                    telefono TEXT,
                    fechaIngreso DATETIME,
                    fechaEgreso DATETIME,
                    motivo TEXT,
                    familiar TEXT,
                    parentesco TEXT,
                    telFamiliar TEXT,
                    modulo TEXT,
                    submodulo TEXT,
                    equip TEXT,
                    sopNutri TEXT,
                    asisRespi TEXT
                ) """
                self.cursor.execute(sql_create_pacientes)
                self.db.commit()
                print("Tabla Pacientes creada")
                self.crear_datos()  # Solo creará datos si la tabla está vacía
                PacienteData.init = True
            except sqlite3.Error as ex:
                print("Error al crear la tabla Pacientes:", ex)
            except Exception as ex:
                print("Error inesperado al crear la tabla Pacientes:", ex)
            finally:
                if hasattr(self, 'cursor') and self.cursor:
                    self.cursor.close()
                if hasattr(self, 'db') and self.db:
                    self.db.close()

    def crear_datos(self):
        try:
            # Verificar si ya hay datos en la tabla
            self.cursor.execute("SELECT COUNT(*) FROM pacientes")
            count = self.cursor.fetchone()[0]

            if count == 0:
                doc = random.randint(10000000, 99999999)
                sql_insert_pacientes = """INSERT INTO pacientes 
                    (nombre, apellido, domicilio, localidad, documento, fechaNacimiento, obraSocial, numAfiliado, telefono, fechaIngreso, 
                    fechaEgreso, motivo, familiar, parentesco, telFamiliar, modulo, submodulo, equip, sopNutri, asisRespi)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                pacientes_datos = [
                    ("Juan", "Perez", "Calle Falsa 123", "Ciudad", str(doc), "01/01/1980", "IOMA", "1111", "123456789", "01/01/2000", "", "", 
                     "Familiar 1", "Hijo", "2215968741", "Módulo 1", '{"Fono": false, "TO": false, "Psico": true}', '{"Cama": false, "Colchon": true, "Silla": false}', "Adultos SIN bomba", '{"A": false, "B": true, "C": false}'),
                    ("Juan", "Garcia", "Calle Falsa 124", "Ciudad", str(doc+1), "01/01/1980", "IOMA", "1111", "123456789", "01/01/2000", 
                     "01/01/2020", "Motivo 1", "Familiar 2", "Hijo", "2215369857","Modulo 2", '{"Fono": false, "TO": false, "Psico": true}', '{"Cama": false, "Colchon": true, "Silla": true}', "Adultos CON bomba", '{"A": false, "B": true, "C": true}'),
                    # Agrega más pacientes si es necesario
                ]
                try:
                    self.cursor.executemany(sql_insert_pacientes, pacientes_datos)
                    self.db.commit()
                    print("Pacientes: Datos de ejemplo insertados correctamente.")
                except sqlite3.IntegrityError as ie:
                    print("Error de integridad:", ie)
                except Exception as ex:
                    print("Error al insertar datos de ejemplo:", ex)
            else:
                print("Los datos de ejemplo ya están presentes en la base de datos.")

        except sqlite3.Error as e:
            print("Error al verificar datos:", e)

    def registrar(self, paciente:Paciente): 
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()

        # # Configura un tiempo de espera para los bloqueos
        # self.cursor.execute("PRAGMA busy_timeout = 3000")

        self.cursor.execute("""
        INSERT INTO pacientes values
        (null, '{}', '{}', '{}', '{}', '{}', 
        '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
        """.format(paciente._nombre, paciente._apellido, paciente._domicilio,
                paciente._localidad, paciente._documento, paciente._fechaNacimiento, 
                paciente._obraSocial, paciente._numAfiliado, paciente._telefono, 
                paciente._fechaIngreso, paciente._fechaEgreso, paciente._motivo, 
                paciente._familiar, paciente._parentesco, paciente._telFamiliar, paciente._modulo, paciente._submodulo, 
                paciente._equip, paciente._sopNutri, paciente._asisRespi))
        self.db.commit()
        if self.cursor.rowcount == 1: #Aca me devuelve cuantos elementos afecto
                return True
        else:
            return False
        
    def mostrar(self, id):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            sql_ver = """ SELECT * FROM pacientes p
                WHERE p.id = '{}'  
            """.format(id)

            self.cursor.execute(sql_ver)
            data = self.cursor.fetchone()
            
            self.cursor.close()
            return data
        except sqlite3.Error as ex:
            return True

    def modificar(self, id, paciente):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()

            sql_update = """UPDATE pacientes SET 
                nombre = '{}', apellido = '{}', domicilio = '{}', localidad = '{}',
                documento = '{}', fechaNacimiento = '{}', obraSocial = '{}', numAfiliado = '{}', 
                telefono = '{}', fechaIngreso = '{}', fechaEgreso = '{}', motivo = '{}',
                familiar = '{}', parentesco = '{}', telFamiliar = '{}', modulo = '{}', submodulo = '{}', equip = '{}', 
                sopNutri = '{}', asisRespi = '{}'   
                WHERE id = '{}'""".format(
                paciente._nombre, paciente._apellido, paciente._domicilio,
                paciente._localidad, paciente._documento, paciente._fechaNacimiento, 
                paciente._obraSocial, paciente._numAfiliado, paciente._telefono, 
                paciente._fechaIngreso, paciente._fechaEgreso, paciente._motivo, 
                paciente._familiar, paciente._parentesco, paciente._telFamiliar, 
                paciente._modulo, paciente._submodulo, paciente._equip, 
                paciente._sopNutri, paciente._asisRespi, id)

            self.cursor.execute(sql_update)
            self.db.commit()
            self.cursor.close()
            return True, ""
        except Exception as ex:
            return False, str(ex)

    def eliminar(self, id_paciente): 
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()

            # Eliminar paciente y sus relaciones en cascada
            self.cursor.execute('DELETE FROM pacientes WHERE id = ?', (id_paciente,))
            self.db.commit()
            print(f"Paciente con ID {id_paciente} y sus relaciones eliminados correctamente.")
            return True, ""
        except sqlite3.Error as ex:
            return False, str(ex)            
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def obtener_pacientes(self):
        pacientes = []
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute("SELECT id, nombre, apellido FROM pacientes")
            pacientes = self.cursor.fetchall()
            
            return pacientes  # Retorna la lista de tuplas (id, nombre, apellido)
        except sqlite3.Error as e:
            print(f"Error al obtener nombres de pacientes: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
    
 
    