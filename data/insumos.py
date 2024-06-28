from datetime import datetime
import sqlite3
import conexion as con
from model.insumo import Insumo

class InsumoData():   

    def __init__(self):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            sql_create_insumo = """ CREATE TABLE IF NOT EXISTS insumos
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            fechaEntrega DATETIME,
            nombre TEXT, 
            cantidad TEXT,
            paciente INTEGER            
            )"""
            
            self.cursor.execute(sql_create_insumo)
            self.db.commit()
            self.cursor.close() 
            self.db.close()           
            print("Tabla Insumos creada")
        except Exception as ex:
            print("Tabla Insumos OK: ", ex)

    def registrar(self, insumo:Insumo): 
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute("""
                INSERT INTO insumos values (null, '{}', '{}', '{}', '{}')
            """.format(insumo._fechaEntrega, insumo._nombre, insumo._cantidad, insumo._paciente))
            self.db.commit()
            if self.cursor.rowcount == 1:  # Asegurarse de que una fila fue insertada
                return True, ""
            else:
                return False, "No se pudo insertar el insumo."
        except sqlite3.Error as e:
            return False, str(e)
        

    def mostrar(self, id):
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()
        sql_ver = """ SELECT * FROM insumos i
            WHERE i.paciente = '{}'  
        """.format(id)

        self.cursor.execute(sql_ver)
        data = self.cursor.fetchall()
        
        self.cursor.close()

        return data