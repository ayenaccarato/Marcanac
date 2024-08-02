import sqlite3
import conexion as con

class PacienteProfesionalesData:

    def __init__(self):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            sql_create_paciente_profesionales = """
            CREATE TABLE IF NOT EXISTS paciente_profesionales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            profesional_id INTEGER,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
            FOREIGN KEY (profesional_id) REFERENCES profesionales(id) ON DELETE CASCADE,
            UNIQUE(paciente_id, profesional_id)
        )
        """
            self.cursor.execute(sql_create_paciente_profesionales)
            self.db.commit()
            print("Tabla paciente_profesionales creada")
        except Exception as ex:
            print("Error al crear la tabla paciente_profesionales: ", ex)
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def asociar_profesional_a_paciente(self, paciente_id, profesional_id):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            sql_insert_paciente_profesional = "INSERT INTO paciente_profesionales (paciente_id, profesional_id) VALUES (?, ?)"
            self.cursor.execute(sql_insert_paciente_profesional, (paciente_id, profesional_id))
            self.db.commit()
            print("Asociación paciente-profesional creada correctamente")
            return True
        except sqlite3.Error as e:
            print(f"Error al asociar profesional a paciente: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def obtener_profesionales_de_paciente(self, paciente_id):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            sql_obtener_profesionales = """
            SELECT profesionales.*
            FROM paciente_profesionales
            JOIN profesionales ON paciente_profesionales.profesional_id = profesionales.id
            WHERE paciente_profesionales.paciente_id = ?
            """
            self.cursor.execute(sql_obtener_profesionales, (paciente_id,))
            profesionales = self.cursor.fetchall()
            return profesionales
        except sqlite3.Error as e:
            print(f"Error al obtener profesionales del paciente: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def obtener_pacientes_de_profesional(self, profesional_id):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            sql_obtener_pacientes = """
            SELECT pacientes.*
            FROM paciente_profesionales
            JOIN pacientes ON paciente_profesionales.paciente_id = pacientes.id
            WHERE paciente_profesionales.profesional_id = ?
            """
            self.cursor.execute(sql_obtener_pacientes, (profesional_id,))
            pacientes = self.cursor.fetchall()
            return pacientes
        except sqlite3.Error as e:
            print(f"Error al obtener pacientes del profesional: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def eliminar_relacion_paciente_profesional(self, paciente_id, profesional_id):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute('''
                DELETE FROM paciente_profesional
                WHERE paciente_id = ? AND profesional_id = ?
            ''', (paciente_id, profesional_id))
            self.db.commit()
        except sqlite3.Error as e:
            print(f"Error al eliminar la relación: {e}")
        finally:
            if self.db:
                self.db.close()
