from datetime import datetime
import conexion as con
from model.paciente import Paciente

class PacienteData():   

    def __init__(self):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            sql_create_pacientes = """ CREATE TABLE IF NOT EXISTS pacientes
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
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
            activo BOOLEAN,
            familiar TEXT,
            modulo TEXT,
            submodulo TEXT,
            equip TEXT,
            sopNutri TEXT,
            asisRespi TEXT
            )"""
            
            self.cursor.execute(sql_create_pacientes)
            self.db.commit()
            self.cursor.close() 
            self.db.close()           
            print("Tabla Pacientes creada")
        except Exception as ex:
            print("Tabla Pacientes OK: ", ex)

    def registrar(self, paciente:Paciente): 
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()
        self.cursor.execute("""
        INSERT INTO pacientes values
        (null, '{}', '{}', '{}', '{}', '{}', 
        '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
        """.format(paciente._nombre, paciente._apellido, paciente._domicilio,
                paciente._localidad, paciente._documento, paciente._fechaNacimiento, 
                paciente._obraSocial, paciente._numAfiliado, paciente._telefono, 
                paciente._fechaIngreso, paciente._fechaEgreso, paciente._motivo, 
                paciente._activo, paciente._familiar, paciente._modulo, paciente._submodulo, 
                paciente._equip, paciente._sopNutri, paciente._asisRespi))
        self.db.commit()
        if self.cursor.rowcount == 1: #Aca me devuelve cuantos elementos afecto
                return True
        else:
            return False
        

    def mostrar(self, id):
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()
        sql_ver = """ SELECT * FROM pacientes p
            WHERE p.id = '{}'  
        """.format(id)

        self.cursor.execute(sql_ver)
        data = self.cursor.fetchone()
        
        self.cursor.close()

        return data

    def modificar(self, id, paciente):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()

            sql_update = """UPDATE pacientes SET 
                nombre = '{}', apellido = '{}', domicilio = '{}', localidad = '{}',
                documento = '{}', fechaNacimiento = '{}', obraSocial = '{}', numAfiliado = '{}', 
                telefono = '{}', fechaIngreso = '{}', fechaEgreso = '{}', motivo = '{}', activo = '{}', 
                familiar = '{}', modulo = '{}', submodulo = '{}', equip = '{}', 
                sopNutri = '{}', asisRespi = '{}'   
                WHERE id = '{}'""".format(
                paciente._nombre, paciente._apellido, paciente._domicilio,
                paciente._localidad, paciente._documento, paciente._fechaNacimiento, 
                paciente._obraSocial, paciente._numAfiliado, paciente._telefono, 
                paciente._fechaIngreso, paciente._fechaEgreso, paciente._motivo, 
                paciente._activo, paciente._familiar, paciente._modulo, paciente._submodulo, 
                paciente._equip, paciente._sopNutri, paciente._asisRespi, id)

            self.cursor.execute(sql_update)
            self.db.commit()
            self.cursor.close()
            return True, ""
        except Exception as ex:
            return False, str(ex)

    
    def eliminar(self):
         pass
 
    