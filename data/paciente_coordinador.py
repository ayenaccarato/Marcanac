import sqlite3
import conexion as con

class PacienteCoordinadorData:
    def __init__(self):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            sql_create_paciente_coordinador = """
            CREATE TABLE IF NOT EXISTS paciente_coordinador (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            coordinador_id INTEGER,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
            FOREIGN KEY (coordinador_id) REFERENCES profesionales(id),
            UNIQUE(paciente_id) ON DELETE CASCADE
            )"""
            self.cursor.execute(sql_create_paciente_coordinador)
            self.db.commit()
            self.cursor.close() 
            self.db.close()           
            print("Tabla paciente_coordinador creada")
        except Exception as ex:
            print("Error al crear la tabla paciente_coordinador: ", ex)
    
    def obtener_coordinador_de_paciente(self, paciente_id):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute("""
            SELECT p.id, p.nombre, p.apellido
            FROM paciente_coordinador pc
            JOIN profesionales p ON pc.coordinador_id = p.id
            WHERE pc.paciente_id = ?
            """, (paciente_id,))
            coordinador = self.cursor.fetchone()
            return coordinador
        except sqlite3.Error as e:
            print(f"Error al obtener coordinador del paciente: {e}")
            return None
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
    
    def asociar_coordinador_a_paciente(self, paciente_id, coordinador_id):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute("""
            INSERT INTO paciente_coordinador (paciente_id, coordinador_id)
            VALUES (?, ?)
            """, (paciente_id, coordinador_id))
            self.db.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al asociar coordinador a paciente: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
