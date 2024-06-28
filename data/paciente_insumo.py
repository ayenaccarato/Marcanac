import sqlite3
import conexion as con

class PacienteInsumoData:

    def __init__(self):
        try:
            self.db = con.Conexion("marcanac.db").conectar()
            self.cursor = self.db.cursor()
            sql_create_paciente_insumo = """
            CREATE TABLE IF NOT EXISTS paciente_insumo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER,
                insumo_id INTEGER,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
                FOREIGN KEY (insumo_id) REFERENCES insumos(id),
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
            self.db = con.Conexion("marcanac.db").conectar()
            self.cursor = self.db.cursor()
            self.cursor.execute("""
            INSERT INTO paciente_insumo (paciente_id, insumo_id) 
            VALUES ('{}', '{}')
            """, (paciente_id, insumo_id))
            self.db.commit()
            print("Asociación paciente-insumo creada correctamente")
            return True
        except sqlite3.Error as e:
            print(f"Error al asociar insumo a paciente: {e}")
            return False

    def obtener_insumos_de_paciente(self, paciente_id):
        try:
            self.db = con.Conexion("marcanac.db").conectar()
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

    # Agrega métodos similares para otras operaciones CRUD según sea necesario
