from datetime import datetime
import random
import sqlite3
import conexion as con
from model.profesional import Profesional

class ProfesionalData():   

    init = False

    def __init__(self):
        if not ProfesionalData.init:
            try:
                self.db = con.Conexion().conectar()
                self.cursor = self.db.cursor()
                
                # Crea la tabla profesionales
                sql_create_profesionales = """ CREATE TABLE IF NOT EXISTS profesionales
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nombre TEXT, 
                apellido TEXT,
                domicilio TEXT,
                localidad TEXT,
                CUIT TEXT UNIQUE,
                fechaNacimiento DATETIME,
                codPostal TEXT,
                matricula TEXT UNIQUE,
                telefono TEXT,
                cbu1 TEXT UNIQUE,
                cbu2 TEXT UNIQUE,
                alias TEXT,
                mail TEXT,
                monotributo BOOLEAN,
                coord BOOLEAN,
                profesional TEXT,
                cuidador BOOLEAN,
                codTransf TEXT UNIQUE,
                nombre2 TEXT,
                apellido2 TEXT,
                CUIT2 TEXT,
                cbu3 TEXT
                )"""
                
                self.cursor.execute(sql_create_profesionales)
                
                # Crea el trigger para verificar unicidad y longitud de los campos cbu1 y cbu2, y solo longitud de cbu3
                sql_create_trigger = """
                CREATE TRIGGER IF NOT EXISTS unique_cbu_and_others
                BEFORE INSERT ON profesionales
                FOR EACH ROW
                BEGIN
                    -- Verificar unicidad de CUIT
                    SELECT CASE
                        WHEN EXISTS (SELECT 1 FROM profesionales WHERE CUIT = NEW.CUIT) THEN
                            RAISE(ABORT, 'CUIT ya existe')
                    END;
                    -- Verificar unicidad de cbu1
                    SELECT CASE
                        WHEN EXISTS (SELECT 1 FROM profesionales WHERE cbu1 = NEW.cbu1 OR cbu2 = NEW.cbu1) THEN
                            RAISE(ABORT, 'CBU1 ya existe')
                    END;
                    -- Verificar unicidad de cbu2
                    SELECT CASE
                        WHEN EXISTS (SELECT 1 FROM profesionales WHERE cbu1 = NEW.cbu2 OR cbu2 = NEW.cbu2) THEN
                            RAISE(ABORT, 'CBU2 ya existe')
                    END;
                    -- Verificar longitud de cbu1
                    SELECT CASE
                        WHEN LENGTH(NEW.cbu1) != 22 THEN
                            RAISE(ABORT, 'CBU1 debe tener 22 caracteres')
                    END;
                    -- Verificar longitud de cbu2
                    SELECT CASE
                        WHEN LENGTH(NEW.cbu2) != 22 THEN
                            RAISE(ABORT, 'CBU2 debe tener 22 caracteres')
                    END;
                    -- Verificar longitud de cbu3
                    SELECT CASE
                        WHEN LENGTH(NEW.cbu3) != 0 AND LENGTH(NEW.cbu3) != 22 THEN
                            RAISE(ABORT, 'CBU3 debe estar vacío o tener 22 caracteres')
                    END;
                    -- Verificar unicidad de matricula
                    SELECT CASE
                        WHEN EXISTS (SELECT 1 FROM profesionales WHERE matricula = NEW.matricula) THEN
                            RAISE(ABORT, 'Matricula ya existe')
                    END;
                    -- Verificar unicidad de codTransf
                    SELECT CASE
                        WHEN EXISTS (SELECT 1 FROM profesionales WHERE codTransf = NEW.codTransf) THEN
                            RAISE(ABORT, 'Codigo de transferencia ya existe')
                    END;
                END;
                """
                
                self.cursor.execute(sql_create_trigger)
                
                self.db.commit()
                print("Tabla Profesionales y trigger creados")
                self.crear_datos()
                ProfesionalData.init = True
            except Exception as ex:
                print("Error al crear la tabla Profesionales o el trigger: ", ex)
            finally:
                if hasattr(self, 'cursor') and self.cursor:
                    self.cursor.close()
                if hasattr(self, 'db') and self.db:
                    self.db.close()

    def crear_datos(self):
        try:
            # Verificar si ya hay datos en la tabla
            self.cursor.execute("SELECT COUNT(*) FROM profesionales")
            count = self.cursor.fetchone()[0]

            if count == 0:
                cuit = random.randint(1000, 9999)
                cbu = random.randint(1000000000000000000000, 9999999999999999999999)
                cod = random.randint(1, 200)
                matricula = random.randint(1000, 9999)
                
                sql_insert_profesionales = """INSERT INTO profesionales 
                    (nombre, apellido, domicilio, localidad, CUIT, fechaNacimiento, codPostal, matricula, telefono, cbu1, 
                    cbu2, alias, mail, monotributo, coord, profesional, cuidador, codTransf, nombre2, apellido2, CUIT2, cbu3)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                profesionales_datos = [
                    ("Juan", "Perez", "Calle Falsa 123", "Ciudad", str(cuit), "01/01/1980", "1900", str(matricula), "123456789", str(cbu), str(cbu+1), 
                     "alias", "mail", 'False', 'False', "Enfermero/a", 'True', str(cod), "", "", "", ""),
                    ("Juan", "Garcia", "Calle Falsa 123", "Ciudad", str(cuit+1), "01/01/1980", "1900", str(matricula+1), "123456789", str(cbu+2), str(cbu+3), 
                     "alias", "mail", 'False', 'True', "Enfermero/a", 'False', str(cod+1), "", "", "", ""),
                    
                ]

                try:
                    self.cursor.executemany(sql_insert_profesionales, profesionales_datos)
                    self.db.commit()
                    print("Profesionales: Datos de ejemplo insertados correctamente.")
                except sqlite3.IntegrityError as ie:
                    print("Error de integridad:", ie)
                except Exception as ex:
                    print("Error al insertar datos de ejemplo:", ex)
            else:
                print("Los datos de ejemplo ya están presentes en la base de datos.")

        except sqlite3.Error as e:
            print("Error al verificar datos:", e)


    def registrar(self, profesional:Profesional): 
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute("""
            INSERT INTO profesionales values
            (null, '{}', '{}', '{}', '{}', '{}', 
            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', 
                                '{}', '{}', '{}', '{}', '{}', '{}')
            """.format(profesional._nombre, profesional._apellido, profesional._domicilio,
                    profesional._localidad, profesional._CUIT, profesional._fechaNacimiento, 
                    profesional._codPostal, profesional._matricula, profesional._telefono, 
                    profesional._cbu1, profesional._cbu2, profesional._alias, profesional._mail, 
                    profesional._monotributo, profesional._coord, profesional._profesional, 
                    profesional._cuidador, profesional._codTransf, profesional._nombre2, 
                    profesional._apellido2, profesional._CUIT2, profesional._cbu3))
            
            self.db.commit()

            if self.cursor.rowcount == 1: # Si se afectó una fila
                return True, None
            else:
                return False, "No se pudo registrar el profesional"
        except sqlite3.IntegrityError as ex:
            return False, "Error de integridad: " + str(ex)
        except Exception as ex:
            return False, "Error: " + str(ex)
        finally:
            self.cursor.close()
            self.db.close()
        
    def mostrar(self, id):
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()
        sql_ver = """ SELECT * FROM profesionales p
            WHERE p.id = '{}'  
        """.format(id)

        self.cursor.execute(sql_ver)
        data = self.cursor.fetchone()
        
        self.cursor.close()

        return data

    def modificar(self, id, profesional):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()

            sql_update = """UPDATE profesionales SET 
                nombre = '{}', apellido = '{}', domicilio = '{}', localidad = '{}', CUIT = '{}', 
                fechaNacimiento = '{}', codPostal = '{}', matricula = '{}', telefono = '{}', 
                cbu1 = '{}', cbu2 = '{}', alias = '{}', mail = '{}', monotributo = '{}', 
                coord = '{}', profesional = '{}', cuidador = '{}', codTransf = '{}', nombre2 = '{}', apellido2 = '{}',
                CUIT2 = '{}', cbu3 = '{}' 
                WHERE id = '{}'""".format(
                profesional._nombre, profesional._apellido, profesional._domicilio,
                profesional._localidad, profesional._CUIT, profesional._fechaNacimiento, 
                profesional._codPostal, profesional._matricula, profesional._telefono, 
                profesional._cbu1, profesional._cbu2, profesional._alias, profesional._mail, 
                profesional._monotributo, profesional._coord, profesional._profesional, 
                profesional._cuidador, profesional._codTransf, profesional._nombre2, 
                profesional._apellido2, profesional._CUIT2, profesional._cbu3, id)

            self.cursor.execute(sql_update)
            self.db.commit()
            self.cursor.close()
            return True, ""
        except Exception as ex:
            return False, str(ex)

    def obtener_profesionales(self):
        profesionales = []
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute("SELECT id, nombre, apellido, profesional FROM profesionales")
            profesionales = self.cursor.fetchall()
            
            return profesionales  # Retorna la lista de tuplas (id, nombre, apellido)
        except sqlite3.Error as e:
            print(f"Error al obtener nombres de profesionales: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def obtener_coordinadores(self):
        profesionales = []
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute("""SELECT id, nombre, apellido
                                    FROM profesionales
                                    WHERE coord = 'True'""")
            profesionales = self.cursor.fetchall()
            
            return profesionales  # Retorna la lista de tuplas (id, nombre, apellido)
        except sqlite3.Error as e:
            print(f"Error al obtener nombres de profesionales: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def eliminar(self, id_profesional): 
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()

            # Eliminar profesionales y sus relaciones en cascada
            self.cursor.execute('DELETE FROM profesionales WHERE id = ?', (id_profesional,))
            self.db.commit()
            print(f"Profesional con ID {id_profesional} y sus relaciones eliminados correctamente.")
            return True, ""
        except sqlite3.Error as ex:
            return False, str(ex)            
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
    