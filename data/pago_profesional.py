import sqlite3
import conexion as con
from model.pago import PagoProfesional

class PagoProfesionalData():

    init = False

    def __init__(self):
        if not PagoProfesionalData.init:
            try:
                self.conn = con.Conexion()  # Usa la instancia de Conexion
                self.db = self.conn.conectar()
                self.cursor = self.db.cursor()

                sql_create_pagos = """ CREATE TABLE IF NOT EXISTS pagos_profesionales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profesional_id INTEGER,
                    fecha_pago TEXT,
                    FOREIGN KEY (profesional_id) REFERENCES profesionales(id) ON DELETE CASCADE
                ) """
                self.cursor.execute(sql_create_pagos)
                self.db.commit()
                print("Tabla Pagos profesionales creada")
                #self.crear_datos()  # Solo creará datos si la tabla está vacía
                PagoProfesionalData.init = True
            except sqlite3.Error as ex:
                print("Error al crear la tabla Pagos profesionales:", ex)
            except Exception as ex:
                print("Error inesperado al crear la tabla Pagos profesionales:", ex)
            finally:
                if hasattr(self, 'cursor') and self.cursor:
                    self.cursor.close()
                if hasattr(self, 'db') and self.db:
                    self.db.close()

    def registrar_pago(self, pago): 
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()

            sql = """
                INSERT INTO pagos_profesionales (profesional_id, fecha_pago)
                VALUES (?, ?)
            """
            self.cursor.execute(sql, (pago.profesional_id, pago.fecha_pago))
            self.db.commit()
            return True, None
        except sqlite3.Error as e:
            return False, str(e)
        finally:
            self.cursor.close()
            self.db.close()
        
    def obtener_pagos(self):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            sql = """
                SELECT * 
                FROM pagos_profesionales
            """
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            return []
        finally:
            self.cursor.close()
            self.db.close()
        
    def obtener_pagos_profesional(self,  mes):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            
            sql = """
                SELECT * 
                FROM pagos_profesionales 
                WHERE strftime('%m', substr(fecha_pago, 7, 4) || '-' || substr(fecha_pago, 4, 2) || '-' || substr(fecha_pago, 1, 2)) = ?
                ORDER BY fecha_pago
            """
            self.cursor.execute(sql, (mes,))
            
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            return []
        finally:
            self.cursor.close()
            self.db.close()

    def obtener_fecha_pago_profesional(self, id_profesional):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
            
            sql = """
                SELECT strftime('%m', substr(fecha_pago, 7, 4) || '-' || substr(fecha_pago, 4, 2) || '-' || substr(fecha_pago, 1, 2)) 
                FROM pagos_profesionales 
                WHERE profesional_id = ?
            """
            self.cursor.execute(sql, (id_profesional,))
            
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            return []
        finally:
            self.cursor.close()
            self.db.close()