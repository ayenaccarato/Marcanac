import sqlite3
import conexion as con
from PyQt6.QtWidgets import QMessageBox

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
            visitas TEXT,
            valor TEXT,
            total TEXT,
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
            
            sql_insert_paciente_profesional = """
            INSERT INTO paciente_profesionales (paciente_id, profesional_id, visitas, valor, total) 
            VALUES (?, ?, ?, ?, ?)
            """
            self.cursor.execute(sql_insert_paciente_profesional, (paciente_id, profesional_id, '0', '0', '0'))
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
            ORDER BY apellido
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
            SELECT pacientes.id, pacientes.nombre, pacientes.apellido, visitas, valor, total
            FROM paciente_profesionales
            JOIN pacientes ON paciente_profesionales.paciente_id = pacientes.id
            WHERE paciente_profesionales.profesional_id = ?
            ORDER BY apellido
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
                DELETE FROM paciente_profesionales
                WHERE paciente_id = ? AND profesional_id = ?
            ''', (paciente_id, profesional_id))
            self.db.commit()
            return True, ""
        except Exception as ex:
            return False, str(ex)
        # except sqlite3.Error as e:
        #     print(f"Error al eliminar la relación: {e}")
        finally:
            if self.db:
                self.db.close()

    def actualizar_dato(self, id_paciente, id_profesional, columna, nuevo_valor):
        try:
            self.db = con.Conexion().conectar()
            self.cursor = self.db.cursor()

                # Convertir el nuevo valor a número si es necesario
            try:
                nuevo_valor = float(nuevo_valor)
            except ValueError:
                return False, "El valor ingresado no es numérico"

            # Construir la consulta para actualizar la columna especificada
            columnas = ['visitas', 'valor', 'total']
            if columna in [3, 4]:  # Columnas editables: visitas (3) y valor (4)
                # Obtener los valores actuales de visitas y valor
                consulta = """
                SELECT visitas, valor 
                FROM paciente_profesionales 
                WHERE paciente_id = ? AND profesional_id = ?
                """
                self.cursor.execute(consulta, (id_paciente, id_profesional))
                result = self.cursor.fetchone()
                if result:
                    visitas_actuales, valor_actual = result
                    visitas_actuales = float(visitas_actuales) if visitas_actuales else 0
                    valor_actual = float(valor_actual) if valor_actual else 0

                    if columna == 3:  # Si se está actualizando visitas
                        visitas_actuales = nuevo_valor
                    elif columna == 4:  # Si se está actualizando valor
                        valor_actual = nuevo_valor

                    # Calcular el nuevo total
                    total = visitas_actuales * valor_actual

                    # Actualizar la columna especificada
                    if columna == 3:
                        consulta = "UPDATE paciente_profesionales SET visitas = ?, total = ? WHERE paciente_id = ? AND profesional_id = ?"
                        self.cursor.execute(consulta, (nuevo_valor, total, id_paciente, id_profesional))
                    elif columna == 4:
                        consulta = "UPDATE paciente_profesionales SET valor = ?, total = ? WHERE paciente_id = ? AND profesional_id = ?"
                        self.cursor.execute(consulta, (nuevo_valor, total, id_paciente, id_profesional))
                    elif columna == 5:  # En caso de actualizar directamente el total
                        consulta = "UPDATE paciente_profesionales SET total = ? WHERE paciente_id = ? AND profesional_id = ?"
                        self.cursor.execute(consulta, (nuevo_valor, id_paciente, id_profesional))

                    self.db.commit()
                    return True, ""
                else:
                    return False, "No se encontraron datos para actualizar"
        except Exception as ex:
            return False, str(ex)
        finally:
            if self.cursor:
                self.cursor.close()
            if self.db:
                self.db.close()
