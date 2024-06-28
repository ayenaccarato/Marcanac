from datetime import datetime
import sqlite3
import conexion as con
from model.profesional import Profesional

class ProfesionalData():   

    def __init__(self):
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
            codTransf TEXT UNIQUE
            )"""
            
            self.cursor.execute(sql_create_profesionales)
            
            # Crea el trigger para verificar unicidad en cbu1 y cbu2
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
            self.cursor.close()
            self.db.close()
            
            print("Tabla Profesionales y trigger creados")
        except Exception as ex:
            print("Error al crear la tabla Profesionales o el trigger: ", ex)


    def registrar(self, profesional:Profesional): 
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute("""
            INSERT INTO profesionales values
            (null, '{}', '{}', '{}', '{}', '{}', 
            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
            """.format(profesional._nombre, profesional._apellido, profesional._domicilio,
                    profesional._localidad, profesional._CUIT, profesional._fechaNacimiento, 
                    profesional._codPostal, profesional._matricula, profesional._telefono, 
                    profesional._cbu1, profesional._cbu2, profesional._alias, profesional._mail, 
                    profesional._monotributo, profesional._coord, profesional._profesional, 
                    profesional._codTransf))
            
            
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
                coord = '{}', profesional = '{}', codTransf = '{}' 
                WHERE id = '{}'""".format(
                profesional._nombre, profesional._apellido, profesional._domicilio,
                profesional._localidad, profesional._CUIT, profesional._fechaNacimiento, 
                profesional._codPostal, profesional._matricula, profesional._telefono, 
                profesional._cbu1, profesional._cbu2, profesional._alias, profesional._mail, 
                profesional._monotributo, profesional._coord, profesional._profesional, 
                profesional._codTransf, id)

            self.cursor.execute(sql_update)
            self.db.commit()
            self.cursor.close()
            return True, ""
        except Exception as ex:
            return False, str(ex)

    def eliminar(self):
         pass