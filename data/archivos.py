import sqlite3
import conexion as con
from PyQt6 import QtWidgets

class ArchivosData():

    def __init__(self):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS archivos (
                    id_archivo INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_archivo TEXT NOT NULL,
                    contenido BLOB,
                    id_paciente INTEGER,
                    FOREIGN KEY (id_paciente) REFERENCES pacientes(id)  -- Ejemplo de clave foránea
                )
            ''')
            self.db.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla de archivos: {e}")
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
                INSERT INTO archivos (nombre_archivo, contenido, id_paciente)
                VALUES (?, ?, ?)
            ''', (nombre_archivo, contenido, id_paciente))
            self.db.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al guardar el archivo: {e}")
            return False
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def obtener_archivos_por_paciente(self, id_paciente):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute('''
                SELECT id_archivo, nombre_archivo, contenido
                FROM archivos
                WHERE id_paciente = ?
            ''', (id_paciente,))
            archivos = self.cursor.fetchall()
            return archivos
        except sqlite3.Error as e:
            print(f"Error al obtener archivos del paciente: {e}")
            return []
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()