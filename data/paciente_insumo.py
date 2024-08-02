import sqlite3
import conexion as con

class PacienteInsumoData:

    def __init__(self):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            sql_create_paciente_insumo = """
            CREATE TABLE IF NOT EXISTS paciente_insumo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER,
                insumo_id INTEGER,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
                FOREIGN KEY (insumo_id) REFERENCES insumos(id) ON DELETE CASCADE,
                UNIQUE(paciente_id, insumo_id)
            )
            """
            self.cursor.execute(sql_create_paciente_insumo)
            self.db.commit()
            self.cursor.close() 
            self.db.close()           
            print("Tabla paciente_insumo creada")
        except Exception as ex:
            print("Error al crear la tabla paciente_insumo: ", ex)
    

    def asociar_insumo_a_paciente(self, paciente_id, insumo_id):
        try:
            # Abrimos la conexión y creamos el cursor dentro del método
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            sql_insert_paciente_insumo = "INSERT INTO paciente_insumo (paciente_id, insumo_id) VALUES (?, ?)"
            self.cursor.execute(sql_insert_paciente_insumo, (paciente_id, insumo_id))
            self.db.commit()
            print("Asociación paciente-insumo creada correctamente")
            return True
        except sqlite3.Error as e:
            print(f"Error al asociar insumo a paciente: {e}")
            return False
        finally:
            # Cerramos el cursor y la conexión en el bloque finally
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def obtener_insumos_de_paciente(self, paciente_id):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute("""
            SELECT insumos.*
            FROM paciente_insumo
            JOIN insumos ON paciente_insumo.insumo_id = insumos.id
            WHERE paciente_insumo.paciente_id = ?
            """, (paciente_id,))
            insumos = self.cursor.fetchall()
            return insumos
        except sqlite3.Error as e:
            print(f"Error al obtener insumos del paciente: {e}")
            return []


    def eliminar_relacion_paciente_insumo(self, paciente_id, insumo_id):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute('''
                DELETE FROM paciente_insumo
                WHERE paciente_id = ? AND insumo_id = ?
            ''', (paciente_id, insumo_id))
            self.db.commit()
        except sqlite3.Error as e:
            print(f"Error al eliminar la relación: {e}")
        finally:
            if self.db:
                self.db.close()
