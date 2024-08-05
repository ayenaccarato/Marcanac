import sqlite3
import conexion as con
from data.paciente_insumo import PacienteInsumoData
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
            cantidad TEXT            
            )"""
            
            self.cursor.execute(sql_create_insumo)
            self.db.commit()
            self.cursor.close() 
            self.db.close()           
            print("Tabla Insumos creada")
        except Exception as ex:
            print("Tabla Insumos OK: ", ex)

    def registrar(self, insumo: Insumo, id_paciente):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()

            # Insertar el insumo en la tabla 'insumos'
            sql_insert_insumo = "INSERT INTO insumos (fechaEntrega, nombre, cantidad) VALUES (?, ?, ?)"
            self.cursor.execute(sql_insert_insumo, (insumo._fechaEntrega, insumo._nombre, insumo._cantidad))
            self.db.commit()

            # Obtener el ID del insumo recién insertado
            insumo_id = self.cursor.lastrowid

            # Asociar el insumo al paciente usando PacienteInsumoData
            objPacienteInsumoData = PacienteInsumoData()
            success = objPacienteInsumoData.asociar_insumo_a_paciente(id_paciente, insumo_id)

            if success:
                return True, None
            else:
                return False, "Error al asociar insumo a paciente"

        except sqlite3.Error as e:
            return False, str(e)

        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def mostrar(self, id):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            sql = """
            SELECT * 
            FROM insumos 
            JOIN paciente_insumo ON insumos.id = paciente_insumo.insumo_id 
            WHERE paciente_insumo.paciente_id = ?
            ORDER BY fechaEntrega
            """
            self.cursor.execute(sql, (id,))
            insumos = self.cursor.fetchall()
            return insumos
        except Exception as e:
            return []
        finally:
            self.cursor.close()
            self.db.close()

    def eliminar(self, id):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()

            # Eliminar insumo y sus relaciones en cascada
            self.cursor.execute('DELETE FROM pacientes WHERE id = ?', (id,))
            self.db.commit()
            print(f"Insumo con ID {id} y sus relaciones eliminados correctamente.")
            return True, ""
        except sqlite3.Error as ex:
            return False, str(ex)            
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()