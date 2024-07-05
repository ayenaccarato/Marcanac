import sqlite3
import conexion as con
from PyQt6 import QtWidgets

class ArchivosProfesionalData():

    def __init__(self):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS archivos_profesional (
                    id_archivo INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_archivo TEXT NOT NULL,
                    contenido BLOB,
                    id_profesional INTEGER,
                    FOREIGN KEY (id_profesional) REFERENCES profesionales(id)  -- Ejemplo de clave foránea
                )
            ''')
            self.db.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla de archivos_profesional: {e}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()

    def guardar_archivo(self, nombre_archivo, contenido, id_profesional):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute('''
                INSERT INTO archivos_profesional (nombre_archivo, contenido, id_profesional)
                VALUES (?, ?, ?)
            ''', (nombre_archivo, contenido, id_profesional))
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

    def obtener_archivos_por_profesional(self, id_profesional):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute('''
                SELECT id_archivo, nombre_archivo, contenido
                FROM archivos_profesional
                WHERE id_profesional = ?
            ''', (id_profesional,))
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