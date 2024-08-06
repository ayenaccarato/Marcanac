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
            FOREIGN KEY (coordinador_id) REFERENCES profesionales(id) ON DELETE CASCADE,
            UNIQUE(paciente_id) 
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

            # # Primero, verificar si ya existe una asociación para el paciente
            # sql_check = "SELECT * FROM paciente_coordinador WHERE paciente_id = ?"
            # self.cursor.execute(sql_check, (paciente_id,))
            # association_exists = self.cursor.fetchone()

            # if association_exists:
            #     # Si existe una asociación, puedes decidir si actualizar o lanzar un error
            #     print(f"El paciente con ID {paciente_id} ya tiene un coordinador asignado.")
            #     return False

            self.cursor.execute("""
            INSERT INTO paciente_coordinador (paciente_id, coordinador_id)
            VALUES (?, ?)
            """, (paciente_id, coordinador_id))
            self.db.commit()
            if self.cursor.rowcount == 1: # Si se afectó una fila
                return True, None
            else:
                return False, "No se pudo registrar el profesional"
        except sqlite3.Error as e:
            return False, "Error de integridad: " + str(e)
        except Exception as ex:
            return False, "Error: " + str(ex)
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def eliminar_relacion(self, paciente_id):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()

            # Eliminar cualquier relación existente
            self.cursor.execute("""
                DELETE FROM paciente_coordinador
                WHERE paciente_id = ?
            """, (paciente_id,))
            
            self.db.commit()
            print("Relación eliminada correctamente.")
        
        except sqlite3.Error as ex:
            return False, "Error al eliminar la relación  " + str(ex)
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
            

        
