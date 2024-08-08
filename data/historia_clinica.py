import sqlite3
import conexion as con

class HistoriaClinicaData():

    def __init__(self):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS historia_clinica (
                    id_hc INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_archivo TEXT NOT NULL,
                    contenido BLOB,
                    id_paciente INTEGER,
                    FOREIGN KEY (id_paciente) REFERENCES pacientes(id) ON DELETE CASCADE  -- Eliminación en cascada
                )
            ''')
            self.db.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla de historia clinica: {e}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def guardar_archivo(self, nombre_archivo, contenido, id_paciente):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute('''
                INSERT INTO historia_clinica (nombre_archivo, contenido, id_paciente)
                VALUES (?, ?, ?)
            ''', (nombre_archivo, contenido, id_paciente))
            self.db.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al guardar el archivo hc: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def obtener_hc_por_paciente(self, id_paciente):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute('''
                SELECT id_hc, nombre_archivo, contenido
                FROM historia_clinica
                WHERE id_paciente = ?
            ''', (id_paciente,))
            archivos = self.cursor.fetchall()
            return archivos
        except sqlite3.Error as e:
            print(f"Error al obtener historia clinica del paciente: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def eliminar_hc(self, nombre_archivo, id_paciente):
        '''Elimina el archivo de la base de datos'''
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            # Ejecutar la consulta de eliminación
            self.cursor.execute("""
                DELETE FROM historia_clinica
                WHERE nombre_archivo = ? AND id_paciente = ?
            """, (nombre_archivo, id_paciente))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar el archivo hc: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()