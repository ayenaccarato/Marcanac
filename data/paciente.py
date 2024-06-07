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
            tipo TEXT,
            documento TEXT UNIQUE,
            fechaNacimiento DATETIME,
            sexo TEXT)"""
            
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
        INSERT INTO pacientes values(null, '{}', '{}', '{}', '{}', '{}', '{}')
        """.format(paciente._nombre, paciente._apellido, paciente._tipo, paciente._documento, paciente._fechaNacimiento, paciente._sexo))
        self.db.commit()
        if self.cursor.rowcount == 1: #Aca me devuelve cuantos elementos afecto
                return True
        else:
            return False
 
    