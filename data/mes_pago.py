import sqlite3
import conexion as con

class MesPagoData():

    init = False

    def __init__(self):
        if not MesPagoData.init:
            try:
                self.conn = con.Conexion()  # Usa la instancia de Conexion
                self.db = self.conn.conectar()
                self.cursor = self.db.cursor()

                sql_create_pagos = """ CREATE TABLE IF NOT EXISTS mes_pago (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_profesional INTEGER,
                    total TEXT,
                    mes TEXT,
                    UNIQUE (id_profesional, mes)                    
                ) """
                self.cursor.execute(sql_create_pagos)
                self.db.commit()
                print("Tabla Mes Pago creada")
                #self.crear_datos()  # Solo creará datos si la tabla está vacía
                MesPagoData.init = True
            except sqlite3.Error as ex:
                print("Error al crear la tabla Pagos profesionales:", ex)
            except Exception as ex:
                print("Error inesperado al crear la tabla Pagos profesionales:", ex)
            finally:
                if hasattr(self, 'cursor') and self.cursor:
                    self.cursor.close()
                if hasattr(self, 'db') and self.db:
                    self.db.close()

    def guardar_pago(self, id_profesional, total, mes):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()

            # Consulta para insertar el archivo
            consulta = """
            INSERT INTO mes_pago (id_profesional, total, mes)
            VALUES (?, ?, ?)
            """
            self.cursor.execute(consulta, (id_profesional, total, mes))
            
            self.db.commit()
            return True, ""
        except Exception as ex:
            return False, str(ex)
        finally:
            self.cursor.close()
            self.db.close()
        
    def obtener_profesionales_por_mes(self, mes):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()

            # Consulta para obtener los archivos del mes especificado
            consulta = """
            SELECT *
            FROM mes_pago
            WHERE mes = ?
            """
            self.cursor.execute(consulta, (mes,))
            archivos = self.cursor.fetchall()
            
            return archivos
        except Exception as e:
            print(f"Error al obtener archivos: {e}")
            return []
        finally:
            self.cursor.close()
            self.db.close()

    def obtener_busqueda(self, apellido, codigo):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()
        
            consulta = """
                SELECT profesionales.apellido, profesionales.nombre, profesionales.codTransf, mes_pago.mes, mes_pago.total
                FROM mes_pago
                JOIN profesionales ON mes_pago.id_profesional = profesionales.id
                WHERE UPPER(profesionales.apellido) LIKE ? OR profesionales.codTransf LIKE ?
                """
            self.cursor.execute(consulta, (f"%{apellido}%", f"%{codigo}%"))

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener archivos: {e}")
            return []
        finally:
            self.cursor.close()
            self.db.close()